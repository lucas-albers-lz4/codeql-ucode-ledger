# Claim 063: Content-Length signedness and chunk-size state

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2019-19945 (negative content length → OOB)
- GHSA-p55c-rmhc-qfm5 / CVE-2026-55612 (invalid chunk-length state reset)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What integer types and parse-state transitions govern Content-Length and chunk-size handling in pinned uhttpd, and are the historical signedness/reset shapes present or fixed in-source?

## Method

Source oracle / P1-gated CodeQL C: record strtol/strtoul usage, assignment types, and chunk parser reset paths with source lines.

## Required evidence

- Type/transition table
- Historical-shape presence statement per site

## Controls

- Positive: signed assignment of parsed length (if present)
- Near miss: unsigned parse with overflow check
- Negative: unrelated integer parse

## Out of scope

- No OOB execution
- No full parser model

## Notes

None.

## Result

Not yet evaluated.
