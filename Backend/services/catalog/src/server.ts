import { startService } from '@perfumespayday/shared';
import { envSchema } from './config/env.js';

await startService({ name: 'catalog', envSchema });
