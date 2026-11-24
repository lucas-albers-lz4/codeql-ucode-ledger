# Claim 073: banip log-monitor first-IP extraction

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-r6hx-4f83-vp8m (attacker-controlled log fields → wrong-target blocking)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned banip log-monitor source, how is the blocked IP extracted from log lines, and can attacker-controlled fields precede the extracted value in-source?

## Method

Source oracle over pinned banip shell/ucode parse logic: transcribe regex/awk/sed extraction and field ordering assumptions.

## Required evidence

- Extraction-chain transcription with source lines
- Field-order assumption statement

## Controls

- Positive: first-match extraction with attacker-controllable prefix (advisory shape)
- Near miss: anchored field extraction
- Negative: non-log input path

## Out of scope

- No blocking execution
- No firewall runtime claim

## Notes

None.

## Result

Not yet evaluated.
