# Claim 067: ubusd peer blobmsg parsing bounds

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-cp32-65v4-cp73 / CVE-2025-62526 (ubusd heap buffer overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned ubusd peer message intake, what length/type validation precedes blobmsg copy/allocation, and is the advisory shape observable in-source?

## Method

Source oracle / P1-gated CodeQL C on pinned ubus source (resolve ubusd package pin at execution): transcribe recv → validate → copy chains.

## Required evidence

- Chain multiset with source lines
- ubus pin resolution receipt

## Controls

- Positive: length-derived allocation without observed bound check (if present)
- Near miss: validated length
- Negative: fixed-size control message path

## Out of scope

- No heap overflow execution
- No libubox internals beyond pinned source

## Notes

ubus repo pin is not in the corpus lock; resolve and record it as a new package pin for this claim.

## Result

Not yet evaluated.
