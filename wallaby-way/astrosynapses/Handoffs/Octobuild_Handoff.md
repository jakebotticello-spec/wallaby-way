# Octobuild — Session Handoff (Parallel Track)
*Track: AstroSynapses Octahedron visualizer · Origin: apparatus S66 · Status: prototype LOCKED, finish build NOT started*
*This is a PARALLEL track, separate from the apparatus lineage. It does not touch the floor, the gate, or canon.*

---

## What this track is
Build the **finished** AstroSynapses octahedron corpus visualizer from the locked prototype + spec. The spec is the authority. This track runs independently of apparatus sessions — its only dependency on the apparatus is read-only consumption of `nodes.json` / `edges.json` when it reaches the real-data wiring step (§5 of the spec).

## Artifacts (carry these in)
1. **`AstroSynapses_Octahedron_Spec.md`** — the build authority. Geometry, constraints, defects, finish upgrades, build order. Read it first and in full.
2. **`astro_octahedron.html`** — the locked prototype. The reference for layout, motion, and palette. ~520 synthetic nodes. The thing the finish must surpass, not match.

## State at lock
- **Concept proven.** Octahedron, 8 faces = 8 clusters, frosted translucent solid, triangle face-skin (rows per face) + inner Sierpinski strut depth (toggleable), nodes flush on skin as embedded discs, arc-pulse current, breathing/mist/shadow motion, winter/snow palette.
- **Aesthetic locked:** winter — clean/frosted/luminous on snow-white. Neon/Tron and weathered/apocalyptic were both explored and **rejected**. Do not revisit.
- **Prototype is ~35–40% of achievable.** Finish ≈ 2–3× via PBR + lighting + post (spec §6).

## The one unsolved look problem (top of the build queue)
Connections render as **shafts off the nodes** — prototype routes them as free-space beziers (outward bow = "flags," inward bow = "penetrating the solid"; both read as protrusions). **Fix = route every connection along the actual structure** (face skin triangle-rows; cross-face walks the weave across the shared edge, or descends into the inner Sierpinski lattice). A connection must always be a path along edges that exist, so it can never spear open space. **This is build step 2 (the first real finish work) — do it before materials/polish.**

## Build order (from spec §9)
1. Geometry (octa + skin + inner Sierpinski toggle). ✓ done in prototype
2. **Connection routing on-structure** (solve the shaft defect). ← start here
3. Wire real `nodes.json` / `edges.json`: 8,288 nodes, ~49,078 edges. Handle the **819-duplicate hazard** (8,288 graph nodes → 7,469 distinct floor identities). Real cluster→face assignment.
4. Density tuning pass — all prototype judgments are on ~520 nodes; real corpus is ~15× denser. This is the genuine unknown.
5. Materials / lighting / post-processing (spec §6).
6. Node-in-weave embedding + face-flatten + polish.

## Hard constraints (verbatim, non-negotiable)
- Three.js **r128**. No `OrbitControls`, no `CapsuleGeometry`. Hand-rolled orbit.
- **No** `localStorage` / `sessionStorage`. State in memory only.
- Single self-contained HTML file. CDN Three.js OK; provide an inlined-Three.js offline variant as a build option.
- Standard file header comment on every code file: name, version, session, change notes.

## Permanent ceilings (set expectations, don't fight them)
- Real-time WebGL, not an offline film render. Excellent interactive piece is the target.
- Procedural-believable, not hand-crafted-studio. Budget ceiling.

## Boundaries
- This track does **not** modify the apparatus floor, the Pollux gate, or canon. Read-only on the data exports.
- Jake is the bridge between this track and the apparatus track. Data exports (`nodes.json`/`edges.json`) come from him / the apparatus side; don't assume their on-disk location — confirm when reaching step 3.

*End octobuild handoff.*
