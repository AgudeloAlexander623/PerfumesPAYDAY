import { configureJwtAuth, startService } from '@perfumespayday/shared';
import { envSchema } from './config/env.js';

await startService({
  name: 'catalog',
  envSchema,
  setup: async (app, env) => {
    await configureJwtAuth(app, env);
  },
});
