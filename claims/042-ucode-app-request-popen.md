# Claim 042: request.args to popen() in application ucode backends

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` — routing probe P2 at HEAD below; application backends not routed
- Producer commit: `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean; probe-ucode/producer); luci slice pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`
- Consumer: none (no consumer join reached)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 class
- M4 luci-base getSwconfigFeatures/getRealtimeStats precedent

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned application ucode backends pass request-controlled values to `popen()` within the supported same-function slice, and with what quoting context?

## Method

Same method as 041 with popen sink; reuse M4 shellquote observation fields; manifested application file set.

## Required evidence

- Predeclared site multiset
- Query receipts
- Quoting-context classification per site

## Controls

- Positive: unquoted request value into popen template
- Near miss: shellquote complete-argument site
- Negative: literal popen command

## Out of scope

- Same limits as 041
- No global flow

## Notes

None.

## Result

Blocked 2026-11-24 — same producer routing gate as claim 041 (codeql-ucode
HEAD `734555a9f56893e89e678cdee63028fc17ea5bc8`, clean; probe P2 receipts in
`work/security-40/probe-ucode/VERDICT.md`): 7/7 application .uc backends
skipped ("No matching language found, skipping file"); extractor
`file_globs` literal basenames only (extractor.rs ~l.45–64) and
RequestArgsExec.ql l.18 `getBaseName() = "luci"` — both orchestrator-verified.
RequestArgsExec.ql over the manifested slice: 7 rows / 5 methods, all
luci-base (getSwconfigFeatures→popen ×1 shellquote,
getSwconfigPortState→popen ×1 shellquote, getRealtimeStats→popen ×2
shellquote), 0 application rows; predeclared expectations matched exactly.

Bounded source observation (P2, pinned luci `b2e0be4b…`): tailscale.uc
`do_login` passes request.args to `popen()` — present in source, unobserved
by the analyzer. Quoting-context classification for application popen sites
requires the supported slice; not performed at this HEAD.

Unblock condition and evidence paths: see claim 041 Result (identical gate,
identical probe). Security-40 lifts no gate. Deviation: openvpn/travelmate
have no .uc backends at this pin.
