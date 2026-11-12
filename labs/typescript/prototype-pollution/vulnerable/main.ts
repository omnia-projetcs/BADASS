declare const process: {argv: string[], stdout: {write(s: string): void}};

function merge(target: any, source: any): any {
    for (const key of Object.keys(source)) {
        const value = source[key];
        if (value !== null && typeof value === "object" && !Array.isArray(value)) {
            if (typeof target[key] !== "object" || target[key] === null) {
                target[key] = {};
            }
            merge(target[key], value);
        } else {
            target[key] = value;
        }
    }
    return target;
}

const incoming = JSON.parse(process.argv[2]);
const target: any = merge({}, incoming);
process.stdout.write(target.isAdmin === true ? "ADMIN" : "USER");
