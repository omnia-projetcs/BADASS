const fs = require('node:fs');
process.stdout.write(fs.readFileSync('public/' + process.argv[2], 'utf8'));