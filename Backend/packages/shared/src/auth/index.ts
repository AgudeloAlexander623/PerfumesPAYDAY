export { authClaimsSchema, hasRole, roleSchema } from './claims.js';
export type { AuthClaims, Role } from './claims.js';
export { createVerificationKey, normalizePem } from './keys.js';
export type { JwtKeyOptions, JwtVerificationKey } from './keys.js';
export { createJwtVerifier } from './verify.js';
export type { JwtVerifier, JwtVerifierOptions } from './verify.js';
export { configureJwtAuth, registerAuth, registerAuthWithVerifier } from './plugin.js';
export type { AuthOptions, JwtAuthEnv } from './plugin.js';
