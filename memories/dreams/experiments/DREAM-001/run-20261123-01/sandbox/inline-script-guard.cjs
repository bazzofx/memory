#!/usr/bin/env node
// DREAM-001 candidate (sandbox prototype). PreToolUse hook for Bash.
// Statically inspects tool_input.command for inline code that Bash (or an earlier
// escaping layer) is likely to have mangled. NEVER executes the command text.
// Fails open: any error, non-Bash tool, or no finding => no output, exit 0.
'use strict';

const INTERP = '(?:python3?|py|node|deno|ruby|perl)(?:\\.exe)?';
const RE_STDIN_INTERP = new RegExp('(?:^|[\\s/])' + INTERP + '(?:\\s+-\\S*)*$');
const RE_ARG_INTERP = new RegExp('(?:^|[\\s/])' + INTERP + '(?:\\s+-\\S+)*\\s+-[cep]$');
const CODE_EXT = '(?:json|jsonl|js|cjs|mjs|ts|py)';
const RE_CODE_FILE = new RegExp('(?:>{1,2}|\\btee\\s+(?:-a\\s+)?)\\s*["\']?[^\\s"\';|&]+\\.' + CODE_EXT + '\\b');
const RE_JSON_FILE = /(?:>{1,2}|\btee\s+(?:-a\s+)?)\s*["']?[^\s"';|&]+\.jsonl?\b/;
const RE_PIPE_INTERP = new RegExp('\\|\\s*' + INTERP + '\\b');
const LONG_LINES = 25;

function scan(cmd) {
  const items = [];
  const n = cmd.length;
  let i = 0, segStart = 0;
  const pending = [];
  const lineEnd = (k) => { const e = cmd.indexOf('\n', k); return e < 0 ? n : e; };
  while (i < n) {
    const ch = cmd[i];
    if (ch === '\\') { i += 2; continue; }
    if (ch === "'") {
      const j = cmd.indexOf("'", i + 1); const end = j < 0 ? n : j;
      items.push({ kind: 'sq', text: cmd.slice(i + 1, end), prefix: cmd.slice(segStart, i), rest: cmd.slice(end + 1, lineEnd(end + 1)) });
      i = end + 1; continue;
    }
    if (ch === '"') {
      let j = i + 1;
      while (j < n && cmd[j] !== '"') { if (cmd[j] === '\\') j++; j++; }
      const end = Math.min(j, n);
      items.push({ kind: 'dq', text: cmd.slice(i + 1, end), prefix: cmd.slice(segStart, i), rest: cmd.slice(end + 1, lineEnd(end + 1)) });
      i = end + 1; continue;
    }
    if (ch === '<' && cmd[i + 1] === '<') {
      if (cmd[i + 2] === '<') { i += 3; continue; } // here-string
      let k = i + 2, dash = false;
      if (cmd[k] === '-') { dash = true; k++; }
      while (cmd[k] === ' ' || cmd[k] === '\t') k++;
      let w = '', quoted = false;
      while (k < n && !/[\s;|&<>()]/.test(cmd[k])) {
        const c = cmd[k];
        if (c === "'" || c === '"') {
          quoted = true; const e = cmd.indexOf(c, k + 1);
          if (e < 0) { k = n; break; }
          w += cmd.slice(k + 1, e); k = e + 1; continue;
        }
        if (c === '\\') { quoted = true; w += cmd[k + 1] || ''; k += 2; continue; }
        w += c; k++;
      }
      if (w) pending.push({ delim: w, quoted, dash, prefix: cmd.slice(segStart, i), rest: cmd.slice(k, lineEnd(k)) });
      i = k; continue;
    }
    if (ch === '\n') {
      i++;
      for (const h of pending) {
        const lines = [];
        while (i < n) {
          const e = lineEnd(i); const line = cmd.slice(i, e); i = e + 1;
          const cmp = (h.dash ? line.replace(/^\t+/, '') : line).replace(/\r$/, '');
          if (cmp === h.delim) break;
          lines.push(line);
        }
        items.push({ kind: h.quoted ? 'hq' : 'hu', text: lines.join('\n'), prefix: h.prefix, rest: h.rest });
      }
      pending.length = 0; segStart = i; continue;
    }
    if (ch === ';' || ch === '|' || ch === '&' || ch === '(') { segStart = i + 1; i++; continue; }
    i++;
  }
  return items;
}

// What the program finally receives after Bash's own backslash processing (no expansion).
function finalText(it) {
  if (it.kind === 'dq') return it.text.replace(/\\\n/g, '').replace(/\\([\\$"`])/g, '$1');
  if (it.kind === 'hu') return it.text.replace(/\\\n/g, '').replace(/\\([\\$`])/g, '$1');
  return it.text;
}

function hasSubstitution(raw) {
  for (let i = 0; i < raw.length; i++) {
    const c = raw[i];
    if (c === '\\') { i++; continue; }
    if (c === '`') return true;
    if (c === '$' && (raw[i + 1] === '{' || raw[i + 1] === '(')) return true;
  }
  return false;
}
const hasBackslashCollapse = (it) => /\\\\/.test(it.text) || (it.kind === 'hu' && /\\[$`]/.test(it.text));

function invalidJsonEscape(s) {
  let inStr = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (!inStr) { if (c === '"') inStr = true; continue; }
    if (c === '"') { inStr = false; continue; }
    if (c === '\\') {
      const nx = s[i + 1];
      if (!nx || !'"\\/bfnrtu'.includes(nx)) return true;
      i++;
    }
  }
  return false;
}
const RE_LONE_BACKSLASH = /(['"])\\\1(?!\1)/;

// Observed on Claude Code 2.1.329 / Windows Git Bash: before bash runs, a run of N backslashes
// becomes ceil(N/2) unless the next char is '"'. This applies even inside single quotes and
// quoted heredocs. Set INLINE_GUARD_NO_TOOL_LAYER=1 on hosts without it.
const TOOL_LAYER = !process.env.INLINE_GUARD_NO_TOOL_LAYER;
const toolLayer = (s) => s.replace(/\\+/g, (m, off, str) => (str[off + m.length] === '"' ? m : '\\'.repeat(Math.ceil(m.length / 2))));

function codeBound(it) {
  const prefix = it.prefix.trim();
  it = { ...it, rest: it.rest.split(/;|&&|\|\|/)[0] }; // only this command's own redirects/pipes
  const isHeredoc = it.kind === 'hq' || it.kind === 'hu';
  const toInterp = isHeredoc ? RE_STDIN_INTERP.test(prefix) || RE_PIPE_INTERP.test(it.rest) : RE_ARG_INTERP.test(prefix);
  const isEcho = !isHeredoc && /^(?:echo|printf)\b/.test(prefix);
  const ctx = prefix + ' ' + it.rest;
  const toCodeFile = (isHeredoc || isEcho) && RE_CODE_FILE.test(ctx);
  const toJson = (isHeredoc || isEcho) && RE_JSON_FILE.test(ctx);
  return { bound: toInterp || toCodeFile || (isEcho && RE_PIPE_INTERP.test(it.rest)), toInterp, toJson };
}

function analyze(cmd) {
  const reasons = new Set();
  if (TOOL_LAYER) {
    for (const it of scan(cmd)) if (codeBound(it).bound && /\\\\(?!")/.test(it.text)) reasons.add('tool-collapse');
    cmd = toolLayer(cmd);
  }
  for (const it of scan(cmd)) {
    const { bound, toInterp, toJson } = codeBound(it);
    if (!bound) continue;
    const expands = it.kind === 'dq' || it.kind === 'hu';
    if (expands && hasSubstitution(it.text)) reasons.add('substitution');
    if (expands && hasBackslashCollapse(it)) reasons.add('backslash-collapse');
    const fin = finalText(it);
    if (!toJson && RE_LONE_BACKSLASH.test(fin)) reasons.add('lone-backslash-literal');
    if (toJson && invalidJsonEscape(fin)) reasons.add('invalid-json-escape');
    // Long-script rule was measured in revision 1 and dropped as a warning: line count didn't
    // separate failures (27, 41 lines) from successes (28-128 lines). Reported only as info.
    if (process.env.INLINE_GUARD_LONG && toInterp && fin.split('\n').length > LONG_LINES) reasons.add('long-inline-script');
  }
  return [...reasons];
}

const HINT = {
  'tool-collapse': 'the Bash tool on this host turns \\\\ into \\ before bash runs, even inside single quotes and quoted heredocs',
  'substitution': 'Bash will expand ${...}, $(...) or backticks inside a double-quoted/unquoted body',
  'backslash-collapse': 'Bash will turn \\\\ into \\ inside a double-quoted/unquoted body',
  'lone-backslash-literal': "the code contains a '\\' string literal, which is a syntax error (a backslash was lost)",
  'invalid-json-escape': 'the JSON has an invalid backslash escape (e.g. C:\\ai)',
  'long-inline-script': 'inline script is longer than ' + LONG_LINES + ' lines',
};

function main(input) {
  let data;
  try { data = JSON.parse(input); } catch { return ''; }
  if (!data || data.tool_name !== 'Bash') return '';
  const cmd = data.tool_input && data.tool_input.command;
  if (typeof cmd !== 'string' || !cmd) return '';
  const reasons = analyze(cmd);
  if (!reasons.length) return '';
  const msg = 'Inline-script guard (DREAM-001): ' + reasons.map((r) => HINT[r]).join('; ') +
    '. Prefer: Write the script/fixture to a file with the Write tool, then run it by path.';
  return JSON.stringify({ systemMessage: msg, hookSpecificOutput: { hookEventName: 'PreToolUse', additionalContext: msg }, _reasons: reasons });
}

module.exports = { analyze, scan, main };

if (require.main === module) {
  let buf = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (d) => { buf += d; });
  process.stdin.on('end', () => {
    try { const out = main(buf); if (out) process.stdout.write(out); } catch { /* fail open */ }
    process.exit(0);
  });
}
