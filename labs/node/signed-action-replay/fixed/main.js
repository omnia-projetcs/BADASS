'use strict';
// Reject reused signed action identifiers before applying a second debit.
const crypto = require('node:crypto');
const fs = require('node:fs');
const NOW = 1000;

function sign(body, key) {
    return crypto.createHmac('sha256', key).update(body).digest('hex');
}

class Processor {
    constructor(key, balance = 1000) {
        this.key = key;
        this.balance = balance;
        this.seen = new Set();
        this.accepted = [];
    }

    process(body, tag, now) {
        if (!Buffer.isBuffer(body) || body.length > 512 || typeof tag !== 'string'
            || tag.length !== 64 || /[^0-9a-f]/.test(tag)
            || !crypto.timingSafeEqual(Buffer.from(sign(body, this.key)), Buffer.from(tag))) return {status: 401};
        let event;
        try { event = JSON.parse(body.toString('utf8')); }
        catch { return {status: 400}; }
        if (!event || typeof event !== 'object' || Array.isArray(event)
            || Object.keys(event).sort().join(',') !== 'amount,expires,id'
            || typeof event.id !== 'string' || event.id.length < 1 || event.id.length > 32 || /[^a-z0-9-]/.test(event.id)
            || !Number.isInteger(event.amount) || event.amount < 1 || event.amount > 500
            || !Number.isInteger(event.expires) || event.expires < NOW || event.expires > 2000) return {status: 400};
        if (event.expires <= now) return {status: 401};
        // Replay state belongs to this synchronous processor instance.
        if (this.seen.has(event.id)) return {status: 409};
        if (event.amount > this.balance) return {status: 402};
        this.seen.add(event.id);
        this.balance -= event.amount;
        this.accepted.push({id: event.id, amount: event.amount});
        return {status: 200};
    }
}

function run(request) {
    // Signed actions and clock values are local scenario controls.
    if (!request || typeof request !== 'object' || !Array.isArray(request.actions)
        || request.actions.length < 1 || request.actions.length > 6) return {status: 400};
    let previous = NOW;
    for (const action of request.actions) {
        if (!action || typeof action !== 'object' || Array.isArray(action)
            || !['valid', 'forged'].includes(action.signature) || !Number.isInteger(action.at)
            || action.at < previous || action.at > 2000) return {status: 400};
        previous = action.at;
    }
    const key = crypto.randomBytes(32);
    const processor = new Processor(key);
    const statuses = [];
    for (const action of request.actions) {
        const body = Buffer.from(JSON.stringify({id: action.id ?? null, amount: action.amount ?? null, expires: NOW + 60}));
        let tag = sign(body, key);
        if (action.signature === 'forged') tag = (tag[0] === '0' ? '1' : '0') + tag.slice(1);
        statuses.push(processor.process(body, tag, action.at).status);
    }
    const state = {balance: processor.balance, accepted: processor.accepted};
    fs.writeFileSync('ledger.json', JSON.stringify(state) + '\n');
    return {statuses, balance: processor.balance};
}

module.exports = {run, Processor, sign};
if (require.main === module) {
    let request;
    try { request = JSON.parse(process.argv[2]); }
    catch { process.stdout.write(JSON.stringify({status: 400})); process.exit(0); }
    process.stdout.write(JSON.stringify(run(request)));
}
