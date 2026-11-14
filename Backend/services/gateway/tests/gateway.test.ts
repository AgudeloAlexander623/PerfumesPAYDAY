import Fastify, { type FastifyInstance } from 'fastify';
import { exportSPKI, generateKeyPair, SignJWT, type CryptoKey } from 'jose';
import { afterAll, beforeAll, beforeEach, describe, expect, it } from 'vitest';
import { configureJwtAuth, createApp } from '@perfumespayday/shared';
import { envSchema } from '../src/config/env.js';
import { registerGateway } from '../src/gateway.js';

const ISSUER = 'perfumespayday-security';
const AUDIENCE = 'perfumespayday-api';
const SUBJECT = '11111111-1111-4111-8111-111111111111';

interface UpstreamCall {
  method: string;
  url: string;
  headers: Record<string, string | string[] | undefined>;
}

let privateKey: CryptoKey;
let publicKeyPem: string;
let upstream: FastifyInstance;
let upstreamUrl: string;
let app: FastifyInstance;
let calls: UpstreamCall[];

function token(roles: string[] = ['customer']): Promise<string> {
  const now = Math.floor(Date.now() / 1000);

  return new SignJWT({ roles })
    .setProtectedHeader({ alg: 'RS256' })
    .setSubject(SUBJECT)
    .setIssuer(ISSUER)
    .setAudience(AUDIENCE)
    .setIssuedAt(now)
    .setExpirationTime(now + 900)
    .setJti('22222222-2222-4222-8222-222222222222')
    .sign(privateKey);
}

function authorization(bearer: string): Record<string, string> {
  return { authorization: `Bearer ${bearer}` };
}

async function buildGateway(overrides: Record<string, string> = {}): Promise<FastifyInstance> {
  const gateway = await createApp({ name: 'gateway-test', logLevel: 'silent' });
  const env = envSchema.parse({
    NODE_ENV: 'test',
    JWT_PUBLIC_KEY: publicKeyPem,
    JWT_ISSUER: ISSUER,
    JWT_AUDIENCE: AUDIENCE,
    SECURITY_SERVICE_URL: upstreamUrl,
    CATALOG_SERVICE_URL: upstreamUrl,
    ORDERS_SERVICE_URL: upstreamUrl,
    CORS_ORIGINS: 'http://localhost:5173',
    RATE_LIMIT_MAX: '1000',
    AUTH_RATE_LIMIT_MAX: '1000',
    PROXY_TIMEOUT_MS: '2000',
    ...overrides,
  });

  await configureJwtAuth(gateway, env);
  await registerGateway(gateway, env);
  return gateway;
}

beforeAll(async () => {
  const pair = await generateKeyPair('RS256');
  privateKey = pair.privateKey;
  publicKeyPem = await exportSPKI(pair.publicKey);

  upstream = Fastify({ logger: false });
  upstream.all('/*', async (request) => {
    calls.push({
      method: request.method,
      url: request.url,
      headers: { ...request.headers },
    });

    return { ok: true, method: request.method, url: request.url };
  });

  await upstream.listen({ port: 0, host: '127.0.0.1' });
  const address = upstream.server.address();

  if (!address || typeof address === 'string') {
    throw new Error('No se pudo obtener el puerto del upstream falso.');
  }

  upstreamUrl = `http://127.0.0.1:${address.port}`;
  app = await buildGateway();
});

beforeEach(() => {
  calls = [];
});

afterAll(async () => {
  await app.close();
  await upstream.close();
});

describe('rutas públicas', () => {
  it('proxifica el catálogo sin exigir token', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1/products?page=1',
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({
      ok: true,
      method: 'GET',
      url: '/api/v1/products?page=1',
    });
  });

  it('conserva el base path /api/v1 al reenviar', async () => {
    await app.inject({ method: 'GET', url: '/api/v1/brands' });

    expect(calls.at(-1)?.url).toBe('/api/v1/brands');
  });

  it('permite login sin token', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/auth/login',
      payload: { email: 'cliente@example.com', password: 'secreto' },
    });

    expect(response.statusCode).toBe(200);
    expect(calls.at(-1)?.url).toBe('/api/v1/auth/login');
  });

  it('reenvía el x-request-id y elimina cabeceras internas', async () => {
    await app.inject({
      method: 'GET',
      url: '/api/v1/categories',
      headers: {
        'x-request-id': 'request-de-prueba',
        'x-internal-token': 'no-debe-pasar',
      },
    });

    const last = calls.at(-1);
    expect(last?.headers['x-request-id']).toBe('request-de-prueba');
    expect(last?.headers['x-internal-token']).toBeUndefined();
  });
});

describe('rutas autenticadas', () => {
  it('responde 401 sin token y no llama al upstream', async () => {
    const response = await app.inject({ method: 'GET', url: '/api/v1/cart' });

    expect(response.statusCode).toBe(401);
    expect(response.json()).toMatchObject({
      error: { code: 'UNAUTHORIZED', requestId: expect.any(String) },
    });
    expect(calls).toHaveLength(0);
  });

  it('proxifica el carrito con un token de cliente', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1/cart',
      headers: authorization(await token()),
    });

    expect(response.statusCode).toBe(200);
    expect(calls.at(-1)?.url).toBe('/api/v1/cart');
    expect(calls.at(-1)?.headers.authorization).toMatch(/^Bearer /);
  });

  it('proxifica el perfil propio con un token de cliente', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1/users/me',
      headers: authorization(await token()),
    });

    expect(response.statusCode).toBe(200);
    expect(calls.at(-1)?.url).toBe('/api/v1/users/me');
  });
});

describe('rutas de administración', () => {
  it('responde 403 si el token es de cliente', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1/admin/products',
      headers: authorization(await token(['customer'])),
    });

    expect(response.statusCode).toBe(403);
    expect(response.json()).toMatchObject({
      error: { code: 'FORBIDDEN', requestId: expect.any(String) },
    });
    expect(calls).toHaveLength(0);
  });

  it('proxifica si el token es de administrador', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/api/v1/admin/orders',
      headers: authorization(await token(['admin'])),
    });

    expect(response.statusCode).toBe(200);
    expect(calls.at(-1)?.url).toBe('/api/v1/admin/orders');
  });
});

describe('CORS y errores del upstream', () => {
  it('rechaza el comodín * en CORS_ORIGINS por el refresh token en cookie', () => {
    const result = envSchema.safeParse({
      NODE_ENV: 'test',
      JWT_PUBLIC_KEY: publicKeyPem,
      JWT_ISSUER: ISSUER,
      JWT_AUDIENCE: AUDIENCE,
      CORS_ORIGINS: 'http://localhost:5173, *',
    });

    expect(result.success).toBe(false);
  });

  it('acepta varios orígenes explícitos', async () => {
    const multiOriginApp = await buildGateway({
      CORS_ORIGINS: 'http://localhost:5173,https://tienda.example.com',
    });

    const response = await multiOriginApp.inject({
      method: 'OPTIONS',
      url: '/api/v1/cart',
      headers: {
        origin: 'https://tienda.example.com',
        'access-control-request-method': 'GET',
      },
    });

    expect(response.statusCode).toBe(204);
    expect(response.headers['access-control-allow-origin']).toBe(
      'https://tienda.example.com',
    );

    await multiOriginApp.close();
  });

  it('responde el preflight con el origen permitido', async () => {
    const response = await app.inject({
      method: 'OPTIONS',
      url: '/api/v1/cart',
      headers: {
        origin: 'http://localhost:5173',
        'access-control-request-method': 'GET',
        'access-control-request-headers': 'authorization',
      },
    });

    expect(response.statusCode).toBe(204);
    expect(response.headers['access-control-allow-origin']).toBe(
      'http://localhost:5173',
    );
    expect(response.headers['access-control-allow-credentials']).toBe('true');
  });

  it('traduce la caída del upstream a 503 con envelope', async () => {
    const closed = Fastify({ logger: false });
    await closed.listen({ port: 0, host: '127.0.0.1' });
    const address = closed.server.address();

    if (!address || typeof address === 'string') {
      throw new Error('No se pudo obtener el puerto del upstream cerrado.');
    }

    const deadUrl = `http://127.0.0.1:${address.port}`;
    await closed.close();

    const failingApp = await buildGateway({
      SECURITY_SERVICE_URL: deadUrl,
      CATALOG_SERVICE_URL: deadUrl,
      ORDERS_SERVICE_URL: deadUrl,
      PROXY_TIMEOUT_MS: '500',
    });

    const response = await failingApp.inject({
      method: 'GET',
      url: '/api/v1/products',
    });

    expect(response.statusCode).toBe(503);
    expect(response.json()).toMatchObject({
      error: {
        code: 'UPSTREAM_UNAVAILABLE',
        requestId: expect.any(String),
      },
    });

    await failingApp.close();
  });

  it('aplica el límite estricto en las rutas de autenticación', async () => {
    const limitedApp = await buildGateway({ AUTH_RATE_LIMIT_MAX: '2' });

    const first = await limitedApp.inject({
      method: 'POST',
      url: '/api/v1/auth/login',
    });
    const second = await limitedApp.inject({
      method: 'POST',
      url: '/api/v1/auth/login',
    });
    const third = await limitedApp.inject({
      method: 'POST',
      url: '/api/v1/auth/login',
    });

    expect(first.statusCode).toBe(200);
    expect(second.statusCode).toBe(200);
    expect(third.statusCode).toBe(429);
    expect(third.json()).toMatchObject({
      error: {
        code: 'RATE_LIMITED',
        requestId: expect.any(String),
      },
    });

    await limitedApp.close();
  });
});
