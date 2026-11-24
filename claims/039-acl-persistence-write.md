# Claim 039: Write grants to persistence paths

- Status: Partial
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle (pinned luci source + glibc fnmatch witness; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
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

Partial — inventory and witness complete; the method's pinned-layout
derivation of the persistence path list is outstanding (upgrade lane
dispatched).

- 56 distinct file-write patterns: hand-transcribed set exactly equals the
  mechanical set (empty diff both ways); base extraction byte-identical to
  claims 035/038 (sha256-verified).
- **5 persistence-covering write grants from 3 packages** (luci-mod-system,
  filemanager, filebrowser). 4 of 6 analyst-fixed families covered by
  explicit luci-mod-system patterns (`/etc/crontabs/*`, `/etc/rc.local`,
  `/etc/init.d/*`, `/etc/uci-defaults/*`); `hotplug.d` and `profile.d` only
  via the two catch-all `/*` write grants (filemanager, filebrowser).
- Controls: 19 witness expectations PASS (span/boundary probes); openvpn
  `/etc/openvpn/*` write at L10 non-persistence; dockerman/luci-base `/*`
  read-only; `/etc/config/network` absent tree-wide. Two logged oracle
  revisions (openvpn line 15→10; pattern count 55→56).
- Why Partial: the claim method requires the persistence list fixed from
  pinned base-files/procd layout evidence; the lane used an analyst-fixed
  list without that derivation. Upgrade lane derives it from openwrt
  `4e9642517b48bae612ff10fb72fb9199e559500e` (package/base-files,
  package/system/procd) and re-runs the inventory.
- Gaps: glibc witness only (musl not exercised).
- Evidence: `/root/workspace/work/security-40/039/` (write_grants.json,
  persistence_multiset.json, witness_receipts.json, controls.json,
  out_of_list_observations.json, summary.md); orchestrator re-ran
  `persistence_inventory.py` (exit 0, all gates true).
