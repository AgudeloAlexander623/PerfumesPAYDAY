import { z } from 'zod';
/** Variables que todo servicio comparte. */
export declare const baseEnvSchema: z.ZodObject<{
    NODE_ENV: z.ZodDefault<z.ZodEnum<{
        development: "development";
        production: "production";
        test: "test";
    }>>;
    HOST: z.ZodDefault<z.ZodString>;
    LOG_LEVEL: z.ZodDefault<z.ZodEnum<{
        debug: "debug";
        error: "error";
        fatal: "fatal";
        info: "info";
        silent: "silent";
        trace: "trace";
        warn: "warn";
    }>>;
}, z.core.$strip>;
export type BaseEnv = z.infer<typeof baseEnvSchema>;
/** Configuración mínima que necesita `startService` para escuchar. */
export interface ServiceEnv extends BaseEnv {
    PORT: number;
}
export type ServiceEnvSchema = z.ZodType<ServiceEnv>;
/** Puerto validado con un valor por defecto propio de cada servicio. */
export declare function portSchema(fallback: number): z.ZodDefault<z.ZodCoercedNumber<unknown>>;
/**
 * Valida `process.env` contra el esquema del servicio.
 * El mensaje no incluye valores para no filtrar secretos en los logs.
 */
export declare function loadEnv<T>(schema: z.ZodType<T>): T;
//# sourceMappingURL=env.d.ts.map