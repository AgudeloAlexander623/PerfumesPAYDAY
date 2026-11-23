import { createApp } from './app.js';
import { loadEnv } from './env.js';
async function shutdown(app, signal) {
    app.log.info({ signal }, 'Cerrando servicio');
    try {
        await app.close();
        process.exit(0);
    }
    catch (error) {
        app.log.error({ err: error }, 'Error al cerrar el servicio');
        process.exit(1);
    }
}
/** Arranca un servicio y registra el cierre ordenado ante SIGINT y SIGTERM. */
export async function startServer(app, options) {
    for (const signal of ['SIGINT', 'SIGTERM']) {
        process.once(signal, () => {
            void shutdown(app, signal);
        });
    }
    try {
        await app.listen(options);
    }
    catch (error) {
        app.log.error({ err: error }, 'No se pudo iniciar el servicio');
        process.exit(1);
    }
}
/** Punto de entrada común: valida el entorno, crea la app y la arranca. */
export async function startService(options) {
    try {
        const env = loadEnv(options.envSchema);
        const app = await createApp({ name: options.name, logLevel: env.LOG_LEVEL });
        await startServer(app, { host: env.HOST, port: env.PORT });
    }
    catch (error) {
        console.error(error instanceof Error ? error.message : error);
        process.exit(1);
    }
}
//# sourceMappingURL=lifecycle.js.map