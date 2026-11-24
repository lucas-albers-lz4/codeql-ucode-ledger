# Claim 051: Request-controlled destinations into fs.write/rename

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
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

Not yet evaluated.
