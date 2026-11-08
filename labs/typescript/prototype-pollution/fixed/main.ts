declare const process: {argv: string[], stdout: {write(s: string): void}};

function run(raw: string): string {
    let incoming: unknown;
    try { incoming = JSON.parse(raw); }
    catch { return 'DENIED'; }
    if (incoming === null || typeof incoming !== 'object' || Array.isArray(incoming)) {
        return 'DENIED';
    }
    const target: Record<string, unknown> = Object.create(null);
    const blocked = new Set(['__proto__', 'constructor', 'prototype']);
    for (const [key, value] of Object.entries(incoming)) {
        if (!blocked.has(key)) target[key] = value;
    }
    // This marker observes property lookup; it is not an authorization design.
    return target.isAdmin === true ? 'ADMIN' : 'USER';
}
process.stdout.write(run(process.argv[2]));
