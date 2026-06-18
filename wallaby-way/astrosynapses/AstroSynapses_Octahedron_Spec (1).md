# AstroSynapses — Octahedron Construct — Build Spec
*Spec v1.0 · authored S66 · prototype reference: `astro_octahedron.html` · for parallel construction track*

---

## 0. What this is
An interactive 3D visualizer for the Wallaby Way corpus: **8,288 nodes / ~49,078 cosine edges** rendered as a **Sierpinski octahedron** — a translucent faceted solid whose 8 faces map to the 8 corpus clusters, with semantic connections running the structure and animated current/atmosphere. Real-time, browser-based (Three.js). Presentation-grade target: the look-and-feel reference is winter/ice — *clean, frosted, luminous on snow-white* — NOT neon/Tron, NOT weathered/apocalyptic (both were explored and rejected).

The prototype proves the concept and layout. This spec defines the **finished** build. Honest delta from prototype: prototype is ~35–40% of achievable; the finish roughly doubles–triples perceived quality via the items in §6.

---

## 1. Hard constraints (carry verbatim)
- **Three.js r128.** No `OrbitControls` (hand-roll orbit). No `CapsuleGeometry` (r142+). Use `SphereGeometry`/`PlaneGeometry`/`BufferGeometry`.
- **No browser storage** (`localStorage`/`sessionStorage`) — fails in target render context. State in JS memory only.
- **Single self-contained HTML file.** Inline JS/CSS. Three.js may load from CDN; offer an **inlined-Three.js offline variant** as a build option (corp network sometimes offline).
- **Data is synthetic in prototype.** Real wiring to `nodes.json` / `edges.json` is a defined later step (§5). Prototype data: real 8 cluster names + proportions, ~520 sample nodes.
- Every code file carries the standard header comment: file name, version (vX.X), session (SX), change notes.

---

## 2. Geometry

### 2.1 The solid
- **Octahedron**, 6 vertices / **8 triangular faces**. Faces 0–7 map 1:1 to the 8 clusters (see §3 roster). This 8:8 mapping is the core structural rhyme — keep it.
- Faces are **frosted translucent** (light blue-white, ~0.13–0.18 opacity, phong/standard with specular) so the interior is visible through them. The solid must read as *present* — a real object, not implied.

### 2.2 Face skin (the triangle weave)
- Each face is tiled into **rows of small triangles** via barycentric subdivision (`FACE_DIV` rows; prototype uses 5). This is the "Faraday wireframe laid over the octahedron face" — it lines up as clean rows down each face.
- Skin drawn as line segments, steel-blue (`~0x33455C`), ~0.4–0.5 opacity, breathing (see §4).
- **Finish upgrade:** skin should be a true mesh with subtle depth/bevel on the struts, not flat lines — so light catches the weave.

### 2.3 Inner Sierpinski depth (build "b")
- Behind the skin: **recursive inner-pyramid struts**, classic open-Sierpinski subdivision of each face (prototype: depth 3), pulled inward to ~0.82× radius so they read as fractal depth *behind* the frosted faces.
- This is the "see-into-it" layer. Jake was trending away from it but confirmed it for the build; keep as a **toggleable layer** so it can be dropped without rework.

---

## 3. Nodes (cluster roster + placement)

### 3.1 Roster (real proportions; colors are prototype winter-palette starting points)
| Face | Cluster | Proportion | Prototype color |
|---|---|---|---|
| 0 | Apparatus / Memory | ~50% | `0x2E6FA8` |
| 1 | Pyris / Ops | ~10% | `0x3F9C8A` |
| 2 | Cypher / Voice | ~8.5% | `0x7A6CC0` |
| 3 | CCF / Recruiting | ~7% | `0xB89A3C` |
| 4 | Maker / 3D-print | ~7% | `0xC06A44` |
| 5 | RecruitMail / LRN | ~4.5% | `0x4F6C92` |
| 6 | Scheduling / Body | ~4.5% | `0x3E94A8` |
| 7 | GloTwp / Portal | ~2.5% | `0x8A5CB0` |

- **Uneven density is correct and honest** — Apparatus face packed, GloTwp sparse. Do NOT fake-balance. (Real corpus: cluster inventory from S66 region build — apparatus ~50% dominant is real.)

### 3.2 Placement & appearance
- Nodes sit **flush on the face skin** (snap to nearest skin vertex; **no outward normal lift** — the lift caused the "floating balls on stalks" defect).
- Render as **flat embedded discs** (soft radial falloff, white-kissed core in cluster color), NOT spheres-on-stalks. Loud nodes brighter/larger but eased (prototype sizes 6/4/2.6 for salience 3/2/1) so they read as *set-in lights*, not balls.
- Salience drives size + glow + slight pull toward face center.
- **Finish upgrade:** nodes set *into* the crust/skin — glowing from within the weave, occluded by struts in front, so they feel embedded not stuck-on.

---

## 4. Connections (the defect to solve properly)

### 4.1 The known defect
Prototype routes connections as **free-space bezier curves**: intra-face hug the skin (OK), but cross-face bow through open space. Outward bow → "shafts waving like flags." Inward bow (current state) → "shafts penetrating the solid." **Both read as protrusions/shafts off the nodes.** This is the one unsolved look problem.

### 4.2 The correct fix (finish requirement)
- **All connections trace the actual structure** — never free space.
  - Intra-face: route along the **face skin triangle-rows** (BFS through skin mesh — prototype already does this).
  - Cross-face: route **along skin to a shared edge/vertex, then along the adjacent face's skin** — i.e. the path walks the surface weave across the face boundary, OR descends into the **inner Sierpinski struts** and traverses the interior lattice to re-emerge. Pick one consistently; surface-walk is cleaner, interior-traverse is more "see-into-it."
  - The point: a connection is always *a path along edges that exist*, so it can never spear through open space. No node ever sprouts a free shaft.
- Connections drawn as faint traced lines; **arc-pulses** ride them (see §4.3).

### 4.3 Current / arc-pulses
- Electrical-arc pulses travel the routes: **bright white head + short fading blue tail** (prototype: 6-point tail, additive-free on white bg).
- Cap visible pulsing routes (~150–160) for framerate + readability. On real 8,288-node data this capping is load-bearing — a fully-lit graph is a white blob. Select a strong subset (e.g. highest-weight or salience-gated edges) to carry current.

---

## 5. Wiring to real data (later step — defined here)
- Source: `nodes.json` (8,288 nodes; identity = `conv_uuid` + `anchor_msg`; carries cluster/strata tag, salience, embed_text/curation) and `edges.json` (k=8 kNN, ~49,078 edges, cosine weight `w`, `si`/`ti` index into nodes).
- **819-duplicate hazard:** 8,288 graph nodes resolve to **7,469 distinct floor identities** — 819 graph nodes share a floor identity. Collect all `node_idx` per identity; decide whether duplicates render once or as-is. Will be visible in any layout; a clean view makes it easier to reconcile.
- **Cluster → face assignment:** use the real cluster tags. Apparatus is ~50% — its face will be dense; plan LOD/clustering for that face specifically.
- **Node placement rule (undecided — design call):** where on its face does a node sit? Options: by sub-cluster similarity (2D-project the cluster onto the face), by salience (loud toward center), or kNN-layout within face. Pick deliberately; prototype uses random barycentric + salience pull as placeholder.
- **Density unknown:** all prototype judgments are on ~520 nodes. Real corpus is ~15× denser. Aesthetic survives but needs tuning against real density — this is the one genuine unknown; budget a tuning pass after first real wire.

---

## 6. Finish upgrades (what takes it from prototype → presentation-grade)
Roughly doubles–triples perceived quality. None require concept change.
1. **PBR materials** — albedo + normal + roughness + AO + displacement on skin/faces so light catches physical relief (biggest single jump).
2. **Lighting & atmosphere** — real shadow-casting, HDRI environment for reflections, volumetric haze/dust with depth. ~70% of "mood" is lighting.
3. **Post-processing** — controlled bloom (embers only), depth-of-field (far side softens), film grain, color grade toward bleached-cool winter palette. Makes it stop looking like "a 3D viewer."
4. **Connections traced on structure** (§4.2) — solves the shaft defect.
5. **Nodes embedded in weave** (§3.2) — glow from within, occluded properly.
6. **Geometry density** — finer Sierpinski recursion + higher FACE_DIV for crisp silhouette/holes (balance vs framerate).

### Permanent ceilings (set expectations)
- Real-time WebGL ≠ offline film render. Will look like an excellent interactive piece, not an Octane still. Hard ceiling.
- Procedural-believable ≠ hand-crafted. Budget ceiling, not possibility ceiling.

---

## 7. Motion inventory (all present in prototype; keep as toggleable layers)
- **Arc pulses** — head+tail current along routes.
- **Breathing** — gentle whole-solid scale + skin/face opacity pulse + loud-node brightness pulse.
- **Drifting mist** — soft sprite cloud slowly orbiting; rises/falls. (Finish: true volumetric.)
- **Contact shadow** — soft blurred disc beneath, grounds the object.
- **Slow auto-orbit** when idle; respects `prefers-reduced-motion`.
- All five exposed as **toggles** (prototype has: arc pulses / breathing / drifting mist / face skin / inner struts).

---

## 8. UI / interaction
- Hand-rolled orbit (drag), zoom (scroll), touch equivalents.
- Hover a node → trace its connections in accent; show cluster + salience tooltip.
- Legend = the 8 clusters with proportions; click to isolate/toggle a cluster (= a face).
- **Face-flatten (stretch):** click a face → unfold/snap to a 2D salience-map tile of that cluster. Prototype has a camera-snap approximation; true unfold is a finish item.
- Palette: winter — snow-white radial-gradient bg, steel/ice-blue structure, cluster-colored node embers, arc-blue current. Fonts: Chakra Petch (display), Space Mono (data).

---

## 9. Build order (recommended)
1. Geometry: octahedron + face skin + inner Sierpinski (toggleable). ✓ prototype
2. Connection routing **on-structure** (solve §4.2 properly). ← first real finish work
3. Wire real `nodes.json`/`edges.json` (§5) + 819-dupe handling + face assignment.
4. Density tuning pass on real data.
5. Materials/lighting/post (§6.1–6.3).
6. Node embedding + face-flatten + polish.

*End spec v1.0.*
