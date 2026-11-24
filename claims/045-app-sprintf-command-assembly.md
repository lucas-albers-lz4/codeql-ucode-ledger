# Claim 045: sprintf/concatenation command assembly before sinks

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` — routing probe P2 at HEAD below; application backends not routed
- Producer commit: `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean; probe-ucode/producer); luci slice pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`
- Consumer: none (no consumer join reached)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 (id/cmd/uid assembled then system())

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned application backends assemble command strings via sprintf/concatenation from request values before a system/popen sink, within same-function name bindings?

## Method

Extend the same-function slice observation to string-building locals feeding sinks; record assembly chain identities; no new flow model.

## Required evidence

- Assembly-chain multiset
- Predeclared oracle
- Binding-limit statement

## Controls

- Positive: sprintf(%s, request.args.x) local then system(local)
- Near miss: sprintf with only literals
- Negative: assembly result never reaching a sink

## Out of scope

- No interprocedural assembly
- No alias/reassignment completeness

## Notes

None.

## Result

Blocked 2026-11-24 — same producer routing gate as claim 041 (codeql-ucode
HEAD `734555a9f56893e89e678cdee63028fc17ea5bc8`, clean; probe P2 receipts in
`work/security-40/probe-ucode/VERDICT.md`): 7/7 application .uc backends
skipped; extractor `file_globs` literal basenames only (extractor.rs
~l.45–64) and RequestArgsExec.ql l.18 `getBaseName() = "luci"` — both
orchestrator-verified.

String-building locals (sprintf/concatenation) feeding system/popen in
application backends are unextracted at this HEAD; assembly-chain identities
were not recorded. No new flow model was added (per method); the supported
same-function name-binding slice remains the only intended observation
surface once routing is unblocked.

Unblock condition and evidence paths: see claim 041 Result. Security-40
lifts no gate.
