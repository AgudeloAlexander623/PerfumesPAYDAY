# syntax=docker/dockerfile:1

FROM node:22-alpine AS base
WORKDIR /app
ENV NPM_CONFIG_UPDATE_NOTIFIER=false
COPY package.json package-lock.json ./
COPY tsconfig.base.json tsconfig.json ./
COPY packages/shared/package.json packages/shared/
COPY services/gateway/package.json services/gateway/
COPY services/catalog/package.json services/catalog/
COPY services/orders/package.json services/orders/
RUN npm ci

FROM base AS build
COPY packages packages
COPY services services
RUN npm run build

FROM base AS production-dependencies
RUN npm prune --omit=dev

FROM node:22-alpine AS runtime
ARG SERVICE
ENV NODE_ENV=production
ENV SERVICE=${SERVICE}
WORKDIR /app
COPY --from=production-dependencies /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/packages/shared/package.json ./packages/shared/package.json
COPY --from=build /app/packages/shared/dist ./packages/shared/dist
COPY --from=build /app/services/gateway/package.json ./services/gateway/package.json
COPY --from=build /app/services/catalog/package.json ./services/catalog/package.json
COPY --from=build /app/services/orders/package.json ./services/orders/package.json
COPY --from=build /app/services/${SERVICE}/dist ./services/${SERVICE}/dist
USER node
CMD ["sh", "-c", "exec node services/$SERVICE/dist/server.js"]
