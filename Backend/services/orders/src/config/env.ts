import type { z } from 'zod';
import {
  baseEnvSchema,
  jwtEnvSchema,
  portSchema,
  type JwtEnv,
  type ServiceEnv,
} from '@perfumespayday/shared';

export type OrdersEnv = ServiceEnv & JwtEnv;

export const envSchema: z.ZodType<OrdersEnv> = baseEnvSchema
  .extend(jwtEnvSchema.shape)
  .extend({
    PORT: portSchema(3002),
  });
