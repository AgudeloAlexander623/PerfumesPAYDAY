import { ZodError } from 'zod';
/** Error de negocio o de transporte que ya conoce su código HTTP. */
export class AppError extends Error {
    code;
    statusCode;
    details;
    constructor(code, message, statusCode = 400, details) {
        super(message);
        this.name = 'AppError';
        this.code = code;
        this.statusCode = statusCode;
        this.details = details;
    }
}
export function errorEnvelope(code, message, requestId, details) {
    return { error: { code, message, details, requestId } };
}
function isValidationError(error) {
    return (typeof error === 'object' &&
        error !== null &&
        Array.isArray(error.validation));
}
function zodDetails(error) {
    return error.issues.map((issue) => ({
        field: issue.path.join('.') || 'body',
        code: issue.code.toUpperCase(),
        message: issue.message,
    }));
}
function validationDetails(issues) {
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
export function registerErrorHandler(app) {
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
                .send(errorEnvelope('VALIDATION_ERROR', 'Los datos enviados no son válidos.', request.id, zodDetails(error)));
            return;
        }
        if (isValidationError(error)) {
            reply
                .status(400)
                .send(errorEnvelope('VALIDATION_ERROR', 'Los datos enviados no son válidos.', request.id, validationDetails(error.validation)));
            return;
        }
        request.log.error({ err: error }, 'Error no controlado');
        reply
            .status(500)
            .send(errorEnvelope('INTERNAL_ERROR', 'Ocurrió un error interno.', request.id));
    });
}
//# sourceMappingURL=errors.js.map