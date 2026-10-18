'use strict';
// A caller-controlled tag length truncates the expected HMAC comparison.
const crypto = require('node:crypto');
const fs = require('node:fs');

function sign(body, key) {
    return crypto.createHmac('sha256', key).update(body).digest('hex');
}

function verify(body, tag, key) {
    if (typeof tag !== 'string' || tag.length > 64 || /[^0-9a-f]/.test(tag)) return false;
    const expected = sign(body, key);
    // Constant-time comparison does not repair an attacker-selected length.
    return crypto.timingSafeEqual(Buffer.from(expected.slice(0, tag.length)), Buffer.from(tag));
}

function run(request) {
    if (!request || typeof request !== 'object' || Array.isArray(request)
        || typeof request.body !== 'string') return {status: 400};
    const mode = request.signature;
    if (!['valid', 'prefix', 'empty', 'wrong', 'malformed'].includes(mode)) return {status: 400};
    const body = Buffer.from(request.body, 'utf8');
    if (body.length > 256 || body.toString('utf8') !== request.body) return {status: 400};
    // Selectors are local scenario controls, not an exposed signing endpoint.
    const key = crypto.randomBytes(32);
    let tag = sign(body, key);
    if (mode === 'prefix') tag = tag.slice(0, 2);
    else if (mode === 'empty') tag = '';
    else if (mode === 'wrong') tag = (tag[0] === '0' ? '1' : '0') + tag.slice(1);
    else if (mode === 'malformed') tag = 'not-a-tag';
    if (!verify(body, tag, key)) return {status: 401};
    fs.writeFileSync('verified-message.txt', body);
    return {status: 201, bytes: body.length};
}

module.exports = {run, verify, sign};
if (require.main === module) {
    let request;
    try { request = JSON.parse(process.argv[2]); }
    catch { process.stdout.write(JSON.stringify({status: 400})); process.exit(0); }
    process.stdout.write(JSON.stringify(run(request)));
}
