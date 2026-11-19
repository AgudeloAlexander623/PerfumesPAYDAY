import { configureJwtAuth, startService } from '@perfumespayday/shared';
import { envSchema } from './config/env.js';

await startService({
  name: 'orders',
  envSchema,
  setup: async (app, env) => {
    await configureJwtAuth(app, env);
  },
});
