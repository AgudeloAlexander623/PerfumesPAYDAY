import {
  createRemoteJWKSet,
  customFetch,
  importSPKI,
  type CryptoKey,
  type FetchImplementation,
  type JWTVerifyGetKey,
  type RemoteJWKSetOptions,
} from 'jose';
import { AppError } from '../errors.js';

export const JWKS_UNAVAILABLE_MESSAGE =
  'No se pudo obtener la clave pública JWT.';

/** Convierte cualquier fallo de red o respuesta no 200 en un 503 explícito. */
const fetchJwks: FetchImplementation = async (resource, init) => {
  try {
    const response = await fetch(resource, init);

    if (!response.ok) {
      throw new AppError('UPSTREAM_UNAVAILABLE', JWKS_UNAVAILABLE_MESSAGE, 503);
    }

    return response;
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }

    throw new AppError('UPSTREAM_UNAVAILABLE', JWKS_UNAVAILABLE_MESSAGE, 503);
  }
};

/** Clave local ya importada o resolvedor JWKS remoto. */
export type JwtVerificationKey = CryptoKey | JWTVerifyGetKey;

/** Origen de la clave pública usada para validar los tokens. */
export interface JwtKeyOptions {
  /** Clave pública RS256 en PEM o su representación base64. */
  publicKey?: string;
  /** Endpoint JWKS de `security-service`; alternativa a `publicKey`. */
  jwksUrl?: string;
  /** Ajustes de caché y timeout para el JWKS remoto. */
  jwks?: RemoteJWKSetOptions;
}

/**
 * Construye la clave de verificación a partir de la configuración.
 * Se acepta una sola fuente para evitar validar contra claves ambiguas.
 */
export async function createVerificationKey(
  options: JwtKeyOptions,
): Promise<JwtVerificationKey> {
  if (options.publicKey && options.jwksUrl) {
    throw new Error('Configura JWT_PUBLIC_KEY o JWT_JWKS_URL, no ambos.');
  }

  if (options.publicKey) {
    return importSPKI(normalizePem(options.publicKey), 'RS256');
  }

  if (options.jwksUrl) {
    // jose recarga ante un kid desconocido, pero su caché por defecto es de
    // 10 min; el ADR-0003 la limita a 5 min. El cooldown de 30 s se mantiene
    // en el valor por defecto de la librería.
    return createRemoteJWKSet(new URL(options.jwksUrl), {
      cacheMaxAge: 300_000,
      [customFetch]: fetchJwks,
      ...options.jwks,
    });
  }

  throw new Error('Falta JWT_PUBLIC_KEY o JWT_JWKS_URL para validar tokens.');
}

/**
 * Acepta PEM multilínea, PEM con `\n` escapados o el PEM codificado en base64.
 * Las variables de entorno suelen perder los saltos de línea.
 */
export function normalizePem(value: string): string {
  const unescaped = value.replace(/\\n/g, '\n').trim();

  if (unescaped.includes('-----BEGIN')) {
    return unescaped;
  }

  const decoded = Buffer.from(unescaped, 'base64').toString('utf8').trim();

  if (!decoded.includes('-----BEGIN')) {
    throw new Error('La clave pública JWT no es un PEM válido.');
  }

  return decoded;
}
