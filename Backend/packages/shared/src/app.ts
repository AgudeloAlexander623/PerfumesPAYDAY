import { randomUUID } from 'node:crypto';
import helmet from '@fastify/helmet';
import Fastify, { type FastifyInstance } from 'fastify';
import { registerErrorHandler } from './errors.js';

export interface CreateAppOptions {
  /** Nombre que se reporta en `/health` y en los logs. */
  name: string;
  /** Nivel de Pino; por defecto `info`. */
  logLevel?: string;
}

/**
 * Construye la aplicación Fastify con lo transversal a todos los servicios:
 * logs, requestId, cabeceras de seguridad, salud y manejo de errores.
 */
export async function createApp({
  name,
  logLevel = 'info',
}: CreateAppOptions): Promise<FastifyInstance> {
  const app = Fastify({
    logger: { level: logLevel },
    requestIdHeader: 'x-request-id',
    genReqId: () => randomUUID(),
  });

  app.addHook('onSend', async (request, reply) => {
    reply.header('x-request-id', request.id);

    // El receptor de un 401 debe saber que debe renovar o autenticarse de nuevo.
    // Se aplica aquí una sola vez para cubrir todos los servicios y todos los 401.
    if (reply.statusCode === 401) {
      reply.header('WWW-Authenticate', 'Bearer');
    }
  });

  await app.register(helmet);
  registerErrorHandler(app);

  app.get('/health', async () => ({ status: 'ok', service: name }));

  return app;
}
