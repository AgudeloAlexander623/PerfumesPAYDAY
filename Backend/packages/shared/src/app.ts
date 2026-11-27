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
  });

  await app.register(helmet);
  registerErrorHandler(app);

  app.get('/health', async () => ({ status: 'ok', service: name }));

  return app;
}
