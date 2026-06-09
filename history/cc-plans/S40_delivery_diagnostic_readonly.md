S40 apparatus — READ-ONLY DIAGNOSTIC (delivery-path bug). Do NOT write, edit, commit, push, or run the loop. No mutations. This is reads + reporting raw code so OC can spec a fix. If anything is ambiguous, STOP and report rather than guess.

FIRST: write this prompt to cc-plans\S40_delivery_diagnostic_readonly.md, then proceed.

Working dir: the apparatus working repo (pipeline/s39/ present). Confirm with pwd + ls pipeline/s39/.

CONTEXT (what we're diagnosing — do not act on it, just inform your reads): on the 01eb6e56 READ-2 run, the read-payload agent returned a ~1,645-char SUMMARY of a 7,527-line payload instead of raw content, and the scope-reader then self-read the payload file directly via 36 Read calls — finding the path from context. This breaks the embedded-payload / no-foothold guarantee. I need to see the ACTUAL code paths to fix it. Quote literal code; do not summarize or paraphrase the logic.

=== READ A — the delivery step in the harness ===
cat pipeline/s39/onsub_loop.js   (the WHOLE file)
Then point me to, with literal line quotes:
  (a) the read-payload agent call — how it's invoked, what agent TYPE it uses, what its prompt/instruction says, and how its return value is captured into the JS (the variable that becomes payloadText or equivalent).
  (b) the scope-reader call — how it's invoked, what agent TYPE, what tools it has available (does the call grant/restrict tools? is Read available?), and EXACTLY what is passed into its prompt (the BOOT_SCOPE_READER text + what payload variable — is it the raw content, or the read-payload agent's return summary?).
  (c) anywhere a FILE PATH to the payload appears in any string that reaches the scope-reader's context (prompt, system text, anything). I want to know if the path is leaking into the reader's context at all.

=== READ B — floor_extract output shape ===
cat pipeline/s39/floor_extract.py   (the WHOLE file)
Report: does floor_extract write the payload to a FILE on disk (what path pattern?), return it as a string, both? Show the literal write/return lines. This tells me whether a path-to-the-payload exists on disk at all during the read (if there's no file, there's no foothold).

=== READ C — agent mechanism reality check ===
I need the literal truth about the agent call primitive the harness uses (the `agent()` / Task / Explore call). From onsub_loop.js (and any helper it imports):
  (a) When you invoke the scope-reader agent, CAN you pass a tools-allowlist / restrict it to NO tools? Quote the call signature / options actually used. If the mechanism grants Tools:* uncontrollably (the S36 finding), confirm that from the code/docs available to you — don't assert from memory.
  (b) For the read-payload step: is there any way in this mechanism to get raw file content into a JS string WITHOUT an agent summarizing it — e.g. Bash `cat` piped to stdout captured directly, or a Python read-to-stdout? Show me whether the harness already has a non-agent file-read path available (even if unused).

=== REPORT FORMAT ===
Raw code quotes for A/B/C — this is the one place I need literal lines, not your reading. After the quotes, give me a tight plain-English map: "raw content lives HERE → gets delivered to the reader via THIS → reader has/doesn't have a Read tool → path is/isn't in reader context." That map is what I'm speccing the fix against. Flag anything that surprised you. Confirm at the end that every action taken was a read — zero mutations.

S40 follow-up: agent() tool-restriction capability check.
