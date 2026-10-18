const assert = require('node:assert/strict');
const variant = process.argv[2];
assert(['vulnerable', 'fixed'].includes(variant));
const checks = [];
const privateBody = { invoices: [{ id: 'INV-001', customer: 'LAB_PRIVATE_CUSTOMER', amount: 10000 }] };
const vectors = [
  ['public health', 'benign', '/api/health', {}, 200, { status: 'ok' }],
  ['authenticated invoice access', 'benign', '/api/private/invoices', { cookie: `lab-session=${process.env.LAB_SESSION_TOKEN}` }, 200, privateBody],
  ['anonymous access denied', 'robustness', '/api/private/invoices', {}, 401, { error: 'Unauthorized' }],
  ['invalid session denied', 'robustness', '/api/private/invoices', { cookie: 'lab-session=wrong' }, 401, { error: 'Unauthorized' }],
  ['external request impersonates internal middleware recursion', 'attack', '/api/private/invoices',
    { 'x-middleware-subrequest': Array(5).fill('middleware').join(':') },
    variant === 'vulnerable' ? 200 : 401, variant === 'vulnerable' ? privateBody : { error: 'Unauthorized' }],
];
(async () => {
  for (const [name, kind, path, headers, status, body] of vectors) {
    try {
      const response = await fetch(`http://web:8000${path}`, { headers, redirect: 'manual', signal: AbortSignal.timeout(8000) });
      assert.equal(response.status, status);
      assert.deepEqual(await response.json(), body);
      checks.push({ case_id: 'nextjs-middleware/CVE-2025-29927', name, kind, status: 'pass' });
    } catch (error) {
      checks.push({ case_id: 'nextjs-middleware/CVE-2025-29927', name, kind, status: 'fail', error: String(error) });
    }
  }
  console.log('BADASS_RESULT=' + JSON.stringify({ variant, checks }));
  process.exitCode = checks.length && checks.every(c => c.status === 'pass') ? 0 : 1;
})();
