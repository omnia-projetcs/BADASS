'use strict';
// Unescaped regex dots allow unrelated origins to receive credentialed data.
const fs = require('node:fs');

function response(origin, privateData = 'LAB_PRIVATE_PROFILE') {
    if (typeof origin !== 'string' || origin.length < 1 || origin.length > 128
        || /[^\x21-\x7e]/.test(origin)) return {status: 400};
    // The dots are wildcards, not literal DNS label separators.
    if (!/^https:\/\/[a-z]+.example.test$/.test(origin)) return {status: 403};
    return {status: 200, headers: {'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Credentials': 'true'}, body: privateData};
}

function run(origin) {
    const result = response(origin);
    if (result.status === 200) fs.writeFileSync('cors-response.json', JSON.stringify(result) + '\n');
    return result;
}

module.exports = {run, response};
if (require.main === module) {
    let request;
    try { request = JSON.parse(process.argv[2]); }
    catch { process.stdout.write(JSON.stringify({status: 400})); process.exit(0); }
    process.stdout.write(JSON.stringify(run(request)));
}
