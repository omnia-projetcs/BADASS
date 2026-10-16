const incoming = JSON.parse(process.argv[2]);
const target = {};
Object.assign(target, incoming);
process.stdout.write(target.isAdmin === true ? 'ADMIN' : 'USER');