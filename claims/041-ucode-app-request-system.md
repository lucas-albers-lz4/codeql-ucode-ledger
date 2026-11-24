# Claim 041: request.args to system() in application ucode backends

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` — routing probe P2 at HEAD below; application backends not routed
- Producer commit: `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean; probe-ucode/producer); luci slice pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`
- Consumer: none (no consumer join reached)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 / GHSA-wjfh-jfr9-fxvm (dockerman docker_rpc.uc run_ttyd builds shell command from id/cmd/uid)
- GHSA-cq4h-h8jr-3xqv

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Does the M4 same-function request.args→system slice observe request-controlled arguments reaching `system()` in pinned application ucode backends (first target: dockerman docker_rpc.uc), with the documented binding limits?

## Method

Probe P2 extraction routing first; then run the supported RequestArgsExec-style query over a manifested application-backend file set at the pinned luci SHA; compare exact finding identities to a source-derived oracle.

## Required evidence

- Extraction routing receipt (P2)
- Predeclared expected finding multiset from source
- Query identity, pack digests, command/exit/time/memory
- Positive and near-miss fixture results

## Controls

- Positive: request.args field concatenated into system() command (advisory shape, synthetic fixture)
- Near miss: same shape with shellquote in complete-argument position
- Negative: fixed literal system() command

## Out of scope

- No interprocedural flow
- No taint-sanitizer guarantee
- No runtime exploitability
- No claim beyond the same-function binding subset

## Notes

If the pinned source still contains the unquoted advisory shape, record it as a bounded source observation; disclosure is a separate user decision.

## Result

Blocked 2026-11-24 — producer routing gate at codeql-ucode HEAD
`734555a9f56893e89e678cdee63028fc17ea5bc8` (clean clone:
`work/security-40/probe-ucode/producer`).

Probe P2 (`work/security-40/probe-ucode/VERDICT.md`) ran the producer's
documented staging-root method (scripts/m3-smoke.sh / m4-sys-smoke.sh pattern;
grammar pin `4a243af329fae2f4ff01e0fc80133cbab8314600`, Cargo.lock `a88727b3…`
matches README pin; rustc 1.100.0 bootstrap, drift from recorded 1.99.1 noted)
over an 8-file manifested slice at luci `b2e0be4b46ec0fd43394c081fa7c50657af14011`
(7 application .uc backends + luci-base extensionless `luci`; sha256 manifest
in MANIFEST.yml):

- SuccessfullyExtractedFiles = 1 (luci-base `luci` only); the 7 application
  files skipped with extractor diagnostic "No matching language found,
  skipping file" (docker_rpc.uc, ddns.uc, tailscale.uc, example.uc,
  rustdesk-server.uc, wifihistory.uc, weechat.uc); ExtractionErrors = 0 rows.
- RequestArgsExec.ql (@id ucode/m4/request-args-exec, pack
  lucas-albers-lz4/ucode-queries 0.1.0, file sha256 `373b359f…`): exit 0,
  7.75 s, peak 358 MB; 7 rows / 5 methods, ALL from luci-base `luci`,
  0 application rows — exactly the predeclared expectation set (positive
  control for the routed file; getFeatures absent as expected).

Two routing gates, orchestrator-verified in producer source:

1. `extractor/src/extractor.rs` (~l.45–64): ucode `file_globs` are literal
   basenames only ("luci", "sys.uc", taint/quote/cfg/ssa fixtures); comment:
   "M4 adds sys.uc (installed luci.sys) without opening '*' routing".
   No manifest/application allowlist support.
2. `ql/src/m4/RequestArgsExec.ql` (l.18):
   `src.getLocation().getFile().getBaseName() = "luci"`.

Bounded source observation (P2, pinned luci): docker_rpc.uc `run_ttyd` passes
request.args to `system()` without shellquote — the CVE-2026-69096 advisory
shape is PRESENT in source and UNOBSERVED by the analyzer at this HEAD.
Detection-gap receipt, not an execution verdict.

Unblock condition: producer adds application .uc routing (allowlist/manifest
per the extractor comment) and lifts/parameterizes the query basename gate;
re-run a P2-style probe; then fulfill per the original method with exact
oracle comparison. Security-40 lifts no gate.

Deviation recorded: openvpn/travelmate have no .uc backends at this pin
(lua/js and shell). Evidence: probe-ucode/{VERDICT.md, MANIFEST.yml, logs/,
db/p2-slice (4.3 MB)}; pack build 72.8 s / peak 366 MB. Lane made no commits
or pushes; ledger, codeql-ucode and luci repos untouched.
