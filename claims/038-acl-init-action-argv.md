# Claim 038: Init-script exec grants and action argv control

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-66wf-c49f-5whc (`travelmate setup`, `/sbin/ifup` as root from read ACL)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

For pinned exec grants of `/etc/init.d/*` and similar service scripts, does the grant pin the full command line (script + action) or only the executable, leaving the action argument to the caller?

## Method

Source inventory: parse each exec grant string into executable + pinned tokens; classify full-pin vs executable-only; cross-check with consumer `file.exec` gate semantics (executable-first, then cmdline) from pinned rpcd-mod-file source.

## Required evidence

- Grant classification multiset
- rpcd-mod-file matching-order evidence at package pin (source lines)

## Controls

- Positive: executable-only grant fixture (caller chooses action)
- Near miss: full `script restart` pin
- Negative: non-init executable grant

## Out of scope

- No claim that a caller-supplied action is accepted by the init script
- No procd runtime behavior

## Notes

Consumer ubus-file-exec emitters document executable-first matching; reuse that oracle, add the inventory decision.

## Result

Not yet evaluated.
