# Claim 051: Request-controlled destinations into fs.write/rename

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (routing probe P2; application .uc not routed)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jjcx-c284-2qv8 (openvpn traversal + persistence)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends pass request-controlled destination paths to fs.write/fs.rename/fs.mkdir within the supported slice?

## Method

Bounded slice as 047 with write-side sinks; record destination construction and any prefix pinning observed in source.

## Required evidence

- Site multiset
- Predeclared oracle

## Controls

- Positive: request-derived destination
- Near miss: fixed directory + request basename only
- Negative: literal destination

## Out of scope

- No write exploitability
- No ACL verdict

## Notes

None.

## Result

Blocked — producer routing gate (probe P2, orchestrator-verified) plus a
sink-model gap. Security-40 lifts no gate.

- P2 at codeql-ucode `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean):
  application `.uc` backends skipped by literal-basename `file_globs`;
  `RequestArgsExec.ql` l.18 gates `getBaseName() = "luci"`. The manifested
  application set this claim's method requires is not extracted (receipts
  probe-ucode/{VERDICT.md,MANIFEST.yml,logs/}).
- Additionally `fs.write` / `fs.rename` / `fs.mkdir` are outside the M4
  request-args sink model (NamedFsPopenCall / BuiltinSystemCall only), so
  write-side destination flows would not surface even in routed files.
- No source prefix-pinning observation was made (claim method is the bounded
  producer slice).
- Unblock: producer routing extension to application `.uc` + a write-side fs
  sink model decision in codeql-ucode; then re-run this claim's slice.
- Evidence: `/root/workspace/work/security-40/probe-ucode/` (P2 receipts);
  gates verified in producer `extractor/src/extractor.rs` and
  `ql/src/m4/RequestArgsExec.ql`.
