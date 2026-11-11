import { randomUUID } from 'node:crypto';
import helmet from '@fastify/helmet';
import Fastify, {} from 'fastify';
import { registerErrorHandler } from './errors.js';
/**
 * Construye la aplicación Fastify con lo transversal a todos los servicios:
 * logs, requestId, cabeceras de seguridad, salud y manejo de errores.
 */
export async function createApp({ name, logLevel = 'info', }) {
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
//# sourceMappingURL=app.js.map