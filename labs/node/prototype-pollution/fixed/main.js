const incoming = JSON.parse(process.argv[2]);
const target = Object.create(null);
for (const key of Object.keys(incoming)) { if (!['__proto__', 'constructor', 'prototype'].includes(key)) target[key] = incoming[key]; }
process.stdout.write(target.isAdmin === true ? 'ADMIN' : 'USER');