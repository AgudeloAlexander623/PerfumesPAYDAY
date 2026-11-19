import { configureJwtAuth, startService } from '@perfumespayday/shared';
import { envSchema } from './config/env.js';
import { registerGateway } from './gateway.js';

await startService({
  name: 'gateway',
  envSchema,
  setup: async (app, env) => {
    await configureJwtAuth(app, env);
    await registerGateway(app, env);
  },
});
