function run(value) {
    const fs = require('node:fs');
    fs.writeFileSync('audit.log', 'user=' + value);
    return fs.readFileSync('audit.log', 'utf8');
}
process.stdout.write(run(process.argv[2]));
