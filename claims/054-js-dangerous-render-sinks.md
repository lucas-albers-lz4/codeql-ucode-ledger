# Claim 054: JS dangerous-render sinks in pinned views

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: syntax oracle (pinned luci JS; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-8v49-6387-7f89 (upnp port-mapping XSS)
- GHSA-vvj6-7362-pjrw / CVE-2026-32721 (WiFi scan modal)
- CVE-2019-25015 (SSID stored XSS)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI JS views contain dangerous-render sink shapes (innerHTML, insertAdjacentHTML, unescaped template interpolation into DOM), as a syntax inventory with controls?

## Method

JS syntax inventory (step1-style) over manifested view set; sink shapes fixed before inspection; no execution, no Track A staffing.

## Required evidence

- Sink-shape multiset with file/line provenance
- Shape definitions and independent transcription of expected cases

## Controls

- Positive: innerHTML assignment from non-literal
- Near miss: textContent assignment
- Negative: innerHTML with literal-only string

## Out of scope

- No runtime DOM behavior
- No taint through JS
- Track A remains unstaffed

## Notes

None.

## Result

Demonstrated — syntax inventory at luci `b2e0be4b…`; no CodeQL database; JS
UCI hold and Track A state unchanged; syntax-only (no execution/taint claim;
raw_call/raw_variable classes do not assert runtime unencodedness).

- 138 dangerous-render sink sites across modules/applications htdocs
  resources JS (133 innerHTML writes + 5 d3-selection .html();
  insertAdjacentHTML/outerHTML/document.write absent). Exact multiset
  byte-verified; 156 grep lines partition into 138 sites + 18 declared
  exclusions (9 comments incl. olsr-viz.js:642–647 block, 8 reads, 1 E()
  attribute-map key → setAttribute), 0 uncovered / 0 phantom. 0 min.js,
  0 jQuery (.html hits are vendored netjsongraph.js d3-selection).
- At-sink classes: literal 49, literal_composed 9, encoded 0, raw_variable 40,
  raw_mixed 18, raw_call 22 (claim families: literal 58 / escaped-encoded 0 /
  raw 80). No encoding helper at any sink argument; %h-at-construction
  recorded for babeld (8 sites) + partial %h in librespeed chart;
  battstatus.js:41 ${} is inert single-quoted text; rustdesk general.js:447
  interpolates public_key into text AND an onclick attribute string. Safe
  context: textContent 102 / innerText 30 / createTextNode 21 lines.
- Controls 3/3 pass (near-miss literal branch; encoded census 0). Oracle rev1
  fixed before inventory, no revisions after.
- Evidence: `/root/workspace/work/security-40/054/` (oracle.{md,json},
  js_sinks.json, controls.json, provenance.json, run_pipeline.sh,
  recon_sinks.txt, recon_html_calls.txt). Orchestrator re-ran
  `run_pipeline.sh` (exit 0, 138 sinks, 3/3 controls); luci pin clean.
