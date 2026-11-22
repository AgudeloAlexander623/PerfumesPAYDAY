import { type FastifyInstance } from 'fastify';
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
export declare function createApp({ name, logLevel, }: CreateAppOptions): Promise<FastifyInstance>;
//# sourceMappingURL=app.d.ts.map