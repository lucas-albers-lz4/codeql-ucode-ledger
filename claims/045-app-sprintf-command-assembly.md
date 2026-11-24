# Claim 045: sprintf/concatenation command assembly before sinks

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 (id/cmd/uid assembled then system())

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned application backends assemble command strings via sprintf/concatenation from request values before a system/popen sink, within same-function name bindings?

## Method

Extend the same-function slice observation to string-building locals feeding sinks; record assembly chain identities; no new flow model.

## Required evidence

- Assembly-chain multiset
- Predeclared oracle
- Binding-limit statement

## Controls

- Positive: sprintf(%s, request.args.x) local then system(local)
- Near miss: sprintf with only literals
- Negative: assembly result never reaching a sink

## Out of scope

- No interprocedural assembly
- No alias/reassignment completeness

## Notes

None.

## Result

Not yet evaluated.
