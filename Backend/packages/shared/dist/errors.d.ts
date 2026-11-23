import type { FastifyInstance } from 'fastify';
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
export declare class AppError extends Error {
    readonly code: string;
    readonly statusCode: number;
    readonly details: ErrorDetail[] | undefined;
    constructor(code: string, message: string, statusCode?: number, details?: ErrorDetail[]);
}
export declare function errorEnvelope(code: string, message: string, requestId: string, details?: ErrorDetail[]): ErrorResponse;
/**
 * Registra el manejo uniforme de errores y de rutas inexistentes.
 * Se aplica una sola vez por aplicación, desde `createApp`.
 */
export declare function registerErrorHandler(app: FastifyInstance): void;
//# sourceMappingURL=errors.d.ts.map