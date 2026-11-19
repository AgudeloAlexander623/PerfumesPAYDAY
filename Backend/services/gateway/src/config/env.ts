import { z } from 'zod';
import { baseEnvSchema, jwtEnvSchema, portSchema } from '@perfumespayday/shared';

const gatewayEnvSchema = baseEnvSchema.extend(jwtEnvSchema.shape).extend({
  PORT: portSchema(3000),
  /**
   * Orígenes permitidos, separados por coma. Deben ser explícitos: el refresh
   * token viaja en cookie y el comodín `*` habilitaría CSRF.
   */
  CORS_ORIGINS: z
    .string()
    .min(1)
    .default('http://localhost:5173')
    .refine(
      (value) => !value.split(',').some((origin) => origin.trim() === '*'),
      'CORS_ORIGINS debe listar orígenes explícitos; el refresh token usa cookies.',
    ),
  RATE_LIMIT_MAX: z.coerce.number().int().positive().default(100),
  RATE_LIMIT_WINDOW: z.string().min(1).default('1 minute'),
  /** Límite más estricto para registro, login y refresh. */
  AUTH_RATE_LIMIT_MAX: z.coerce.number().int().positive().default(10),
  PROXY_TIMEOUT_MS: z.coerce.number().int().positive().default(5000),
  SECURITY_SERVICE_URL: z.url().default('http://localhost:8000'),
  CATALOG_SERVICE_URL: z.url().default('http://localhost:3001'),
  ORDERS_SERVICE_URL: z.url().default('http://localhost:3002'),
});

export type GatewayEnv = z.infer<typeof gatewayEnvSchema>;

export const envSchema: z.ZodType<GatewayEnv> = gatewayEnvSchema;
