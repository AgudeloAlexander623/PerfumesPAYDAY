import { describe, expect, it } from 'vitest';
import { AppError, createApp } from '../src/index.js';

describe('createApp', () => {
  it('expone /health con el nombre del servicio', async () => {
    const app = await createApp({ name: 'test', logLevel: 'silent' });

    const response = await app.inject({ method: 'GET', url: '/health' });

    expect(response.statusCode).toBe(200);
    expect(response.json()).toEqual({ status: 'ok', service: 'test' });

    await app.close();
  });

  it('devuelve el envelope de error y conserva el requestId', async () => {
    const app = await createApp({ name: 'test', logLevel: 'silent' });

    const response = await app.inject({
      method: 'GET',
      url: '/no-existe',
      headers: { 'x-request-id': 'req-123' },
    });

    expect(response.statusCode).toBe(404);
    expect(response.json()).toEqual({
      error: {
        code: 'NOT_FOUND',
        message: 'El recurso solicitado no existe.',
        requestId: 'req-123',
      },
    });
    expect(response.headers['x-request-id']).toBe('req-123');

    await app.close();
  });

  it('mapea AppError a su estado y código', async () => {
    const app = await createApp({ name: 'test', logLevel: 'silent' });
    app.get('/sin-dependencia', async () => {
      throw new AppError('DEPENDENCY_UNAVAILABLE', 'Servicio no disponible.', 503);
    });

    const response = await app.inject({ method: 'GET', url: '/sin-dependencia' });

    expect(response.statusCode).toBe(503);
    expect(response.json()).toEqual({
      error: {
        code: 'DEPENDENCY_UNAVAILABLE',
        message: 'Servicio no disponible.',
        requestId: expect.any(String),
      },
    });

    await app.close();
  });

  it('oculta el detalle de un error no controlado', async () => {
    const app = await createApp({ name: 'test', logLevel: 'silent' });
    app.get('/boom', async () => {
      throw new Error('detalle interno que no debe salir');
    });

    const response = await app.inject({ method: 'GET', url: '/boom' });

    expect(response.statusCode).toBe(500);
    expect(response.json()).toEqual({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'Ocurrió un error interno.',
        requestId: expect.any(String),
      },
    });

    await app.close();
  });
});
