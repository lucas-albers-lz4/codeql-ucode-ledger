# Claim 039: Write grants to persistence paths

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-v5f9-62c7-cw29 (mounts ACL stale /etc/crontabs/root write → root RCE)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ACL write scopes cover persistence paths (`/etc/crontabs/*`, `/etc/rc.local`, `/etc/init.d/*`, `/etc/hotplug.d/*`, `/etc/profile.d/*`, `/etc/uci-defaults/*`)?

## Method

Source inventory of write.file patterns against a persistence-path list fixed from pinned base-files/procd layout evidence; fnmatch witness for glob patterns.

## Required evidence

- Persistence-write multiset with provenance
- Path-list derivation (pinned package install rules)

## Controls

- Positive: `/etc/crontabs/root` write fixture
- Near miss: `/etc/crontabs/*` glob (witness spans)
- Negative: `/etc/config/network` write (config, not persistence)

## Out of scope

- No RCE claim
- No cron daemon behavior

## Notes

None.

## Result

Not yet evaluated.
