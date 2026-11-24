# Claim 036: Exec rules misplaced into read ACL scope

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-66wf-c49f-5whc (travelmate read ACL carries `/etc/init.d/travelmate setup` and `/sbin/ifup` exec)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ACL files place `exec` entries inside `read.file` (or read-scope ubus grants whose methods mutate), and what commands do those entries pin?

## Method

Source inventory over pinned ACL JSON: enumerate scope → file → permission triples; classify exec-in-read vs exec-in-write; record exact command strings.

## Required evidence

- Complete exec-in-read multiset with file/line provenance
- Independent hand-transcribed expected cases from at least three named packages before comparison

## Controls

- Positive: travelmate-shaped read-scope exec entry (synthetic fixture mirroring the advisory shape)
- Near miss: same command correctly under write scope
- Negative: read-only file entry with no exec permission

## Out of scope

- No authorization-violation verdict for any real grant
- No live session test

## Notes

Consumer policy oracle already models specific exec grants; this claim is the cross-package inventory decision, not a duplicate of an existing emitter.

## Result

Not yet evaluated.
