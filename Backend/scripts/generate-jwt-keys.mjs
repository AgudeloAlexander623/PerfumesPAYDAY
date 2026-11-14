#!/usr/bin/env node

import { exportPKCS8, exportSPKI, generateKeyPair } from 'jose';

const { publicKey, privateKey } = await generateKeyPair('RS256', {
  extractable: true,
});

const toBase64 = (pem) => Buffer.from(pem, 'utf8').toString('base64');

const publicPem = await exportSPKI(publicKey);
const privatePem = await exportPKCS8(privateKey);

console.log('# Par de claves RS256 para desarrollo. No lo uses en producción.');
console.log('# Pega JWT_PUBLIC_KEY en Backend/.env y entrega JWT_PRIVATE_KEY a security-service.');
console.log(`JWT_PUBLIC_KEY=${toBase64(publicPem)}`);
console.log(`JWT_PRIVATE_KEY=${toBase64(privatePem)}`);
