# Claim 058: JS rpc.declare UCI set call sites (enumeration only)

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p35r-3323-6g7g class
- 24-package program package 22 precedent

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What is the complete pinned-site multiset of JS UCI set call shapes (rpc.declare with set/commit semantics) in the manifested application set, as source enumeration under the existing execution hold?

## Method

Source enumeration only, re-pinned manifest, receiver/computed-name/shadow controls recorded; no JS execution, no hold lift.

## Required evidence

- Full expected multiset from independent enumeration
- Control classification per site

## Controls

- Positive: literal rpc.declare set call
- Near miss: computed method name (classified, not resolved)
- Negative: rpc.declare read-only call

## Out of scope

- No execution
- No Track A promotion
- Hold remains until separately lifted

## Notes

None.

## Result

Not yet evaluated.
