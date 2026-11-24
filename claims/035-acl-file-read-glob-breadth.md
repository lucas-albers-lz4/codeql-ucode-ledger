# Claim 035: ACL file-read globs spanning path separators

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle method — pinned `openwrt/luci` + `openwrt/rpcd` checkouts and an independent libc fnmatch witness; no CodeQL producer run for this claim
- Producer commit: luci `b2e0be4b46ec0fd43394c081fa7c50657af14011`; rpcd `d99f703e4035d03fbcfbada3cb697db346c2b984` (both clean before and after)
- Consumer: none (no consumer join named in this claim)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-4h7q-j9hv-2536 (luci-app-uhttpd `/*` read exposes /etc/shadow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI ACL `file` read grants contain patterns that match paths outside their apparent directory under rpcd fnmatch semantics (`FNM_NOESCAPE`, no `FNM_PATHNAME`, so `*` spans `/`)?

## Method

Source-derived inventory of every `read.file` pattern in ACL JSON at the pinned luci SHA (application slice manifested separately from the luci-ssl corpus profile), joined against an independent libc fnmatch witness per pattern with concrete cross-directory probe paths.

## Required evidence

- Full pattern multiset with package/path provenance
- fnmatch witness binary/source, compile command and probe-path expectations fixed before running
- Per-pattern match/non-match table for the probe paths

## Controls

- Positive: `/*` matches `/etc/shadow`
- Near miss: `/etc/config/*` matches `/etc/config/wireless` but not `/etc/shadow`
- Negative: literal `/etc/uhttpd.key` does not match `/etc/uhttpd.crt`

## Out of scope

- No claim that any grant is reachable by a live session
- No rpcd runtime execution
- No severity scoring

## Notes

fnmatch-witness-feasibility skill governs the witness; plan-time advisory says rpcd matches with FNM_NOESCAPE and without FNM_PATHNAME — verify against pinned rpcd source, not the advisory text.

## Result

Demonstrated 2026-11-24 (local source-oracle + libc witness; no CodeQL run).

Matcher semantics verified against pinned rpcd source, not the advisory:
`session.c:146-147` matches object and function with `fnmatch(..., FNM_NOESCAPE)`
only — no `FNM_PATHNAME`, no `FNM_PERIOD`, so `*` spans `/`; wildcard set
`session.c:434-436` (`strcspn(str, "*?[")`); only `read`/`write` permission
blocks recognized (`session.c:1071-1073`); table vs array notation
(`session.c` ~1011-1046, array notation grants function = block name); rpcd
loads `INSTALL_PREFIX "/share/rpcd/acl.d"` (`include/rpcd/session.h:37`).

Corpus (enumerated before inventory): 120 acl.d JSON files = 119 rpcd-loaded
(104 application / 9 module / 5 protocol / 1 theme) + 1 foreign LuCI-JS ACL
(`modules/luci-base/root/usr/share/acl.d/luci-base.json`, different schema,
excluded from all decisions). 914 rpcd entries; 3 anomalies recorded (bmx7
bare-string table value skipped by rpcd; dockerman string scope ignored;
foreign luci-base entry quarantined).

Headline: 117 file read grants — 80 literal, 24 trailing-star, 10 star-suffix,
3 bracket/other (hand-fixed before the witness run). 37 breadth-positive
(glob reaches beyond its apparent directory). Three `/*` read grants match all
10 sensitive global probes including `/etc/shadow`, `/etc/uhttpd.key`, `/bin/sh`
(witness-confirmed, orchestrator spot-checked against the pinned JSON):

- `applications/luci-app-dockerman/.../luci-app-dockerman.json:7` — read block, `["list","read"]`
- `applications/luci-app-filebrowser/.../luci-app-filebrowser.json:10` — write block carrying `read`
- `applications/luci-app-filemanager/.../luci-app-filemanager.json:10` — write block carrying `read` (and `exec`)

The historical anchor shape (GHSA-4h7q-j9hv-2536, luci-app-uhttpd `/*` read)
is ABSENT at this pin — uhttpd's read block is uci-only plus one init.d exec
entry — but the shape class persists in the three packages above.

Witness: glibc, C locale, `FNM_NOESCAPE` only; binary sha256
`84375768c2a9504e4f508e3a5cf152c99fb6572360057d90f571a42c231e124e`;
1189/1189 probe expectations matched, 0 mismatches; rebuild byte-identical.
Six-package hand oracle fixed before inventory; exact-multiset comparison
ALL PASS. Controls 4/4 PASS (claim-named positive, near miss, negative).

Evidence: `work/security-40/035/` (summary.md, multiset.json,
classification.json, breadth_table.json, oracle.md/json, hand_fixed.json,
probes/expectations.tsv, witness_output.tsv, witness_results.json,
controls.json, witness_receipts.json, provenance.json, run_pipeline.sh).
Reproduce: `sh 035/run_pipeline.sh` from `work/security-40`. Orchestrator
re-ran the full pipeline 2026-11-24: all gates pass, counts reproduced.

Gaps: glibc only (musl not exercised); cross-directory judged against the
fixed 10-probe set; no reachability or authorization verdict (out of scope);
no CodeQL producer involvement in this claim.
