// Runs the guard as a real hook process (stdin JSON) over synthetic cases and the transcript corpus.
'use strict';
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process'), crypto = require('crypto');
const dir = __dirname;
const guard = path.join(dir, 'inline-script-guard.cjs');
const corpusPath = process.argv[2];
const POS_IDS = new Set([102, 176, 244, 361]);
const NEUTRAL_IDS = new Set([144, 282]);
const BROAD = (c) => /(<<|python3? -c|node -e|printf|echo )/.test(c) && /(\\|\$\{)/.test(c);

function runHook(input) {
  const t = process.hrtime.bigint();
  const r = spawnSync(process.execPath, [guard], { input, encoding: 'utf8' });
  const ms = Number(process.hrtime.bigint() - t) / 1e6;
  let reasons = [];
  if (r.stdout) { try { reasons = JSON.parse(r.stdout)._reasons || ['?']; } catch { reasons = ['BAD-JSON-OUTPUT']; } }
  return { code: r.status, out: r.stdout, err: r.stderr, ms, reasons };
}
const hookInput = (command, tool = 'Bash') => JSON.stringify({ session_id: 'test', hook_event_name: 'PreToolUse', tool_name: tool, tool_input: { command } });
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);

const times = [];
let fails = 0;
console.log('== Synthetic cases');
const caseDir = path.join(dir, 'cases');
for (const f of fs.readdirSync(caseDir).sort()) {
  const cmd = fs.readFileSync(path.join(caseDir, f), 'utf8');
  // Ground truth = behaviour when sent through the Bash tool (layer-sim run2 + real-tool spot check):
  // broken: all pos*, neg01, neg09, edge03; silently altered output: neg02, edge02. adv01 works.
  const BROKEN_VIA_TOOL = ['neg01', 'neg09', 'edge03', 'neg02', 'edge02'];
  const expectWarn = process.env.INLINE_GUARD_NO_TOOL_LAYER
    ? f.startsWith('pos')
    : f.startsWith('pos') || BROKEN_VIA_TOOL.some((p) => f.startsWith(p));
  const r = runHook(hookInput(cmd)); times.push(r.ms);
  const warned = r.reasons.length > 0;
  const ok = warned === expectWarn && r.code === 0;
  if (!ok) fails++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${f.padEnd(40)} warn=${warned} broad=${BROAD(cmd)} ${r.reasons.join(',')} [${sha(cmd)}]`);
}
console.log('== Robustness');
for (const [name, input, expectWarn] of [
  ['malformed JSON', '{not json', false], ['empty stdin', '', false],
  ['non-Bash tool', hookInput('python -c "print(\'\\\\\')"', 'Write'), false],
  ['missing command', JSON.stringify({ tool_name: 'Bash', tool_input: {} }), false],
  ['200KB command', hookInput('echo "' + 'x'.repeat(200000) + '"'), false],
  ['unterminated quote', hookInput('node -e "console.log(`${a}`'), true],
]) {
  const r = runHook(input); times.push(r.ms);
  const ok = r.code === 0 && (r.reasons.length > 0) === expectWarn && !r.err;
  if (!ok) fails++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name.padEnd(20)} code=${r.code} warn=${r.reasons.length > 0} ${r.err ? 'STDERR:' + r.err.slice(0, 80) : ''} ${r.ms.toFixed(0)}ms`);
}

if (corpusPath) {
  console.log('== Transcript corpus');
  const rows = fs.readFileSync(corpusPath, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
  let tp = 0, fn = 0, fpC = 0, fpB = 0, neg = 0, longOnly = 0;
  const fpList = [];
  for (const r of rows) {
    if (NEUTRAL_IDS.has(r.id)) continue;
    const h = runHook(hookInput(r.command)); times.push(h.ms);
    const w = h.reasons.length > 0;
    if (POS_IDS.has(r.id)) { w ? tp++ : fn++; console.log(`  positive id ${r.id}: warn=${w} broad=${BROAD(r.command)} ${h.reasons.join(',')}`); continue; }
    neg++;
    if (BROAD(r.command)) fpB++;
    if (w) { fpC++; if (h.reasons.every((x) => x === 'long-inline-script')) longOnly++; fpList.push(`  FP id ${r.id} err=${r.is_error} ${h.reasons.join(',')} :: ${r.command.slice(0, 140).replace(/\n/g, ' | ')}`); }
  }
  console.log(fpList.join('\n'));
  console.log(`corpus: ${rows.length} rows, sha ${sha(fs.readFileSync(corpusPath, 'utf8'))}`);
  console.log(`recall (candidate): ${tp}/${tp + fn}   recall (broad): ${[...POS_IDS].filter((id) => BROAD((rows.find((x) => x.id === id) || {}).command || '')).length}/${POS_IDS.size}`);
  console.log(`warnings on non-failing calls: candidate ${fpC}/${neg} (${(100 * fpC / neg).toFixed(1)}%, ${longOnly} long-only)   broad ${fpB}/${neg} (${(100 * fpB / neg).toFixed(1)}%)`);
}
times.sort((a, b) => a - b);
const p = (q) => times[Math.min(times.length - 1, Math.floor(q * times.length))].toFixed(0);
console.log(`timing over ${times.length} hook runs: p50 ${p(0.5)}ms  p95 ${p(0.95)}ms  max ${p(0.999)}ms`);
console.log(`synthetic/robustness failures: ${fails}`);
