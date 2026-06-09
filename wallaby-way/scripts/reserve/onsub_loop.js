export const meta = {
  name: 'onsub-loop',
  description: 'On-sub scope reader: extract one conv from floor, embed payload, read nodes, persist',
  phases: [
    { title: 'Guard1' },
    { title: 'Guard2' },
    { title: 'Extract' },
    { title: 'ReadConv' },
    { title: 'Persist' },
    { title: 'Log' },
  ],
}

// Called via: Workflow({scriptPath: 'pipeline/s39/onsub_loop.js', args: {conv_uuid: '<uuid>'}})

const convUuid = args.conv_uuid
if (!convUuid) throw new Error('args.conv_uuid is required')

// ── Guard 1 ───────────────────────────────────────────────────────────────────
// Bash $var:+word expansion is unreliable here: Explore agents include the word
// in prose explanations, causing false positives with includes(). Fix: Python
// one-liner prints exactly CLEAN or DIRTY — no prose, no ambiguity.
// Python scripts (floor_extract.py, persist_guard.py) also call
// assert_env_unloaded() independently as a second enforcement layer.
phase('Guard1')
const envCheck = await agent(
  'Run this python one-liner and return ONLY the output (no commentary, no extra text):\n' +
  "python -c \"import os,sys; sys.stdout.write('DIRTY' if 'ANTHROPIC_API_KEY' in os.environ else 'CLEAN')\"",
  {agentType: 'Explore', label: 'guard1-billing-check'}
)
if (envCheck && envCheck.trim().startsWith('DIRTY'))
  throw new Error('BILLING GUARD FIRED — ANTHROPIC_API_KEY in env. HALT.')
log('Guard 1 PASS: ' + envCheck.trim())

// ── Guard 2 ───────────────────────────────────────────────────────────────────
phase('Guard2')
const WHALE_UUIDS = new Set([
  'cfc7a70a-16f0-4f09-8467-d40260ee7434',
  '83506215-d78e-4d0c-a4bf-2d67faf5f59c',
  '55217328-5845-4745-bcea-054acf8f39b7',
  'd9d05961-b0e1-47d5-8fbc-1b68e8b32cd9',
])
if (WHALE_UUIDS.has(convUuid))
  throw new Error(`KNOWN_WHALE: ${convUuid} — use Stage C chunker. HALT.`)
log('Guard 2 PASS: not a known whale')

// ── Extract ───────────────────────────────────────────────────────────────────
phase('Extract')
const extractOut = await agent(
  `Run this command and return the full stdout:\n` +
  `python pipeline/s39/floor_extract.py --conv-uuid ${convUuid} ` +
  `--out pipeline/s39/${convUuid}_payload.txt`,
  {agentType: 'Explore', label: 'floor-extract'}
)
log('Extract: ' + extractOut)

// ── ReadConv — PROHIBITION 3 compliant ───────────────────────────────────────
// Three-agent flow: read prompt file → read payload → scope-reader gets embedded text
// (NO file path, NO write instruction) → harness-controlled write of catalog output.
phase('ReadConv')

// d.0 — Read Boot_ScopeReader_v4.0 prompt into JS (avoids backtick-escaping issues)
const BOOT_SCOPE_READER = await agent(
  'Read the file pipeline/test_call_system_prompt_S32.md using the Read tool. ' +
  'Return its COMPLETE contents verbatim — no truncation, no summary, no paraphrasing.',
  {agentType: 'Explore', label: 'read-boot-prompt'}
)
log('Boot prompt loaded: ' + BOOT_SCOPE_READER.length + ' chars')

// d.1 — Read payload via Bash cat (no line limit; Read tool silently truncates at 2000 lines)
const payloadText = await agent(
  `Run this bash command and return the COMPLETE output verbatim (no truncation, no summary):\n` +
  `cat 'pipeline/s39/${convUuid}_payload.txt'`,
  {agentType: 'Explore', label: 'read-payload'}
)
log('Payload: ' + payloadText.length + ' chars')

// d.2 — Scope-reader: receives ONLY embedded text, NO file path, NO write instruction
// Default agent type (no agentType) so Boot_ScopeReader is the sole system context.
const nodeText = await agent(
  BOOT_SCOPE_READER + '\n\n' + payloadText,
  {label: 'scope-reader'}
)
log('Node catalog: ' + nodeText.length + ' chars')

// d.3 — Harness controls the write (PROHIBITION 3: reader never touched a file)
// Single-quoted heredoc delimiter = conv_uuid without dashes, guaranteed unique.
const delim = 'NODECAT_' + convUuid.replace(/-/g, '')
const writeResult = await agent(
  `Write the following text verbatim to file pipeline/s39/${convUuid}_nodes_raw.txt.\n` +
  `Use the Bash tool with this exact heredoc command (single-quoted delimiter prevents\n` +
  `variable expansion; the delimiter is unique and will not appear in catalog text):\n\n` +
  `cat > 'pipeline/s39/${convUuid}_nodes_raw.txt' << '${delim}'\n` +
  nodeText + '\n' + delim + '\n\n' +
  `After the Bash command succeeds, return: WRITTEN: pipeline/s39/${convUuid}_nodes_raw.txt`,
  {label: 'write-output'}
)
log('Write: ' + writeResult)

// ── Persist (Guards 3 + 4) ────────────────────────────────────────────────────
phase('Persist')
const persistOut = await agent(
  `Run this command and return the full stdout and stderr:\n` +
  `python pipeline/s39/persist_guard.py ` +
  `--node-text pipeline/s39/${convUuid}_nodes_raw.txt ` +
  `--parents-json pipeline/s39/${convUuid}_payload.txt.parents.json ` +
  `--conv-uuid ${convUuid} ` +
  `--out harvested_nodes/${convUuid}.md`,
  {agentType: 'Explore', label: 'persist-guard'}
)
log('Persist: ' + persistOut)

// ── Log ───────────────────────────────────────────────────────────────────────
phase('Log')
await agent(
  `Append one row to pipeline/s39/run_log.csv using Bash.\n` +
  `If run_log.csv does not yet exist, write the header line first:\n` +
  `conv_uuid,input_tokens,node_count,M_F_T,stop_reason,persisted_path\n\n` +
  `Parse node_count and M/F/T counts from this persist output: ${persistOut}\n` +
  `The persist output contains a JSON line like: {"node_count":N,"motion":M,"fence":F,"texture":T,...}\n` +
  `Format: conv_uuid = ${convUuid}, input_tokens = proxy (from worklist, not metered),\n` +
  `node_count = parsed from JSON, M_F_T = MOTION:M/FENCE:F/TEXTURE:T, ` +
  `stop_reason = end_turn, persisted_path = harvested_nodes/${convUuid}.md\n\n` +
  `Return: LOGGED`,
  {agentType: 'Explore', label: 'log-row'}
)

log('Pipeline complete for ' + convUuid)
