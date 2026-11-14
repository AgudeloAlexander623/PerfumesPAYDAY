/** Servicio interno que atiende una ruta del gateway. */
export type UpstreamName = 'security' | 'catalog' | 'orders';

/** Nivel de autenticación exigido antes de proxificar. */
export type AuthRequirement = 'public' | 'authenticated' | 'admin';

export interface GatewayRoute {
  /** Prefijo público que se conserva al reenviar la petición. */
  prefix: string;
  upstream: UpstreamName;
  auth: AuthRequirement;
  /** Métodos permitidos; si se omite, se aceptan todos. */
  methods?: string[];
  /** Aplica el límite estricto de autenticación (login, registro y refresh). */
  authRateLimit?: boolean;
}

/**
 * Rutas del contrato público. Los servicios internos exponen el mismo
 * base path `/api/v1`, por eso el proxy conserva el prefijo.
 */
export const gatewayRoutes: readonly GatewayRoute[] = [
  {
    prefix: '/api/v1/auth',
    upstream: 'security',
    auth: 'public',
    authRateLimit: true,
  },
  {
    prefix: '/api/v1/users',
    upstream: 'security',
    auth: 'authenticated',
  },
  {
    prefix: '/api/v1/products',
    upstream: 'catalog',
    auth: 'public',
    methods: ['GET', 'HEAD'],
  },
  {
    prefix: '/api/v1/brands',
    upstream: 'catalog',
    auth: 'public',
    methods: ['GET', 'HEAD'],
  },
  {
    prefix: '/api/v1/categories',
    upstream: 'catalog',
    auth: 'public',
    methods: ['GET', 'HEAD'],
  },
  {
    prefix: '/api/v1/cart',
    upstream: 'orders',
    auth: 'authenticated',
  },
  {
    prefix: '/api/v1/addresses',
    upstream: 'orders',
    auth: 'authenticated',
  },
  {
    prefix: '/api/v1/orders',
    upstream: 'orders',
    auth: 'authenticated',
  },
  {
    prefix: '/api/v1/admin/products',
    upstream: 'catalog',
    auth: 'admin',
  },
  {
    prefix: '/api/v1/admin/brands',
    upstream: 'catalog',
    auth: 'admin',
  },
  {
    prefix: '/api/v1/admin/categories',
    upstream: 'catalog',
    auth: 'admin',
  },
  {
    prefix: '/api/v1/admin/orders',
    upstream: 'orders',
    auth: 'admin',
  },
  // `/api/v1/admin/audit` se agregará cuando exista la consulta paralela
  // a catalog y orders descrita en CU-23.
];
