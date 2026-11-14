import type {
  FastifyInstance,
  FastifyReply,
  FastifyRequest,
  preHandlerHookHandler,
} from 'fastify';
import type { JwtEnv } from '../env.js';
import { AppError } from '../errors.js';
import { hasRole, type AuthClaims, type Role } from './claims.js';
import { createJwtVerifier, type JwtVerifier, type JwtVerifierOptions } from './verify.js';

/** Variables de entorno mínimas para configurar la autenticación. */
export interface JwtAuthEnv extends JwtEnv {
  NODE_ENV: 'development' | 'test' | 'production';
}

export interface AuthOptions extends JwtVerifierOptions {}

declare module 'fastify' {
  interface FastifyRequest {
    /** Claims validados del access token; `null` si la ruta no exige autenticación. */
    auth: AuthClaims | null;
  }

  interface FastifyInstance {
    /** Pre-handler que exige un access token válido y adjunta `request.auth`. */
    authenticate: preHandlerHookHandler;
    /** Pre-handler que exige al menos uno de los roles indicados. */
    requireRole: (...roles: Role[]) => preHandlerHookHandler;
  }
}

function bearerToken(request: FastifyRequest): string {
  const header = request.headers.authorization;

  if (!header) {
    throw new AppError('UNAUTHORIZED', 'Se requiere un token de acceso.', 401);
  }

  const [scheme, token, ...rest] = header.trim().split(/\s+/);

  if (scheme?.toLowerCase() !== 'bearer' || !token || rest.length > 0) {
    throw new AppError(
      'UNAUTHORIZED',
      'La cabecera Authorization debe usar el esquema Bearer.',
      401,
    );
  }

  return token;
}

/**
 * Registra `request.auth`, `app.authenticate` y `app.requireRole` con un verificador ya construido.
 * Debe llamarse antes de declarar las rutas que usan los guards.
 */
export function registerAuthWithVerifier(
  app: FastifyInstance,
  verifier: JwtVerifier,
): void {
  app.decorateRequest('auth', null);

  const authenticate: preHandlerHookHandler = async (request: FastifyRequest) => {
    request.auth = await verifier.verify(bearerToken(request));
  };

  const requireRole = (...roles: Role[]): preHandlerHookHandler => {
    return async (request: FastifyRequest, _reply: FastifyReply) => {
      if (!request.auth) {
        throw new AppError('UNAUTHORIZED', 'Se requiere autenticación.', 401);
      }

      if (!hasRole(request.auth, ...roles)) {
        throw new AppError(
          'FORBIDDEN',
          'No tienes permisos para realizar esta operación.',
          403,
        );
      }
    };
  };

  app.decorate('authenticate', authenticate);
  app.decorate('requireRole', requireRole);
}

/**
 * Registra `request.auth`, `app.authenticate` y `app.requireRole`.
 * Debe llamarse antes de declarar las rutas que usan los guards.
 */
export async function registerAuth(
  app: FastifyInstance,
  options: AuthOptions,
): Promise<void> {
  registerAuthWithVerifier(app, await createJwtVerifier(options));
}

/**
 * Configura la autenticación a partir del entorno de un servicio.
 * En desarrollo permite arrancar sin clave para no frenar el trabajo local;
 * en producción exige una fuente de clave.
 */
export async function configureJwtAuth(
  app: FastifyInstance,
  env: JwtAuthEnv,
): Promise<void> {
  if (!env.JWT_PUBLIC_KEY && !env.JWT_JWKS_URL) {
    if (env.NODE_ENV === 'production') {
      throw new Error(
        'JWT_PUBLIC_KEY o JWT_JWKS_URL es obligatorio en producción.',
      );
    }

    app.log.warn(
      'Autenticación JWT sin clave: las rutas protegidas responderán 401. Configura JWT_PUBLIC_KEY o JWT_JWKS_URL.',
    );

    registerAuthWithVerifier(app, {
      async verify() {
        throw new AppError(
          'UNAUTHORIZED',
          'La autenticación no está configurada.',
          401,
        );
      },
    });
    return;
  }

  await registerAuth(app, {
    ...(env.JWT_PUBLIC_KEY ? { publicKey: env.JWT_PUBLIC_KEY } : {}),
    ...(env.JWT_JWKS_URL ? { jwksUrl: env.JWT_JWKS_URL } : {}),
    issuer: env.JWT_ISSUER,
    audience: env.JWT_AUDIENCE,
  });
}
