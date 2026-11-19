import type { FastifyError, FastifyInstance } from 'fastify';
import { ZodError } from 'zod';

/** Detalle de un error de validación, estable para el frontend. */
export interface ErrorDetail {
  field: string;
  code: string;
  message: string;
}

/** Cuerpo uniforme de error definido en ADR-0006. */
export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details: ErrorDetail[] | undefined;
    requestId: string;
  };
}

/** Error de negocio o de transporte que ya conoce su código HTTP. */
export class AppError extends Error {
  readonly code: string;
  readonly statusCode: number;
  readonly details: ErrorDetail[] | undefined;

  constructor(
    code: string,
    message: string,
    statusCode = 400,
    details?: ErrorDetail[],
  ) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
  }
}

export function errorEnvelope(
  code: string,
  message: string,
  requestId: string,
  details?: ErrorDetail[],
): ErrorResponse {
  return { error: { code, message, details, requestId } };
}

interface ValidationIssue {
  instancePath?: string;
  keyword?: string;
  message?: string;
}

function isValidationError(
  error: unknown,
): error is FastifyError & { validation: ValidationIssue[] } {
  return (
    typeof error === 'object' &&
    error !== null &&
    Array.isArray((error as { validation?: unknown }).validation)
  );
}

function zodDetails(error: ZodError): ErrorDetail[] {
  return error.issues.map((issue) => ({
    field: issue.path.join('.') || 'body',
    code: issue.code.toUpperCase(),
    message: issue.message,
  }));
}

function validationDetails(issues: ValidationIssue[]): ErrorDetail[] {
  return issues.map((issue) => ({
    field: (issue.instancePath ?? '').replace(/^\//, '').replace(/\//g, '.') || 'body',
    code: (issue.keyword ?? 'invalid').toUpperCase(),
    message: issue.message ?? 'Valor inválido.',
  }));
}

/**
 * Registra el manejo uniforme de errores y de rutas inexistentes.
 * Se aplica una sola vez por aplicación, desde `createApp`.
 */
export function registerErrorHandler(app: FastifyInstance): void {
  app.setNotFoundHandler((request, reply) => {
    reply
      .status(404)
      .send(errorEnvelope('NOT_FOUND', 'El recurso solicitado no existe.', request.id));
  });

  app.setErrorHandler((error, request, reply) => {
    if (error instanceof AppError) {
      reply
        .status(error.statusCode)
        .send(errorEnvelope(error.code, error.message, request.id, error.details));
      return;
    }

    if (error instanceof ZodError) {
      reply
        .status(400)
        .send(
          errorEnvelope(
            'VALIDATION_ERROR',
            'Los datos enviados no son válidos.',
            request.id,
            zodDetails(error),
          ),
        );
      return;
    }

    if (isValidationError(error)) {
      reply
        .status(400)
        .send(
          errorEnvelope(
            'VALIDATION_ERROR',
            'Los datos enviados no son válidos.',
            request.id,
            validationDetails(error.validation),
          ),
        );
      return;
    }

    request.log.error({ err: error }, 'Error no controlado');
    reply
      .status(500)
      .send(errorEnvelope('INTERNAL_ERROR', 'Ocurrió un error interno.', request.id));
  });
}
