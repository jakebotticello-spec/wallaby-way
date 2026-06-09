# Prior-Art Survey: claude.ai Conversation-Capture Tooling
_Research date: 2026-05-27. Research only — no code was installed, run, or built._

---

## Context: What We're Building

A Brave/Chrome extension that **passively captures** the network payload from `GET /api/organizations/{org}/chat_conversations/{conv_uuid}` as the claude.ai SPA fetches it, then persists the raw JSON (including `content` blocks of type `text`, `thinking`, `tool_use`, `tool_result`; per-message `uuid`; `parent_message_uuid`; `current_leaf_message_uuid`) as the verbatim floor of a memory-continuity system.

Key distinction from all existing tools: **we want passive capture at network layer, not on-demand export**.

---

## Critical Architectural Finding (Read This First)

**Chrome/Brave MV3 cannot passively intercept response bodies.** `browser.webRequest.filterResponseData()` — the only browser API that lets an extension read response bodies in-flight — is **Firefox-only**. Chrome's MV3 removed `webRequestBlocking` for general extensions and never shipped `filterResponseData`. Brave follows Chromium here.

Practical consequence: on Chrome/Brave, the only viable "capture" strategy is an **active authenticated re-fetch** — content/service-worker script detects a conversation load (URL change or DOM signal), then makes its own `fetch(chat_conversations/{uuid}?tree=True&render_all_tools=true, {credentials: 'include'})`. Result is functionally identical to passive intercept but is triggered by our code rather than by hooking the page's own request. All Chrome-targeting tools already do this.

---

## Ranked Shortlist (Closest Matches)

### #1 — legoktm/claude-to-markdown
**Why it's close:** The only tool that implements the true passive network-intercept pattern we want — `chrome.webRequest.onBeforeRequest` + `browser.webRequest.filterResponseData` — matching exactly our URL pattern.

| Signal | Value |
|--------|-------|
| URL | https://github.com/legoktm/claude-to-markdown |
| Capture method | **NETWORK intercept** — `webRequest.onBeforeRequest` + `filterResponseData` on `*://claude.ai/api/organizations/*/chat_conversations/*` |
| Content completeness | Converts to Markdown (lossy); raw JSON stored in `chrome.storage.local` as `lastIntercepted` (full payload before conversion) |
| Preserves UUIDs / tree / branches | Yes — raw JSON captured before any transformation |
| Storage target | `chrome.storage.local` (JSON payload); Markdown to GitHub Gist |
| License | Apache-2.0 ✅ |
| Maintenance | 18 stars, last commit May 2026, not archived |
| Target platform | claude.ai |
| **Critical caveat** | Firefox only (uses MV2 `webRequestBlocking` + `filterResponseData`; not supported in Chrome/Brave MV3) |

**Background.js key code:**
```js
const CLAUDE_URL_PATTERN = /^https:\/\/claude\.ai\/api\/organizations\/[\w-]+\/chat_conversations\/[\w-]+\?tree=True.*?/;
chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    let filter = browser.webRequest.filterResponseData(details.requestId);
    filter.ondata = event => { str += decoder.decode(event.data, {stream: true}); filter.write(event.data); };
    filter.onstop = event => {
      const jsonData = JSON.parse(str);
      chrome.storage.local.set({ lastIntercepted: { timestamp, url: details.url, content: jsonData } });
      filter.disconnect();
    };
  },
  { urls: ["*://claude.ai/api/organizations/*/chat_conversations/*"], types: ["xmlhttprequest"] },
  ["blocking"]
);
```

**What's reusable:** The exact webRequest pattern, URL filter, and `filterResponseData` approach — fork this for Firefox. For Chrome/Brave, use the same URL filter pattern but trigger an active re-fetch instead.

---

### #2 — agoramachina/claude-exporter
**Why it's close:** Most maintained claude.ai exporter (72 stars, updated May 27 2026), MIT, MV3 Chrome-compatible, calls the exact endpoint with `tree=True&render_all_tools=true`, captures thinking + tool_use blocks.

| Signal | Value |
|--------|-------|
| URL | https://github.com/agoramachina/claude-exporter |
| Capture method | **API fetch from content script** — `fetch(chat_conversations/${id}?tree=True&rendering_mode=messages&render_all_tools=true, {credentials:'include'})` |
| Content completeness | Full JSON available; exports to JSON/Markdown/Text. render_all_tools=true means tool_use/tool_result included; thinking blocks present in raw JSON |
| Preserves UUIDs / tree / branches | Yes — exports JSON with all branches; current branch only in Markdown |
| Storage target | Local file download (JSON, MD, ZIP) |
| License | MIT ✅ |
| Maintenance | 72 stars, 31 forks, v1.10.17 (May 19 2026), active |
| Target platform | claude.ai |
| Manifest | MV3, no `webRequest` (pure content script + scripting API) |

**What's reusable:** Content script `fetchConversation()` function, org-ID auto-detection from `/api/organizations`, model-snapshot tracking, the full fetch boilerplate. We'd add: auto-trigger on URL navigation instead of popup click, and persistence to IndexedDB/chrome.storage rather than file download.

---

### #3 — HumainLabs/claude-chatgpt-backup-extension
**Why it's close:** Only dual-platform (Claude + ChatGPT) TypeScript extension using background script fetch; calls the exact `chat_conversations?tree=True&render_all_tools=true` endpoint; explicitly captures thinking blocks.

| Signal | Value |
|--------|-------|
| URL | https://github.com/HumainLabs/claude-chatgpt-backup-extension |
| Capture method | **API fetch from background script** — `fetch(.../chat_conversations/${conversationId}?tree=True&rendering_mode=messages&render_all_tools=true, {credentials:'include'})` |
| Content completeness | Full raw JSON including thinking blocks (confirmed in README); tool_use/tool_result via render_all_tools |
| Preserves UUIDs / tree / branches | Yes — stores verbatim API JSON |
| Storage target | Local file download (JSON) |
| License | MIT (README claims MIT; GitHub shows NOASSERTION — LICENSE file should be verified) |
| Maintenance | 4 stars, 3 forks, last commit 2026-02-27, not archived |
| Target platform | claude.ai + chatgpt.com |
| Manifest | MV2, `cookies` + `downloads` permissions, background persistent:false |

**What's reusable:** `fetchConversationDetails()` TypeScript function, cookie extraction for org-ID, the dual-platform architecture pattern. We'd add: navigation listener to auto-trigger, replace file-download with IndexedDB persistence.

---

### #4 — twilligon/claude-backup
**Why it's close:** Cleanest pure-API implementation (Python CLI), reverse-engineers the full `chat_conversations` endpoint, preserves raw API JSON with human-readable naming, CC0 (maximum freedom).

| Signal | Value |
|--------|-------|
| URL | https://github.com/twilligon/claude-backup |
| Capture method | **Direct API calls** via Python aiohttp + browser_cookie3 (extracts session from browser's cookie store) |
| Content completeness | Raw API JSON responses; incremental sync by updated_at |
| Preserves UUIDs / tree / branches | Yes — stores verbatim API JSON including UUID tree |
| Storage target | Local filesystem `~/.local/share/claude-backup`, organized by org |
| License | CC0-1.0 ✅ (public domain) |
| Maintenance | 6 stars, last commit May 19 2026, not archived |
| Target platform | claude.ai |

**What's reusable:** The API call pattern, incremental sync logic, rate-limit handling — directly portable to a background service worker. Not a browser extension, so no direct code reuse, but the API choreography is valuable reference.

---

### #5 — Emnolope/claude-conversation-export
**Why it's close:** Bookmarklet that calls the exact endpoint (`chat_conversations/{id}?tree=True&rendering_mode=messages&render_all_tools=true`), zero-dependency, captures full tree including hidden branches, no install required.

| Signal | Value |
|--------|-------|
| URL | https://github.com/Emnolope/claude-conversation-export |
| Capture method | **API fetch via bookmarklet** — same authenticated fetch pattern |
| Content completeness | tool_use/tool_result via render_all_tools; thinking block preservation unclear |
| Preserves UUIDs / tree / branches | Yes — full DAG structure, explicit design goal |
| Storage target | XML file (dot/dash notation for branch hierarchy) |
| License | None specified ❌ (no license = all rights reserved by default) |
| Maintenance | 0 stars, 11 commits |
| Target platform | claude.ai |

**What's reusable:** The bookmarklet demonstrates the minimal viable fetch — useful as a quick test harness. Cannot be legally cannibalized (no license).

---

## claude-mem — Storage/Retrieval Substrate Assessment

| Signal | Value |
|--------|-------|
| URL | https://github.com/thedotmack/claude-mem |
| Stars | 79,061 (largest repo in this survey) |
| License | Apache-2.0 |
| Purpose | Claude Code session memory — hooks into Claude Code lifecycle (SessionStart, PostToolUse, Stop, etc.) to capture agent observations, compress with AI, and inject into future sessions |
| Capture mechanism | Claude Code hooks (NOT browser/network interception) |
| Data structures | SQLite (FTS5), Chroma vector DB, HTTP API on port 37777 |
| Relevance as substrate | **Moderate** — excellent at semantic search/retrieval; designed for Claude Code tool-call observations, not claude.ai web conversation JSON. Could ingest our captured conversation payloads if we write an adapter, but schema mismatch is significant |
| Storage fit | Would need to extract meaningful "observations" from raw conversation JSON rather than storing verbatim — different from our "verbatim floor" requirement |

---

## Portable Prior Art — ChatGPT Exporters

| Name | Capture Method | Stars | License | Endpoint Called | Notes |
|------|---------------|-------|---------|-----------------|-------|
| pionxzh/chatgpt-exporter | Active fetch from Tampermonkey userscript | 2,490 | MIT | `/backend-api/conversation/{id}` | Most popular; calls the conversation API then offers JSON/MD/HTML/PNG export. Full message mapping preserved. |
| hoya98/chatgpt-export | Content script authenticated fetch | 9 | MIT | `/backend-api/conversations` + `/backend-api/conversation/{id}` | Bulk export, handles Team/Business workspaces, rate-limit handling |
| vincze-tamas/chatgpt-exporter | Content script fetch | 0 | MIT | `/backend-api/gizmos/{id}/conversations` + `/backend-api/conversation/{id}` | Flat JSON output (flattens tree), project-aware |

**Pattern:** All ChatGPT exporters use active authenticated fetch from content/userscript context — no passive network intercept tools found for ChatGPT either. This is the universal approach. Forking pionxzh/chatgpt-exporter for claude.ai would require: replacing the ChatGPT auth flow with Claude's cookie-based auth, swapping the backend-api URL for claude.ai's `chat_conversations` endpoint, and adapting the message-mapping schema.

---

## Full Candidate JSONL Reference

See `prior_art.jsonl` in this directory for all candidates.

---

## Network-Capture vs DOM-Scrape Tally

| Approach | Tools Found | Notes |
|----------|-------------|-------|
| True passive network intercept (`webRequest.filterResponseData`) | **1** (legoktm — Firefox only) | This path exists but is Firefox-exclusive |
| Active authenticated re-fetch from extension context | **6** (agoramachina, HumainLabs, withLinda, twilligon, Emnolope, vincze-tamas) | Functionally equivalent result; universal across Chrome/Brave/Firefox |
| DOM scraping | **~4** (ryanschiang, agarwalvishal, Llaves, some modes of socketteer) | Lossy — loses thinking + tool_use structure |
| Total surveyed | ~14 | |

**Key takeaway:** The active-fetch approach is well-trodden (6 tools); the passive-intercept approach is essentially untrodden for Chrome/Brave (0 tools). Our "network capture" goal is best served by the active-fetch pattern on Brave, since true passive intercept isn't possible in Chromium MV3.

---

## Recommendation

**Fork/cannibalize `agoramachina/claude-exporter` (MIT, 72 stars, MV3, active May 2026).**

**Keep:**
- `fetchConversation(orgId, conversationId)` — calls our exact endpoint with `tree=True&rendering_mode=messages&render_all_tools=true`
- Org-ID auto-detection from `/api/organizations`
- The content script injection and MV3 manifest skeleton
- Model-snapshot tracking (bonus: tracks model drift across sessions)

**Replace/add:**
- Remove the popup export UI and format-conversion logic
- Add a `chrome.webNavigation.onHistoryStateUpdated` listener (or URL-change detection in the content script) to auto-trigger capture when navigating to `/chat/{uuid}`
- Replace `chrome.downloads.download()` with `chrome.storage.local` or IndexedDB persistence of the raw JSON payload
- Add deduplication by `uuid` and a delta-check on `updated_at` to avoid re-capturing unchanged conversations

**Why not legoktm:** It does the passive intercept we ideally want, but Firefox-only and converts to Markdown (lossy). On Chrome/Brave the active-fetch result is indistinguishable and is already proven.

**Why not HumainLabs:** TypeScript/MV2, low traction (4 stars), license ambiguity. Agoramachina is better maintained and already MV3.

**Why not build from scratch:** The fetch pattern, org-ID detection, and API endpoint parameters are non-trivial to reverse-engineer. Agoramachina has already done this work correctly, is MIT, and actively maintained. We're adding a trigger mechanism and persistence layer — that's the actual novel work.

---

## Anthropic Native Export (FYI)

Anthropic offers a built-in data export via Settings → Privacy → Export Data. It produces a ZIP of all conversations as JSON. Limitations: all-or-nothing (no single-conversation export), download link expires in 24h, desktop only, unknown whether it includes `thinking` blocks or `tool_use` payloads. Not useful for a real-time memory-continuity system.
