import type { FastifyInstance } from 'fastify';
import { type ServiceEnvSchema } from './env.js';
/** Arranca un servicio y registra el cierre ordenado ante SIGINT y SIGTERM. */
export declare function startServer(app: FastifyInstance, options: {
    host: string;
    port: number;
}): Promise<void>;
/** Punto de entrada común: valida el entorno, crea la app y la arranca. */
export declare function startService(options: {
    name: string;
    envSchema: ServiceEnvSchema;
}): Promise<void>;
//# sourceMappingURL=lifecycle.d.ts.map