import { baseEnvSchema, portSchema, type ServiceEnvSchema } from '@perfumespayday/shared';

export const envSchema: ServiceEnvSchema = baseEnvSchema.extend({
  PORT: portSchema(3002),
});
