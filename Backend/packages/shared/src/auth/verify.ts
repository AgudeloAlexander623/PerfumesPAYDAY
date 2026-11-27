import { errors as joseErrors, jwtVerify, type JWSAlgorithm } from 'jose';
import { AppError } from '../errors.js';
import { authClaimsSchema, type AuthClaims } from './claims.js';
import {
  createVerificationKey,
  JWKS_UNAVAILABLE_MESSAGE,
  type JwtKeyOptions,
  type JwtVerificationKey,
} from './keys.js';

/** Configuración para validar access tokens RS256. */
export interface JwtVerifierOptions extends JwtKeyOptions {
  /** Emisor esperado; debe coincidir con `security-service`. */
  issuer: string;
  /** Audiencia esperada por la API. */
  audience: string;
  /** Tolerancia de reloj en segundos; por defecto 5. */
  clockToleranceSeconds?: number;
}

export interface JwtVerifier {
  /** Valida firma, vigencia y claims. Lanza `AppError` 401 si algo falla. */
  verify(token: string): Promise<AuthClaims>;
}

const UNAUTHORIZED_MESSAGE = 'Token de acceso inválido o expirado.';
const ALGORITHMS: JWSAlgorithm[] = ['RS256'];

/** El resolvedor remoto expone `reload`; una clave local no lo necesita. */
type ReloadableKey = JwtVerificationKey & { reload?: () => Promise<void> };

function authFailure(error: unknown): AppError {
  if (error instanceof AppError) {
    return error;
  }

  // Un timeout al buscar el JWKS es una dependencia caída, no un token malo.
  if (error instanceof joseErrors.JWKSTimeout) {
    return new AppError('UPSTREAM_UNAVAILABLE', JWKS_UNAVAILABLE_MESSAGE, 503);
  }

  return new AppError('UNAUTHORIZED', UNAUTHORIZED_MESSAGE, 401);
}

/**
 * Crea un verificador reutilizable. La clave se importa una sola vez;
 * el JWKS remoto cachea las claves según `jose`.
 */
export async function createJwtVerifier(
  options: JwtVerifierOptions,
): Promise<JwtVerifier> {
  const key = await createVerificationKey(options);

  const verifyOptions = {
    algorithms: ALGORITHMS,
    issuer: options.issuer,
    audience: options.audience,
    clockTolerance: options.clockToleranceSeconds ?? 5,
  };

  const validate = async (token: string): Promise<AuthClaims> => {
    const { payload } = await jwtVerify(token, key, verifyOptions);
    const claims = authClaimsSchema.safeParse(payload);

    if (!claims.success) {
      throw new AppError('UNAUTHORIZED', UNAUTHORIZED_MESSAGE, 401);
    }

    return claims.data;
  };

  return {
    async verify(token: string): Promise<AuthClaims> {
      try {
        return await validate(token);
      } catch (error) {
        const reloadableKey = key as ReloadableKey;

        // jose espera 30 s antes de recargar por su cooldown; al rotar, ese
        // primer token con el kid nuevo debe refrescar el JWKS de inmediato.
        if (
          error instanceof joseErrors.JWKSNoMatchingKey &&
          typeof reloadableKey.reload === 'function'
        ) {
          try {
            await reloadableKey.reload();
            return await validate(token);
          } catch (retryError) {
            throw authFailure(retryError);
          }
        }

        throw authFailure(error);
      }
    },
  };
}
