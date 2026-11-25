// Simulate the observed Bash-tool backslash layer (Claude Code 2.1.329, Windows/Git Bash),
// then run each case under bash in ./run2 to get "as sent through the Bash tool" ground truth.
'use strict';
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process');
const toolLayer = (s) => s.replace(/\\+/g, (m, off, str) => (str[off + m.length] === '"' ? m : '\\'.repeat(Math.ceil(m.length / 2))));
module.exports = { toolLayer };
if (require.main === module) {
  const dir = __dirname, cases = path.join(dir, 'cases'), run = path.join(dir, 'run2');
  fs.mkdirSync(run, { recursive: true });
  for (const f of fs.readdirSync(cases).sort()) {
    const raw = fs.readFileSync(path.join(cases, f), 'utf8');
    const eff = toolLayer(raw);
    fs.writeFileSync(path.join(run, f), eff);
    const r = spawnSync('bash', [f], { cwd: run, encoding: 'utf8' });
    const out = (r.stdout + r.stderr).replace(/\s+/g, ' ').slice(0, 90);
    console.log(`${f.padEnd(38)} changed=${raw !== eff ? 'Y' : 'n'} rc=${r.status} | ${out}`);
  }
}
