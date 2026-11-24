import { createJwtVerifier } from '../../packages/shared/src/auth/verify.js';
import { AppError } from '../../packages/shared/src/errors.js';

/**
 * Puente de prueba: valida con el verificador Node un token emitido por Python.
 * Imprime un único JSON en stdout para que el test pytest pueda compararlo.
 */
async function main(): Promise<void> {
  const [token, jwksUrl, issuer, audience] = process.argv.slice(2);

  if (!token || !jwksUrl || !issuer || !audience) {
    throw new Error(
      'Uso: verify_jwt.ts <token> <jwksUrl> <issuer> <audience>',
    );
  }

  try {
    const verifier = await createJwtVerifier({ jwksUrl, issuer, audience });
    const claims = await verifier.verify(token);
    process.stdout.write(JSON.stringify({ ok: true, claims }));
  } catch (error) {
    // Solo se traducen los errores conocidos; cualquier otro fallo debe romper
    // el test en lugar de disfrazarse de 401.
    const appError =
      error instanceof AppError
        ? error
        : new AppError('VERIFICATION_FAILED', 'Unexpected failure.', 500);

    process.stdout.write(
      JSON.stringify({
        ok: false,
        error: { code: appError.code, statusCode: appError.statusCode },
      }),
    );
    process.exitCode = 2;
  }
}

await main();
