import { z } from 'zod';
/** Variables que todo servicio comparte. */
export const baseEnvSchema = z.object({
    NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
    HOST: z.string().min(1).default('0.0.0.0'),
    LOG_LEVEL: z
        .enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace', 'silent'])
        .default('info'),
});
/** Puerto validado con un valor por defecto propio de cada servicio. */
export function portSchema(fallback) {
    return z.coerce.number().int().min(1).max(65535).default(fallback);
}
/**
 * Valida `process.env` contra el esquema del servicio.
 * El mensaje no incluye valores para no filtrar secretos en los logs.
 */
export function loadEnv(schema) {
    const result = schema.safeParse(process.env);
    if (!result.success) {
        const problems = result.error.issues
            .map((issue) => `${issue.path.join('.') || 'env'}: ${issue.message}`)
            .join('; ');
        throw new Error(`Configuración de entorno inválida (${problems})`);
    }
    return result.data;
}
//# sourceMappingURL=env.js.map