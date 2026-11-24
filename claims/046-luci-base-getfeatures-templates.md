# Claim 046: Fixed-command template substitution in getFeatures

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (GetFeaturesDirectExec.ql on manifested 1-file DB) + source oracle
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- M4 documented unmodeled set: hostapd/wpa_supplicant system() templates, dnsmasq/odhcpd/ipset popen

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What command-template substitution sites exist in pinned luci-base getFeatures beyond the five M4-inventoried methods, and which carry request-derived vs config-derived values?

## Method

Source inventory of getFeatures handler command construction at pinned luci SHA; classify value provenance (request.args vs uci/config vs literal); bounded query only where the supported slice reaches.

## Required evidence

- Template-site multiset with provenance class
- Source lines and oracle

## Controls

- Positive: config-derived substitution site
- Near miss: request-derived site inside supported slice
- Negative: fully literal command

## Out of scope

- No claim of full getFeatures coverage
- No interprocedural init_action modeling

## Notes

This is the documented M4 gap turned into a named bounded decision.

## Result

Demonstrated — bounded source inventory + exact query confirmation on the
covered slice. Evaluated 2026-11-24; CodeQL CLI 2.27.4 (`gh codeql`).

- Beyond the five M4-inventoried methods, getFeatures command construction
  contains **4 substitution sites**: L268 `system(/usr/sbin/hostapd
  -v${feature}…)` and L275 `system(/usr/sbin/wpa_supplicant -v${feature}…)`
  (feature ranges only over the closed literal `wifi_features` array,
  L248–262, 13 literals); and L26 `popen('opkg list-installed ' +
  shellquote(pkg)…)` / L37 `popen('apk list -I ' + shellquote(pkg)…)` in
  helper `callPackageVersionCheck`, whose sole call site L313 binds literal
  `'netifd'`.
- Provenance: **literal 2, other-named-literal-bound 2, request-derived 0,
  config-derived 0**. `getFeatures.call` is `function()` with no request
  param/args (L224); uci reads (L122/197/201/203/207) reach non-command
  consumers only — no uci value anywhere in the routed file reaches a
  command string. Three commands fully literal (0 substitutions): L278
  dnsmasq --version, L294 odhcpd -h, L315 ipset --help.
- `GetFeaturesDirectExec.ql` on a fresh manifested 1-file database: exactly
  the 5 predicted direct exec sites (268/275 system; 278/294/315 popen),
  multiplicity 1 each — exact-multiset match, 0 query-only, 0 unexplained
  oracle-only. The 2 helper popen sites are oracle-only against this query
  by its lexical `inGetFeaturesCall` boundary (documented M3 coverage;
  `GetFeaturesPopen` observes 2 rows, entity-label projection only —
  disclosed). Routing: 1 file extracted, 0 extraction errors.
  `RequestArgsExec` fresh run reproduces P2's 5-method/7-row inventory with
  getFeatures absent.
- Oracle fixed pre-query: 39/39 mechanical source checks. Controls 4/5:
  near miss PASS (getSwconfigFeatures L343 request-derived, excluded from
  getFeatures query, present in RequestArgsExec via shellquote); negative
  PASS (L278 fully literal); labeled extras PASS (L268 literal-derived;
  helper-boundary receipt). **Named positive (config-derived site)
  FAIL-no-eligible-instance** — full-file census confirms zero config-derived
  substitutions at this pin (predicted by the fixed oracle); the absence is
  part of the bounded answer, no synthetic instance invented. The
  config-derived classification path is therefore not exercised on real
  source — disclosed limit.
- Receipts: GetFeaturesDirectExec 6.84 s / 319 MB peak; all steps serial,
  ≤389 MB; `run_pipeline.sh` re-run byte-identical (multiset/controls),
  comparison identical after path normalization; orchestrator re-ran the
  pipeline (exit 0) and spot-checked every cited line in the pinned file
  (sha256 6f9d9729… matches MANIFEST).
- Limits: site counts, not runtime enumeration (loops not unrolled); no
  interprocedural modeling, no flow-model extension, no gate lifted; no
  runtime/reachability/authorization/vulnerability claim; 1-file smoke
  slice, timings not extrapolable; application .uc backends remain
  not-routed per P2 (outside this claim's file set).
- Evidence: `/root/workspace/work/security-40/046/` (summary.md, oracle.md,
  oracle.json, oracle_check.json, multiset.json, comparison.json,
  controls.json, provenance.json, MANIFEST.yml, receipts/, logs/,
  run_pipeline.sh, rerun-verify/).
