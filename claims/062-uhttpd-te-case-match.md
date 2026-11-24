# Claim 062: Transfer-Encoding matching case sensitivity

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-mcfg-c4r7-pjpf / CVE-2026-55614 (smuggling via case-sensitive TE matching)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd header parsing, how is Transfer-Encoding matched (strcmp/strcasecmp/other), and does the observed comparison decide the advisory shape?

## Method

P1-gated CodeQL C or source oracle on uhttpd 93b05e0: transcribe header comparison call sites with exact functions and arguments.

## Required evidence

- Comparison-site multiset with source lines
- If CodeQL: extraction receipt, query identity, predeclared oracle

## Controls

- Positive: case-sensitive comparison of TE header (advisory shape if present)
- Near miss: case-insensitive comparison
- Negative: unrelated header comparison

## Out of scope

- No smuggling demonstration
- No HTTP state-machine completeness

## Notes

Establish fixed-vs-vulnerable from pinned source, not advisory dates.

## Result

Not yet evaluated.
