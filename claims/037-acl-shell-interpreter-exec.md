# Claim 037: Shell-interpreter exec grants

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-vj96-f37g-37f6 / CVE-2026-55897 (advanced-reboot read ACL exposes /bin/sh via file.exec)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ACLs grant exec on shell interpreters or busybox (`/bin/sh`, `/bin/ash`, `/bin/bash`, `/usr/bin/env`, `/bin/busybox`) in any scope?

## Method

Source inventory of exec-grant command strings against an interpreter allowlist fixed before inspection; include symlinked/alternative paths only when the pinned filesystem layout evidence supports them.

## Required evidence

- Interpreter-grant multiset with provenance
- Allowlist derivation recorded (pinned busybox config or package manifest, not assumption)

## Controls

- Positive: `/bin/sh` exec grant fixture
- Near miss: `/bin/shutdown` (not an interpreter)
- Negative: `/etc/init.d/uhttpd restart` pinned exec

## Out of scope

- No claim about what an interpreter grant enables at runtime
- No argv injection modeling

## Notes

None.

## Result

Not yet evaluated.
