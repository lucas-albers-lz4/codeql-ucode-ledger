# Claim 039: Write grants to persistence paths

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source oracle (Python ACL enumeration + pinned base-files/procd layout derivation + glibc fnmatch witness; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011; rpcd d99f703e4035d03fbcfbada3cb697db346c2b984; openwrt 4e9642517b48bae612ff10fb72fb9199e559500e
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

Demonstrated — at pins luci `b2e0be4b…`, rpcd `d99f703e…`, openwrt
`4e9642517b…`. The persistence-path list is now DERIVED from pinned
base-files/procd install rules + shipped layout: **14 families, 62
machine-verified file:line citations** (+8/−0 vs the analyst baseline; the
6 retained families are now pinned-cited). Scope rule fixed before
classification (E = execution persistence; P = upgrade-preservation control).

- 60 file/write grants (56 distinct patterns; grants.json sha256 `4d47fe68…`
  unchanged from the base extraction, byte-identical to claims 035/038).
- **6 persistence-covering write grants from 3 packages**: filemanager +
  filebrowser `/*` write (L10) covering all 14 families per glibc witness;
  luci-mod-system `/etc/rc.local` (init L83), `/etc/crontabs/root` (cron
  L104, mounts L133 — GHSA-v5f9 anchor shape present, no vulnerability
  claim), `/etc/sysupgrade.conf` (L168, P-class, promoted by derivation).
- Controls pass: positive crontabs/root (2 grants); near-miss 5/5
  span/boundary checks; negative network zero tree writes, 9/9 family
  NOMATCH. **61/61 witness expectations** (19 original + 42 new-family
  probes); witness sha256 gated against recorded receipt. Oracle comparison
  6/6 exact, zero violations; oracle rev3 logged (derivation-driven family
  expansion; expectations fixed before re-run).
- 7 persistence-adjacent write targets remain out-of-list observations
  (dropbear authorized_keys L33, firewall.user L16, keepalived.user L17,
  mwan3.user L85, opkg.conf L27, apk/repositories L29, config/unbound L21) —
  evidence the derived list is narrower than the full persistence-adjacent
  surface; not counted in the multiset.
- Limitations (disclosed, not method gaps): glibc-only witness (musl not
  exercised); rcS executor + inittab parser live in procd's external source
  repo (not fetched) — caveats on rc.d/inittab; board.d first-boot gated;
  uci-defaults one-shot; shared openwrt HEAD ≠ pin, read via `git show` only.
- No RCE / cron-daemon / runtime verdicts.
- Evidence: `/root/workspace/work/security-40/039/` (derivation.{md,json},
  build_derivation.py, persistence_multiset.json, oracle_comparison.json,
  controls.json, witness_receipts.json, out_of_list_observations.json,
  summary.md). Orchestrator re-ran `build_derivation.py` (62 citations
  verified, exit 0) and `persistence_inventory.py` (exit 0, all gates true);
  spot-checked base-files Makefile L204 and luci-mod-system.json L168.
