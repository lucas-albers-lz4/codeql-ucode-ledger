# Claim 036: Exec rules misplaced into read ACL scope

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle method — pinned `openwrt/luci` + `openwrt/rpcd` checkouts with a hand-transcribed oracle and synthetic fixtures; no CodeQL producer run for this claim
- Producer commit: luci `b2e0be4b46ec0fd43394c081fa7c50657af14011`; rpcd `d99f703e4035d03fbcfbada3cb697db346c2b984` (both clean before and after)
- Consumer: none (no consumer join named in this claim)
- Consumer commit: none
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

Demonstrated 2026-11-24 (local source-oracle method; no CodeQL run).

Semantics verified against pinned rpcd source: only `read`/`write` permission
blocks recognized (`session.c:1071-1073`); table notation permits any function
name including `exec` under either block (~1011-1024); array notation forces
function = block name (~1037-1046), so `read.file` arrays can never be exec
grants; the permission block gates which users receive the grants
(`rpc_login_test_permission`, ~940-989) and write implies read (985-987) — an
`exec` entry under `read` is delivered to read-only users of that group
(source observation; no authorization verdict). Function matching is fnmatch
`FNM_NOESCAPE` (`session.c:146-147`), so function `"*"` covers `exec`
(predeclared decision rule).

Corpus: same complete enumeration as claim 035 — 119 rpcd-loaded ACL JSONs +
1 foreign excluded; 914 rpcd entries; 3 anomalies.

Headline: 96 exec-in-read entries across 37 packages; 77 exec-in-write across
18 packages (complete multisets with file/line/group/command provenance in
classification.json). The historical anchor (GHSA-66wf-c49f-5whc, travelmate
read-scope `/etc/init.d/travelmate setup` + `/sbin/ifup` exec) is ABSENT from
read at this pin — travelmate's 6 exec entries are all under write. The shape
is nonetheless widespread: luci-app-uhttpd still carries
`/etc/init.d/uhttpd restart` exec under read; luci-mod-status (13 entries incl.
`/bin/dmesg -r`), luci-mod-network (11 incl. `/bin/ping`, `/bin/traceroute`),
luci-app-ocserv (5), luci-app-unbound (5) among the 37 packages.

Read-scope ubus parenthetical: raw multiset of 167 read-scope ubus entries
enumerated (ubus_read_multiset.json); the mutating-method verdict is claim
040's decision per the plan's category A split — explicitly deferred, not
silently dropped.

Controls 5/5 PASS: claim-named positive (travelmate-shaped read-scope exec →
2/0), near miss (same commands under write → 0/2), negative (read-only
list/read → 0/0); labeled extras: wildcard function `["*"]` under read counts
exec-capable; array notation `read.file ["/bin/sh"]` never exec. Six-package
hand oracle fixed before inventory; exact-multiset and placement comparisons
ALL PASS; fixtures run through the same parser/classifier.

Evidence: `work/security-40/036/` (summary.md, classification.json,
multiset.json, ubus_read_multiset.json, controls.json, fixtures/,
oracle.md/json, comparison_entries.json, provenance.json, run_pipeline.sh).
Reproduce: `sh 036/run_pipeline.sh` from `work/security-40`. Orchestrator
re-ran 2026-11-24: files=120 entries=916 (914 rpcd + 2 quarantined foreign)
anomalies=3, all comparisons and controls pass, 96/77 reproduced.

Gaps: ubus mutation verdict deferred to 040; no authorization-violation
verdict for any real grant; no live-session test; no emitter join
(consumer-policy-oracle duplication note honored).
