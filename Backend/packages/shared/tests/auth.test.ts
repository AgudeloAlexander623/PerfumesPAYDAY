import type { FastifyInstance } from 'fastify';
import {
  exportJWK,
  exportSPKI,
  generateKeyPair,
  SignJWT,
  UnsecuredJWT,
  type CryptoKey,
} from 'jose';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import {
  configureJwtAuth,
  createApp,
  createJwtVerifier,
  normalizePem,
  registerAuth,
} from '@perfumespayday/shared';

const ISSUER = 'perfumespayday-security';
const AUDIENCE = 'perfumespayday-api';
const SUBJECT = '11111111-1111-4111-8111-111111111111';

interface TokenOptions {
  subject?: string;
  issuer?: string;
  audience?: string;
  roles?: string[];
  issuedAt?: number;
  expiresAt?: number;
  key?: CryptoKey;
}

let privateKey: CryptoKey;
let publicKey: CryptoKey;
let otherPrivateKey: CryptoKey;
let publicKeyPem: string;
let app: FastifyInstance;

async function signToken(options: TokenOptions = {}): Promise<string> {
  const issuedAt = options.issuedAt ?? Math.floor(Date.now() / 1000);

  return new SignJWT({ roles: options.roles ?? ['customer'] })
    .setProtectedHeader({ alg: 'RS256' })
    .setSubject(options.subject ?? SUBJECT)
    .setIssuer(options.issuer ?? ISSUER)
    .setAudience(options.audience ?? AUDIENCE)
    .setIssuedAt(issuedAt)
    .setExpirationTime(options.expiresAt ?? issuedAt + 900)
    .setJti('22222222-2222-4222-8222-222222222222')
    .sign(options.key ?? privateKey);
}

function bearer(token: string): Record<string, string> {
  return { authorization: `Bearer ${token}` };
}

beforeAll(async () => {
  const pair = await generateKeyPair('RS256');
  privateKey = pair.privateKey;
  publicKey = pair.publicKey;
  publicKeyPem = await exportSPKI(pair.publicKey);
  otherPrivateKey = (await generateKeyPair('RS256')).privateKey;

  app = await createApp({ name: 'auth-test', logLevel: 'silent' });
  await registerAuth(app, {
    publicKey: publicKeyPem,
    issuer: ISSUER,
    audience: AUDIENCE,
  });

  app.get('/public', async () => ({ ok: true }));
  app.get('/private', { preHandler: app.authenticate }, async (request) => ({
    sub: request.auth?.sub,
  }));
  app.get(
    '/admin',
    { preHandler: [app.authenticate, app.requireRole('admin')] },
    async () => ({ ok: true }),
  );
});

afterAll(async () => {
  await app.close();
});

describe('registro de autenticación', () => {
  it('deja pasar rutas públicas sin token', async () => {
    const response = await app.inject({ method: 'GET', url: '/public' });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ ok: true });
  });

  it('adjunta los claims validados a la petición', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken()),
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ sub: SUBJECT });
  });

  it('rechaza una petición sin cabecera Authorization', async () => {
    const response = await app.inject({ method: 'GET', url: '/private' });

    expect(response.statusCode).toBe(401);
    expect(response.json()).toMatchObject({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Se requiere un token de acceso.',
        requestId: expect.any(String),
      },
    });
  });

  it.each(['Token abc', 'Bearer', 'Bearer uno dos', 'Bearer   '])(
    'rechaza la cabecera mal formada %s',
    async (authorization) => {
      const response = await app.inject({
        method: 'GET',
        url: '/private',
        headers: { authorization },
      });

      expect(response.statusCode).toBe(401);
      expect(response.json()).toMatchObject({
        error: { code: 'UNAUTHORIZED' },
      });
    },
  );
});

describe('validación del token', () => {
  it('rechaza un token expirado', async () => {
    const now = Math.floor(Date.now() / 1000);
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken({ issuedAt: now - 120, expiresAt: now - 60 })),
    });

    expect(response.statusCode).toBe(401);
    expect(response.json()).toMatchObject({
      error: { code: 'UNAUTHORIZED' },
    });
  });

  it('rechaza un token firmado con otra clave', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken({ key: otherPrivateKey })),
    });

    expect(response.statusCode).toBe(401);
  });

  it('rechaza un token con algoritmo HS256', async () => {
    const now = Math.floor(Date.now() / 1000);
    const token = await new SignJWT({ roles: ['customer'] })
      .setProtectedHeader({ alg: 'HS256' })
      .setSubject(SUBJECT)
      .setIssuer(ISSUER)
      .setAudience(AUDIENCE)
      .setIssuedAt(now)
      .setExpirationTime(now + 900)
      .sign(new TextEncoder().encode('una-clave-simetrica-suficientemente-larga'));

    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(token),
    });

    expect(response.statusCode).toBe(401);
  });

  it('rechaza un token sin firma (alg none)', async () => {
    const now = Math.floor(Date.now() / 1000);
    const token = new UnsecuredJWT({ roles: ['admin'] })
      .setSubject(SUBJECT)
      .setIssuer(ISSUER)
      .setAudience(AUDIENCE)
      .setIssuedAt(now)
      .setExpirationTime(now + 900)
      .encode();

    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(token),
    });

    expect(response.statusCode).toBe(401);
  });

  it('rechaza un emisor distinto', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken({ issuer: 'otro-emisor' })),
    });

    expect(response.statusCode).toBe(401);
  });

  it('rechaza una audiencia distinta', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken({ audience: 'otra-api' })),
    });

    expect(response.statusCode).toBe(401);
  });

  it('rechaza claims obligatorios inválidos', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken({ subject: 'no-es-un-uuid' })),
    });

    expect(response.statusCode).toBe(401);
  });
});

describe('autorización por rol', () => {
  it('permite el acceso a un administrador', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/admin',
      headers: bearer(await signToken({ roles: ['admin'] })),
    });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ ok: true });
  });

  it('deniega el acceso a un cliente con 403', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/admin',
      headers: bearer(await signToken({ roles: ['customer'] })),
    });

    expect(response.statusCode).toBe(403);
    expect(response.json()).toMatchObject({
      error: {
        code: 'FORBIDDEN',
        requestId: expect.any(String),
      },
    });
  });

  it('deniega el acceso si el token no trae roles', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/admin',
      headers: bearer(await signToken({ roles: [] })),
    });

    expect(response.statusCode).toBe(403);
  });
});

describe('formatos de clave pública', () => {
  it('acepta un PEM con saltos de línea escapados', async () => {
    const verifier = await createJwtVerifier({
      publicKey: publicKeyPem.replace(/\n/g, '\\n'),
      issuer: ISSUER,
      audience: AUDIENCE,
    });

    await expect(verifier.verify(await signToken())).resolves.toMatchObject({
      sub: SUBJECT,
      roles: ['customer'],
    });
  });

  it('acepta un PEM codificado en base64', async () => {
    const verifier = await createJwtVerifier({
      publicKey: Buffer.from(publicKeyPem, 'utf8').toString('base64'),
      issuer: ISSUER,
      audience: AUDIENCE,
    });

    await expect(verifier.verify(await signToken())).resolves.toMatchObject({
      sub: SUBJECT,
    });
  });

  it('valida con un JWKS remoto', async () => {
    const jwksApp = await createApp({ name: 'jwks-test', logLevel: 'silent' });
    const jwk = await exportJWK(publicKey);

    jwksApp.get('/.well-known/jwks.json', async () => ({
      keys: [{ ...jwk, kid: 'clave-de-prueba', alg: 'RS256', use: 'sig' }],
    }));

    await jwksApp.listen({ port: 0, host: '127.0.0.1' });
    const address = jwksApp.server.address();

    if (!address || typeof address === 'string') {
      throw new Error('No se pudo obtener el puerto del JWKS de prueba.');
    }

    try {
      const verifier = await createJwtVerifier({
        jwksUrl: `http://127.0.0.1:${address.port}/.well-known/jwks.json`,
        issuer: ISSUER,
        audience: AUDIENCE,
      });

      const now = Math.floor(Date.now() / 1000);
      const token = await new SignJWT({ roles: ['customer'] })
        .setProtectedHeader({ alg: 'RS256', kid: 'clave-de-prueba' })
        .setSubject(SUBJECT)
        .setIssuer(ISSUER)
        .setAudience(AUDIENCE)
        .setIssuedAt(now)
        .setExpirationTime(now + 900)
        .sign(privateKey);

      await expect(verifier.verify(token)).resolves.toMatchObject({
        sub: SUBJECT,
      });
    } finally {
      await jwksApp.close();
    }
  });

  it('exige una fuente de clave', async () => {
    await expect(
      createJwtVerifier({ issuer: ISSUER, audience: AUDIENCE }),
    ).rejects.toThrow('Falta JWT_PUBLIC_KEY o JWT_JWKS_URL');
  });

  it('rechaza configurar PEM y JWKS a la vez', async () => {
    await expect(
      createJwtVerifier({
        publicKey: publicKeyPem,
        jwksUrl: 'http://localhost:8000/.well-known/jwks.json',
        issuer: ISSUER,
        audience: AUDIENCE,
      }),
    ).rejects.toThrow('no ambos');
  });

  it('rechaza un PEM inválido', () => {
    expect(() => normalizePem('no-es-una-clave')).toThrow('no es un PEM válido');
  });
});

describe('configuración desde el entorno', () => {
  it('en desarrollo registra guards que fallan cerrados sin clave', async () => {
    const devApp = await createApp({ name: 'auth-env-dev', logLevel: 'silent' });

    await configureJwtAuth(devApp, {
      NODE_ENV: 'development',
      JWT_ISSUER: ISSUER,
      JWT_AUDIENCE: AUDIENCE,
    });

    expect(devApp.hasDecorator('authenticate')).toBe(true);
    expect(devApp.hasDecorator('requireRole')).toBe(true);

    devApp.get('/private', { preHandler: devApp.authenticate }, async () => ({
      ok: true,
    }));

    const response = await devApp.inject({
      method: 'GET',
      url: '/private',
      headers: bearer(await signToken()),
    });

    expect(response.statusCode).toBe(401);
    expect(response.json()).toMatchObject({
      error: { code: 'UNAUTHORIZED' },
    });

    await devApp.close();
  });

  it('en producción exige una fuente de clave', async () => {
    const prodApp = await createApp({ name: 'auth-env-prod', logLevel: 'silent' });

    await expect(
      configureJwtAuth(prodApp, {
        NODE_ENV: 'production',
        JWT_ISSUER: ISSUER,
        JWT_AUDIENCE: AUDIENCE,
      }),
    ).rejects.toThrow('obligatorio en producción');

    await prodApp.close();
  });

  it('registra los guards cuando hay clave pública', async () => {
    const configuredApp = await createApp({
      name: 'auth-env-key',
      logLevel: 'silent',
    });

    await configureJwtAuth(configuredApp, {
      NODE_ENV: 'development',
      JWT_PUBLIC_KEY: publicKeyPem,
      JWT_ISSUER: ISSUER,
      JWT_AUDIENCE: AUDIENCE,
    });

    expect(configuredApp.hasDecorator('authenticate')).toBe(true);
    expect(configuredApp.hasDecorator('requireRole')).toBe(true);
    await configuredApp.close();
  });
});
