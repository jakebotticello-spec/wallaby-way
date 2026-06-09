S40 apparatus — STAGE B DELIVERY-PATH FIX. This WRITES CODE. Enter PLAN MODE first. Do NOT edit/build/run/commit until I approve your plan. Read the PROHIBITIONS before forming any plan — they are hard NOs, not preferences.

FIRST: write this prompt to cc-plans\S40_delivery_fix.md, then proceed to plan mode.

=== PROHIBITIONS (read first — these are the recurring traps; violating any = stop and re-plan) ===
P1. Do NOT keep an agent() in the payload-delivery step. The bug is that agent() returns a model text response (a summary), never raw bytes. The delivery MUST be a non-agent read (JS reads the file directly). If your plan routes payload content through any agent() call, it's wrong.
P2. Do NOT leave the payload file on disk during the scope-reader call. The fix's core is that the file is GONE before the reader runs, so there's nothing to self-read. If your plan keeps the file present during the read "for safety/audit/convenience," it's wrong — the floor is the immortal source; the payload is regenerable.
P3. Do NOT weaken any guard to make the flow simpler. assert_env_unloaded, tally_nodes, persist_node_file, the parents/sidecar integrity — all stay ENFORCED. If a guard is inconvenient, that's not license to comment it out or downgrade it. New guards get ADDED, none removed.
P4. Do NOT claim anything is "approved," "verified," or "per Jake" unless it literally is. Your plan is a proposal until I say go. Don't round "I think this is fine" up to "approved."
P5. Disk over memory. Read the actual current onsub_loop.js, floor_extract.py, persist_guard.py, pipeline_guards.py before planning. If reality differs from anything I describe below, the DISK wins — flag the discrepancy, don't build to my description.

=== THE PROBLEM (settled, do not re-diagnose) ===
Two joints break the no-foothold guarantee:
- Joint 1: the read-payload step is an Explore agent running `cat` — agent() returns the model's SUMMARY, not raw content. Large payloads reached the scope-reader as a ~1.6K-char summary of a 7.5K-line conv.
- Joint 2: the payload file sits on disk + the scope-reader runs with no agentType = Tools:* including Read + the path leaks into context = the reader self-reads the file (36 Read calls observed). agent() has NO tools-restriction param (confirmed from source: opts = {label,phase,schema,model,isolation,agentType}); Explore is read-only but still has Read. So the reader CANNOT be made structurally toolless on this mechanism.

=== THE FIX (this is the design; your plan implements it against real code) ===
Convert blindness from "by absence-of-tool" (impossible here) to "by absence-of-target" (free), plus defense-in-depth:

1. RAW DELIVERY (fixes Joint 1): delete the read-payload Explore-agent step entirely. The harness is JS and the payload file is on disk from floor_extract — read it directly into a JS string with fs.readFileSync(path,'utf-8'). payloadText becomes the TRUE complete raw payload, no agent in the middle.

2. DELETE-BEFORE-READ (fixes Joint 2 structurally): after reading the payload into the JS string, and after reading whatever the sidecar/parents step needs into memory, DELETE the payload file from disk BEFORE the scope-reader agent() call fires. The reader runs on the in-memory string only. File gone = nothing for Read to reach, regardless of tools or a leaked path. Sequence carefully against the sidecar — persist_node_file needs the parents map; make sure everything downstream needs from disk is already in memory before the unlink. Show me the exact ordering in your plan.

3. GUARDS (defense-in-depth, additive — P3):
   a. agentType:'Explore' on the scope-reader call — strips Write/Edit so it structurally cannot write anywhere, even though it retains Read (and Read now has no target). (Confirm Explore doesn't break the reader's output-return path — the scope-reader returns node text as its response, which Explore can still do.)
   b. DELIVERY-LENGTH GUARD: before the scope-reader call, assert payloadText length is consistent with floor_extract's reported byte count (floor_extract prints "Wrote N bytes"). If delivered text is materially short of N, HALT — catches a truncated/failed read instead of cataloging a partial conv guard-green.
   c. READ-CALL TRIPWIRE: a correct run on raw embedded text should make ZERO Read calls from the scope-reader. If the run surface exposes the scope-reader's tool calls, check for any Read call and FLAG that conv for review. If the mechanism doesn't expose per-agent tool calls post-hoc, say so and note it as a gap — don't fabricate the check.

4. RESUMABILITY must survive: if a conv's read fails after the payload file is deleted, a re-run must cleanly re-extract from the floor (the floor is immortal). Confirm the loop handles "payload file absent → re-extract" without choking. Already-harvested convs (in harvested_nodes/) still skip.

=== PLAN MODE DELIVERABLE ===
A single consolidated plan: every file you'll touch + every change + the exact NEW ordering of the per-conv steps (extract → read-into-memory → [what else must be in memory] → delete file → scope-read → persist), how each guard is wired, any spot where the sidecar/parents sequencing is delicate, and any place the real code differs from my description above. Surface open questions BEFORE editing. Then STOP and wait for my one approval.

After approval (not before): build → commit to a scratch branch → `gh pr create --draft` → run code-review:code-review on the PR → report findings. Do NOT merge or delete the branch — Jake pushes/merges, and per the rule: merge → checkout main → pull → eyeball the commits on main → THEN delete branch. That's all post-approval; right now, PLAN ONLY.

S40 FLAG-1 probe: testing fs/Buffer availability in Workflow runtime before approving the fix.
S40 schema-mechanics probe: testing whether agent() schema can carry a large raw payload field before re-architecting delivery.
S40 max-scale probe: testing schema passthrough on the largest non-whale payload before re-architecture plan.
