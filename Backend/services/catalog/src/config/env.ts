import type { z } from 'zod';
import {
  baseEnvSchema,
  jwtEnvSchema,
  portSchema,
  type JwtEnv,
  type ServiceEnv,
} from '@perfumespayday/shared';

export type CatalogEnv = ServiceEnv & JwtEnv;

export const envSchema: z.ZodType<CatalogEnv> = baseEnvSchema
  .extend(jwtEnvSchema.shape)
  .extend({
    PORT: portSchema(3001),
  });
