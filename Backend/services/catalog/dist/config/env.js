import { baseEnvSchema, portSchema } from '@perfumespayday/shared';
export const envSchema = baseEnvSchema.extend({
    PORT: portSchema(3001),
});
//# sourceMappingURL=env.js.map