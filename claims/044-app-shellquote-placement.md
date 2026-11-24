# Claim 044: shellquote placement in application command templates

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-pm9w-522m-8rrh (openvpn generateKey cl_meta command injection)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned application command templates reaching system/popen, where does `shellquote` appear — complete-argument position, executable position, or absent — under the M4 barrier definition?

## Method

Inventory shellquote call sites feeding command strings in the manifested application set; classify placement per the documented M4 barrier context; do not extend the barrier model.

## Required evidence

- Placement multiset with source lines
- M4 barrier definition cited by pack digest

## Controls

- Positive: absent-quote advisory shape
- Near miss: complete-argument quote (barrier context)
- Negative: quoted executable selection (still injection candidate per M4)

## Out of scope

- No global sanitizer claim
- No barrier promotion

## Notes

None.

## Result

Not yet evaluated.
