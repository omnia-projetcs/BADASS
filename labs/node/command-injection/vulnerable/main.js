const cp = require('node:child_process');
process.stdout.write(cp.execSync('printf %s ' + process.argv[2], {encoding: 'utf8'}));