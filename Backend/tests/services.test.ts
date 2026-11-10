import { describe, expect, it } from 'vitest';
import { createApp } from '@perfumespayday/shared';
import { envSchema as catalogEnv } from '../services/catalog/src/config/env.js';
import { envSchema as gatewayEnv } from '../services/gateway/src/config/env.js';
import { envSchema as ordersEnv } from '../services/orders/src/config/env.js';

const services = [
  ['gateway', gatewayEnv],
  ['catalog', catalogEnv],
  ['orders', ordersEnv],
] as const;

describe.each(services)('%s', (name, envSchema) => {
  it('arranca con su configuración y responde /health', async () => {
    const env = envSchema.parse({});
    const app = await createApp({ name, logLevel: 'silent' });
    expect(env.PORT).toBeGreaterThan(0);

    const response = await app.inject({ method: 'GET', url: '/health' });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ status: 'ok', service: name });

    await app.close();
  });
});
