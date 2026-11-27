import { jwtVerify, type JWSAlgorithm } from 'jose';
import { AppError } from '../errors.js';
import { authClaimsSchema, type AuthClaims } from './claims.js';
import { createVerificationKey, type JwtKeyOptions } from './keys.js';

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

  return {
    async verify(token: string): Promise<AuthClaims> {
      try {
        const { payload } = await jwtVerify(token, key, verifyOptions);
        const claims = authClaimsSchema.safeParse(payload);

        if (!claims.success) {
          throw new AppError('UNAUTHORIZED', UNAUTHORIZED_MESSAGE, 401);
        }

        return claims.data;
      } catch (error) {
        if (error instanceof AppError) {
          throw error;
        }

        throw new AppError('UNAUTHORIZED', UNAUTHORIZED_MESSAGE, 401);
      }
    },
  };
}
