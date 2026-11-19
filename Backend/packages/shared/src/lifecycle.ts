import type { FastifyInstance } from 'fastify';
import type { z } from 'zod';
import { createApp } from './app.js';
import { loadEnv, type ServiceEnv } from './env.js';

async function shutdown(app: FastifyInstance, signal: NodeJS.Signals): Promise<void> {
  app.log.info({ signal }, 'Cerrando servicio');
  try {
    await app.close();
    process.exit(0);
  } catch (error) {
    app.log.error({ err: error }, 'Error al cerrar el servicio');
    process.exit(1);
  }
}

/** Arranca un servicio y registra el cierre ordenado ante SIGINT y SIGTERM. */
export async function startServer(
  app: FastifyInstance,
  options: { host: string; port: number },
): Promise<void> {
  for (const signal of ['SIGINT', 'SIGTERM'] as const) {
    process.once(signal, () => {
      void shutdown(app, signal);
    });
  }

  try {
    await app.listen(options);
  } catch (error) {
    app.log.error({ err: error }, 'No se pudo iniciar el servicio');
    process.exit(1);
  }
}

/** Opciones de arranque común a todos los servicios. */
export interface StartServiceOptions<T extends ServiceEnv = ServiceEnv> {
  name: string;
  envSchema: z.ZodType<T>;
  /**
   * Configura la app antes de escuchar: autenticación, plugins y rutas.
   * Se ejecuta después de `createApp` y antes de `listen`.
   */
  setup?: (app: FastifyInstance, env: T) => Promise<void> | void;
}

/** Punto de entrada común: valida el entorno, crea la app y la arranca. */
export async function startService<T extends ServiceEnv>(
  options: StartServiceOptions<T>,
): Promise<void> {
  try {
    const env = loadEnv(options.envSchema);
    const app = await createApp({ name: options.name, logLevel: env.LOG_LEVEL });
    await options.setup?.(app, env);
    await startServer(app, { host: env.HOST, port: env.PORT });
  } catch (error) {
    console.error(error instanceof Error ? error.message : error);
    process.exit(1);
  }
}
