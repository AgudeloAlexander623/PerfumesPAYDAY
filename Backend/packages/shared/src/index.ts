export { createApp } from './app.js';
export type { CreateAppOptions } from './app.js';
export {
  authClaimsSchema,
  configureJwtAuth,
  createJwtVerifier,
  createVerificationKey,
  hasRole,
  normalizePem,
  registerAuth,
  registerAuthWithVerifier,
  roleSchema,
} from './auth/index.js';
export type {
  AuthClaims,
  AuthOptions,
  JwtAuthEnv,
  JwtKeyOptions,
  JwtVerificationKey,
  JwtVerifier,
  JwtVerifierOptions,
  Role,
} from './auth/index.js';
export { baseEnvSchema, jwtEnvSchema, loadEnv, portSchema } from './env.js';
export type { BaseEnv, JwtEnv, ServiceEnv, ServiceEnvSchema } from './env.js';
export { AppError, errorEnvelope } from './errors.js';
export type { ErrorDetail, ErrorResponse } from './errors.js';
export { startServer, startService } from './lifecycle.js';
export type { StartServiceOptions } from './lifecycle.js';
