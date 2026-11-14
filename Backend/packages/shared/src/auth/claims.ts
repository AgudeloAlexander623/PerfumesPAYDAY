import { z } from 'zod';

/** Roles reconocidos por el backend. Coinciden con `docs/security.md`. */
export const roleSchema = z.enum(['customer', 'admin']);

export type Role = z.infer<typeof roleSchema>;

const audienceSchema = z.union([
  z.string().min(1),
  z.array(z.string().min(1)).nonempty(),
]);

/**
 * Claims del access token emitido por `security-service`.
 * Se permite cualquier claim adicional, pero solo estos se usan para autorizar.
 */
export const authClaimsSchema = z
  .object({
    sub: z.uuid(),
    iss: z.string().min(1),
    aud: audienceSchema,
    exp: z.number().int().positive(),
    iat: z.number().int().nonnegative(),
    jti: z.string().min(1).optional(),
    roles: z.array(roleSchema).default([]),
  })
  .passthrough();

export type AuthClaims = z.infer<typeof authClaimsSchema>;

/** Indica si el token tiene al menos uno de los roles indicados. */
export function hasRole(claims: AuthClaims, ...roles: Role[]): boolean {
  return roles.some((role) => claims.roles.includes(role));
}
