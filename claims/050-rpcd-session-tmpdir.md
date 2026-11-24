# Claim 050: Session-token-derived temporary UCI paths

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-r2w2-q7cw-cfp2 (release-note cited; advisory not publicly retrievable at plan time)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Where does pinned rpcd uci-plugin source construct temporary paths from session tokens, and what visibility/permissions do those paths have in-source?

## Method

Source oracle on rpcd d99f703 uci.c: trace token → directory-name construction, mkstemp/mkdir mode arguments, and cleanup; record exact identities.

## Required evidence

- Construction-chain transcription with source lines
- Mode/permission constants recorded

## Controls

- Positive: token-named directory fixture shape
- Near miss: random-suffix temp name
- Negative: fixed non-token path

## Out of scope

- No cross-session read demonstration
- No runtime permission verdict

## Notes

None.

## Result

Not yet evaluated.
