import cors from '@fastify/cors';
import httpProxy from '@fastify/http-proxy';
import rateLimit from '@fastify/rate-limit';
import type { FastifyInstance } from 'fastify';
import type { IncomingHttpHeaders } from 'node:http';
import { AppError, errorEnvelope } from '@perfumespayday/shared';
import type { GatewayEnv } from './config/env.js';
import {
  gatewayRoutes,
  type GatewayRoute,
  type UpstreamName,
} from './config/routes.js';

/** Cabeceras que no deben reenviarse entre saltos HTTP. */
const HOP_BY_HOP_HEADERS = [
  'connection',
  'keep-alive',
  'proxy-authenticate',
  'proxy-authorization',
  'te',
  'trailer',
  'transfer-encoding',
  'upgrade',
] as const;

/** Cabeceras internas que el gateway nunca debe propagar. */
const INTERNAL_HEADERS = ['x-internal-token', 'x-service-token'] as const;

/**
 * Registra CORS, rate limit y el proxy `/api/v1/*`.
 * Debe ejecutarse después de `configureJwtAuth` para que existan los guards.
 */
export async function registerGateway(
  app: FastifyInstance,
  env: GatewayEnv,
): Promise<void> {
  await app.register(cors, {
    origin: parseCorsOrigins(env.CORS_ORIGINS),
    credentials: true,
    methods: ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: [
      'Content-Type',
      'Authorization',
      'Idempotency-Key',
      'X-Request-Id',
    ],
    exposedHeaders: [
      'X-Request-Id',
      'Retry-After',
      'X-RateLimit-Limit',
      'X-RateLimit-Remaining',
      'X-RateLimit-Reset',
    ],
    maxAge: 86_400,
  });

  await app.register(rateLimit, {
    global: true,
    max: env.RATE_LIMIT_MAX,
    timeWindow: env.RATE_LIMIT_WINDOW,
    errorResponseBuilder: () =>
      new AppError(
        'RATE_LIMITED',
        'Demasiadas peticiones. Intenta de nuevo más tarde.',
        429,
      ),
  });

  const upstreams: Record<UpstreamName, string> = {
    security: env.SECURITY_SERVICE_URL,
    catalog: env.CATALOG_SERVICE_URL,
    orders: env.ORDERS_SERVICE_URL,
  };

  for (const route of gatewayRoutes) {
    await registerProxyRoute(app, route, upstreams[route.upstream], env);
  }
}

async function registerProxyRoute(
  app: FastifyInstance,
  route: GatewayRoute,
  upstream: string,
  env: GatewayEnv,
): Promise<void> {
  await app.register(async (scope) => {
    const adminGuard =
      route.auth === 'admin' ? scope.requireRole('admin') : undefined;

    scope.addHook('preHandler', async (request, reply) => {
      if (route.auth === 'public') {
        return;
      }

      await scope.authenticate(request, reply, () => undefined);

      if (adminGuard) {
        await adminGuard.call(scope, request, reply, () => undefined);
      }
    });

    await scope.register(httpProxy, {
      upstream,
      prefix: route.prefix,
      // Conserva `/api/v1/...`; los servicios internos usan el mismo contrato.
      rewritePrefix: route.prefix,
      ...(route.methods ? { httpMethods: route.methods } : {}),
      ...(route.authRateLimit
        ? {
            config: {
              rateLimit: {
                max: env.AUTH_RATE_LIMIT_MAX,
                timeWindow: env.RATE_LIMIT_WINDOW,
              },
            },
          }
        : {}),
      replyOptions: {
        timeout: env.PROXY_TIMEOUT_MS,
        rewriteRequestHeaders: (request, headers) =>
          forwardHeaders(request, headers),
        rewriteHeaders: (headers) => {
          // El gateway es el único que define CORS; evita cabeceras duplicadas.
          for (const name of Object.keys(headers)) {
            if (name.toLowerCase().startsWith('access-control-')) {
              delete (headers as Record<string, unknown>)[name];
            }
          }
          return headers;
        },
        onError: (reply, { error }) => {
          reply.log.error(
            { err: error },
            'Error al contactar el servicio interno',
          );

          if (reply.sent) {
            return;
          }

          reply
            .code(503)
            .send(
              errorEnvelope(
                'UPSTREAM_UNAVAILABLE',
                'El servicio solicitado no está disponible.',
                reply.request.id,
              ),
            );
        },
      },
    });
  });
}

/** Reenvía la petición con un `x-request-id` correlacionable y sin cabeceras internas. */
function forwardHeaders(
  request: { id: string },
  headers: IncomingHttpHeaders,
): IncomingHttpHeaders {
  const forwarded: IncomingHttpHeaders = {
    ...headers,
    'x-request-id': request.id,
  };

  for (const name of [...HOP_BY_HOP_HEADERS, ...INTERNAL_HEADERS]) {
    delete forwarded[name];
  }

  return forwarded;
}

/**
 * Convierte la lista de orígenes en la configuración de `@fastify/cors`.
 * El esquema de entorno ya rechaza el comodín `*`.
 */
function parseCorsOrigins(value: string): string[] {
  return value
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean);
}
