import {
  createRemoteJWKSet,
  importSPKI,
  type CryptoKey,
  type JWTVerifyGetKey,
  type RemoteJWKSetOptions,
} from 'jose';

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
    return createRemoteJWKSet(new URL(options.jwksUrl), options.jwks);
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
