# Claim 072: procd PATH/environment filter in service exec

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jw28-hxcm-j934 / CVE-2026-30874 (PATH filter bypass)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned procd service exec source, how is PATH/environment filtered before exec, and is the advisory bypass shape observable in-source?

## Method

Source oracle / P1-gated CodeQL C on procd (resolve pin at execution): transcribe env construction and exec paths.

## Required evidence

- Env-filter transcription with source lines
- Pin receipt

## Controls

- Positive: filter bypassable by observed construction (if present)
- Near miss: fully sanitized env
- Negative: non-service exec path

## Out of scope

- No command execution demonstration
- Low-severity advisory — claim value is the interface observation

## Notes

None.

## Result

Not yet evaluated.
