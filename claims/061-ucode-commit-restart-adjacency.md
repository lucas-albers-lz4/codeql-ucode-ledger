# Claim 061: uci.commit to service-restart adjacency

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (routing probe P2)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p35r-3323-6g7g (travelmate auto-login trigger chain)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends place uci cursor commit adjacent to service restart/exec calls in the same function, and what service/action identities are observed?

## Method

Bounded same-function observation of commit + fs.exec/system adjacency; record exact call identities; no causal/runtime claim.

## Required evidence

- Adjacency multiset with source lines
- Predeclared oracle

## Controls

- Positive: commit then /etc/init.d/<svc> restart in one handler
- Near miss: commit with no restart call
- Negative: restart without commit

## Out of scope

- No trigger-chain execution claim
- No interprocedural adjacency

## Notes

None.

## Result

Blocked — producer routing gate (same as 041–045/047/051/057). codeql-ucode
`734555a9…` routes only luci-base `luci.uc`; application ucode backends (the
GHSA-p35r travelmate commit→auto-login anchor scope) are not extracted
("No matching language found, skipping file", probe-ucode/VERDICT.md). The
claimed bounded same-function uci.commit + fs.exec/system adjacency
observation over application backends cannot be produced. Unblock: routing
extension to application .uc + a commit/restart adjacency query with exact
call identities. No causal/runtime claim made. Receipts:
`/root/workspace/work/security-40/probe-ucode/{VERDICT.md,MANIFEST.yml,logs/}`.
