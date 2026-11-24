# Claim 069: mdnsd PTR/reverse-lookup stack buffers

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-mpgh-v658-jqv5 / CVE-2026-30872
- GHSA-7c3j-f7w2-p8f6 / CVE-2026-30871 (both critical stack overflows)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned mdnsd source, what stack buffers receive DNS PTR/reverse-lookup name construction, and what bounds checks are observed in-source?

## Method

Source oracle / P1-gated CodeQL C on mdnsd (resolve package pin at execution): transcribe name-building loops and buffer declarations.

## Required evidence

- Buffer→write-chain multiset
- Pin resolution receipt

## Controls

- Positive: unbounded name copy into fixed stack buffer (if present)
- Near miss: bounded snprintf
- Negative: heap-allocated name path

## Out of scope

- No overflow execution
- No DNS protocol completeness

## Notes

None.

## Result

Not yet evaluated.
