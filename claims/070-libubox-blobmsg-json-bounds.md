# Claim 070: libubox blobmsg JSON serialization bounds

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2020-7248 (tagged binary JSON serialization stack overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned libubox blobmsg_json source, what buffer management governs serialization of nested/tagged data, and is the historical stack-overflow shape present or fixed?

## Method

Source oracle / P1-gated CodeQL C on libubox (resolve pin at execution): transcribe serialization buffer growth and recursion depth handling.

## Required evidence

- Buffer-management transcription with source lines
- Historical-shape presence statement

## Controls

- Positive: fixed stack buffer with recursion (if present)
- Near miss: realloc-grown buffer
- Negative: non-recursive scalar path

## Out of scope

- No overflow execution
- No JSON parser completeness

## Notes

None.

## Result

Not yet evaluated.
