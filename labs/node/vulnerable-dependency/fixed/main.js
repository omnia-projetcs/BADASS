const merge = require('lodash.merge');
const settings = merge({ preferences: { theme: 'light' } }, JSON.parse(process.argv[2]));
// Inspect a different object: user settings must never alter its inherited privileges.
process.stdout.write(JSON.stringify({ theme: settings.preferences.theme, isAdmin: ({}).isAdmin === true }));
