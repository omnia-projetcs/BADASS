// Run after npm ci in each dependency fixture; no network is used by this check.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { createRequire } = require('node:module');
const root = path.resolve(__dirname, '../..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog/cases.json'), 'utf8'));
const ids = ['node/vulnerable-dependency', 'node/vulnerable-transitive-dependency'];
let checked = 0;
for (const id of ids) {
  const entry = catalog.find(c => c.id === id);
  assert.ok(entry, `Missing catalog case: ${id}`);
  assert.equal(fs.readFileSync(path.join(root, entry.vulnerable), 'utf8'),
    fs.readFileSync(path.join(root, entry.fixed), 'utf8'), 'Only the dependency should change');
  for (const variant of ['vulnerable', 'fixed']) {
    const source = path.join(root, entry[variant]);
    const directory = path.dirname(source);
    const localRequire = createRequire(source);
    const libraryRequire = entry.dependency.relationship === 'transitive'
      ? createRequire(localRequire.resolve('badass-settings-fixture')) : localRequire;
    const packagePath = libraryRequire.resolve('lodash.merge/package.json');
    assert.ok(fs.realpathSync(packagePath).startsWith(directory + path.sep + 'node_modules' + path.sep),
      'The fixture must use its own installed dependency, not a global fallback');
    const installed = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    const lock = JSON.parse(fs.readFileSync(path.join(directory, 'package-lock.json'), 'utf8'));
    assert.equal(installed.version, entry.dependency[variant + '_version']);
    assert.equal(lock.packages['node_modules/lodash.merge'].version, installed.version);
    for (const vector of entry.tests) {
      // Each vector gets a fresh process, so polluted prototypes cannot leak between tests.
      const result = spawnSync(process.execPath, [path.join(root, entry[variant]), vector.input],
        { encoding: 'utf8', timeout: 5000, cwd: root });
      assert.ifError(result.error);
      assert.equal(result.status, 0, `${id}/${variant}: ${result.stderr}`);
      assert.equal(result.stdout, vector[variant].equals, `${id}/${variant}: ${vector.name}`);
      checked++;
    }
  }
}
console.log(`PASS: ${ids.length} dependency cases, ${checked} variant/vector checks`);
