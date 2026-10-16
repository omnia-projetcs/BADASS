const fs = require('node:fs');
process.stdout.write(process.argv[2] === 'welcome.txt' ? fs.readFileSync('public/welcome.txt', 'utf8') : 'DENIED');