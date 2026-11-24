# Claim 038: Init-script exec grants and action argv control

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle (pinned luci + rpcd source + glibc fnmatch witness; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011; rpcd d99f703e4035d03fbcfbada3cb697db346c2b984
- Consumer: none
- Consumer commit: none
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

Demonstrated (source-oracle; no CodeQL producer run for this claim).

- Consumer gate semantics transcribed from pinned rpcd `file.c`: two-stage
  OR-fallback — executable-only match first, then full-cmdline match (not a
  conjunction); fnmatch `FNM_NOESCAPE`, no `FNM_PATHNAME`, so `*` spans `/`
  and spaces; argv unconstrained under executable-only grants; env table
  denied for session-bound exec (L1052–1053); `execv` at L1172
  (`038/matching_order.md`).
- Corpus: 120 ACL JSONs (119 rpcd-format + 1 uhttpd-format excluded), 1045
  grants, 0 parse failures; **173 exec grants** (96 read / 77 write) across
  46 files — read/write split cross-consistent with claim 036.
- Classification: 90 full_pin, 38 executable_only, 44 wildcard_argv,
  1 wildcard_executable. Init-script subset: **40 grants = 30 full-pin +
  10 wildcard_argv** (action argument left to the caller).
- Oracle: 13/13 expected exec grants (travelmate, advanced-reboot, clamav,
  luci-mod-system) + bmx7 string-valued "exec" non-grant reproduced; matcher
  fixtures M1–M8 8/8 via glibc witness; controls PASS. One logged oracle
  revision (M6 fixture literal, M8 citation).
- Gaps: glibc witness only (musl fnmatch not exercised); union-over-groups
  multiset (per-session subset not modeled).
- Evidence: `/root/workspace/work/security-40/038/` (grants.json,
  exec_grants.json, oracle_comparison.json, matcher_receipts.json,
  controls.json, matching_order.md, inventory_stats.json, summary.md);
  orchestrator re-ran `exec_inventory.py` (exit 0, all gates true).
