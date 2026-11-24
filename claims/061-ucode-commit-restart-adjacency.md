# Claim 061: uci.commit to service-restart adjacency

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
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

Not yet evaluated.
