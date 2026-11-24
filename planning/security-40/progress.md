# Security-40 progress

Resume point for the [Security-40 program](../security-40-20261124.md).
Update after every claim transition; newest entries first.

## State

- Program opened: 2026-11-24
- Claims created: 035–074 (40); base commit `379b172` on main.
  035–038 Demonstrated (waves 1A/1B); 039/040 Partial (closure lanes
  running); 041–045 Blocked (wave 2, commit `2757d61`); 046 lane running;
  047–074 Proposed.
- Wave 0: P1 DONE — **PASS, full-build-extraction** (probe-c/VERDICT.md):
  15/15 uhttpd .c files, 0 extractor diagnostics, semantic queries verified;
  claims 062–066 viable now; 067–071 need per-package P1-style probes.
  Dependency SHAs were probe-time HEADs — claim lanes must re-pin against
  the corpus lock. P3 fnmatch witness DONE. P2 DONE — **not-routed**
  (probe-ucode/VERDICT.md): application .uc backends skipped by producer;
  041–045 Blocked; 046 feasible within current routing.
- Wave 1: lane A DONE — 035/036/037 gated by orchestrator (full pipeline
  re-runs: controls green, witness 0 mismatches, pinned JSON spot-checks,
  shared pins clean) and transitioned to Demonstrated.
  - lane B DONE (proc_95e20daccda0, exit 0): 038 Demonstrated, 039/040
    Partial — gated by orchestrator (script re-runs + line spot-checks).
  - proc_e3a216ca2ae9: 039 upgrade lane (derive persistence list from pinned
    base-files/procd layout), log lanes/lane039up.log
  - proc_4fa69f89a8af: 040 fix lane (repair D1–D3 mechanical reconciliation),
    log lanes/lane040fix.log
  - P2: DONE (proc_4027700a0cc1, exit 0) — verdict not-routed; receipts
    probe-ucode/{VERDICT.md,MANIFEST.yml,logs/,db/p2-slice}
  - proc_0e309702728b: 046 lane (getFeatures templates; heavy slot), log
    lanes/lane046.log; completion notify armed
- Lanes: isolated `hermes chat` on alibaba/qwen4-max-preview (delegate_task
  codex-pipeline routing hit invalidated openai-codex OAuth; smoke SMOKE_OK).
  -Q logs stay empty until exit; progress visible via artifact dirs.
- Shared pinned checkouts (read-only): work/security-40/shared/{luci,rpcd,
  uhttpd,ubus,libubox,uci,mdnsd,procd,packages,openwrt} (last seven blobless,
  no checkout; openwrt/packages working trees dirty — read pins via git show)
- Next: gate 039-upgrade / 040-fix / 046 lanes on completion → transition →
  commit (wave 1 fully closed); then wave 3 D: 048/049/050 C source-oracle
  lanes + 047/051 Blocked (same routing gate). Routing-blocked set also
  includes 057/061 (C). E: 053/054/055 viable; 052/056 stay inside documented
  markup subset (feasibility check, no gate lift). F: 062–066 viable (P1
  PASS); 067 needs ubusd probe. H: 068–071 per-package probes. G: 072–074
  shell source oracle. Wave order stays A→B→D→E→C→F→H→G.

## Pins (plan-time observations; re-resolve at execution)

- luci openwrt-25.12: b2e0be4b46ec0fd43394c081fa7c50657af14011
- openwrt openwrt-25.12: 4e9642517b48bae612ff10fb72fb9199e559500e
- packages openwrt-25.12: 07e0d16305d2b5903b37ad7913e33e18795f81a4
- rpcd PKG_SOURCE_VERSION: d99f703e4035d03fbcfbada3cb697db346c2b984
- uhttpd PKG_SOURCE_VERSION: 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- cgi-io PKG_SOURCE_VERSION: 31cb3c89f02d918d7f17bf62a80c852fc38a1ca1
- CodeQL CLI: 2.27.4 (gh extension)

## Log

### 2026-11-24 — wave 1B gated (038 Demonstrated; 039/040 Partial + closure lanes)

- Lane B delivered all three; orchestrator re-ran the self-gating scripts
  with correct cwd (038/039 exit 0 all gates true; 040 exit 1 reproducing the
  recorded mechanical FAIL) and spot-checked every headline trace at the
  cited pinned lines (dockerman acl L10/11/15; docker_rpc.uc L289/291/319/
  322/387; ddns L7/sqm L14/upnp L7; sys.uc L153/159; rc.c L318/385;
  luci-mod-system rc.local L83 + crontabs L104/133; filemanager/filebrowser
  `/*` L10).
- 038 Demonstrated: 173 exec grants (96 read/77 write, cross-consistent with
  036); 90 full_pin / 38 executable_only / 44 wildcard_argv / 1
  wildcard_executable; init subset 40 = 30 full-pin + 10 caller-action.
  Matching order: two-stage OR-fallback (executable-first, then cmdline),
  FNM_NOESCAPE, env denied for session-bound exec, execv L1172. Oracle 13/13
  + bmx7 non-grant; fixtures M1–M8 8/8.
- 039 Partial: 56 write patterns hand==mechanical; 5 persistence-covering
  write grants (luci-mod-system, filemanager, filebrowser); hotplug.d/
  profile.d only via `/*` catch-alls. Method requires derivation from pinned
  base-files/procd layout — not done by lane B → upgrade lane
  proc_e3a216ca2ae9 (derive from openwrt 4e964251 package/base-files +
  package/system/procd via git show; re-run inventory).
- 040 Partial: 337 ubus grants (240 read/97 write), 55 objects, 168 pairs;
  8 read-scope grants across 5 packages cover mutating handlers. **A1:
  GHSA-cq4h dockerman shape present under READ scope** (docker:*/docker.*:*
  read → ttyd_start → run_ttyd request.args.id → system). A2 setInitAction
  (basename-guarded, action-whitelisted backend), A3 rc:init (whitelisted).
  Mechanical gate FAILED on 3 identified defects (registry .name vs object
  registration; "return methods;" unparsed; coarse verb classification;
  255/337 unresolved) → fix lane proc_4fa69f89a8af (no gate weakening).
- Dockerman hotspot across waves: 035 `/*` read breadth + 036 exec-in-read +
  040 A1 read-scope mutating exec + 041/042 source shapes unobserved by
  producer. Candidate consolidated finding for codeql-ucode/codeql-openwrt.
- glibc-only witness caveat carries across 035–039 (musl not exercised).

### 2026-11-24 — P2 not-routed; wave 2 closed (041–045 Blocked, 046 dispatched)

- P2 verdict: **not-routed** at codeql-ucode HEAD `734555a9f56893e89e678cdee63028fc17ea5bc8`
  (clean disposable clone probe-ucode/producer). 8-file manifested slice at
  luci b2e0be4b (7 application .uc + luci-base `luci`): SuccessfullyExtractedFiles=1,
  7 application files skipped ("No matching language found, skipping file"),
  ExtractionErrors=0. RequestArgsExec.ql: 7 rows / 5 methods, all luci-base,
  0 application rows — predeclared expectations matched exactly.
- Gates orchestrator-verified in producer source: extractor.rs file_globs
  literal basenames only (comment "without opening '*' routing");
  RequestArgsExec.ql l.18 getBaseName()="luci". 043 additionally: fs.exec /
  fs.exec_direct outside the supported sink set (popen/system only).
- Detection gap (high-value): CVE-2026-69096 shape (docker_rpc.uc run_ttyd
  request.args→system, no shellquote) and tailscale.uc do_login→popen are
  PRESENT in pinned source, UNOBSERVED by the analyzer. Candidate codeql-ucode
  finding — recorded here, not filed as an issue.
- 041–045 → Blocked with full receipts + unblock conditions. 046 lane
  launched (proc_0e309702728b): source inventory of getFeatures substitution
  sites beyond the five M4 methods + GetFeaturesDirectExec.ql within routing.
- Producer build facts: grammar pin 4a243af3 (clone-grammar.sh lowers
  tree-sitter 0.27.1→0.26.8), Cargo.lock a88727b3 matches README pin, rustc
  1.100.0 bootstrap (drift from 1.99.1 noted); pack build 72.8 s / 366 MB peak;
  query 7.75 s / 358 MB peak; db/p2-slice 4.3 MB. Deviation: openvpn/travelmate
  have no .uc backends at this pin.
- Feasibility map for remaining waves: D 048/049/050 viable (C source oracle),
  047/051 routing-blocked; E 053/054/055 viable, 052/056 bounded markup subset;
  C 058/059/060 viable, 057/061 routing-blocked; F 062–066 viable (P1),
  067 ubusd probe; H 068–071 per-package probes; G 072–074 shell source oracle.

### 2026-11-24 — wave 0 P1 PASS; wave 1A (035–037) demonstrated

- P1 verdict: full-build-extraction PASS. Real CMake build (TLS/LUA/UBUS/UCODE
  ON) wrapped by `gh codeql database create --language=c`; 15/15 uhttpd .c,
  221 functions / 1386 calls, 0 diagnostics; semantic smoke on client.c
  header/Content-Length parse sites. Blockers overcome and logged:
  libblobmsg-json ships inside current libubox; ucode mirror is jow-/ucode;
  mbedtls 3.6 LTS (main API-incompatible); liblua.a rebuilt -fPIC; MODULE
  targets need CMAKE_MODULE_LINKER_FLAGS. Caveats: dep SHAs probe-time HEADs
  (re-pin per claim); mbedtls backend vs OpenWrt wolfssl/openssl; no peak-RSS
  receipts; `@kind table` CSV interpretation rejected → BQRS decode used.
- Lane A results (orchestrator re-ran all three pipelines; every gate pass):
  - 035: 117 file read grants, 37 breadth-positive; three `/*` read grants
    (dockerman:7 read block; filebrowser:10, filemanager:10 write blocks)
    match all 10 sensitive probes incl /etc/shadow. uhttpd anchor shape
    ABSENT at pin; shape class persists. Witness 1189/1189, controls 4/4.
  - 036: 96 exec-in-read across 37 packages; 77 exec-in-write across 18.
    travelmate anchor ABSENT from read (6 exec under write); uhttpd still
    carries init.d restart exec under read. Controls 5/5. 167 read-scope
    ubus entries enumerated; mutation verdict deferred to 040.
  - 037: 173 exec-capable; 0 exact interpreter grants + 1 glob-covering
    (filemanager `/*` write exec covers all five allowlist paths).
    advanced-reboot /bin/sh anchor ABSENT. Allowlist derived from pinned
    busybox 1.37.0 bytes (ASH=y, ENV=y, BASH_IS_NONE=y). Witness 220/220,
    controls 5/5.
- Pattern: historical anchor shapes are patched at the 25.12 pins, but the
  shape classes persist in other packages — detection-relevant results.
- P2 launched (ucode application routing; gates wave 2 claims 041–046).

### 2026-11-24 — program opened

- Advisory catalog captured: 41 published advisories + release-note security
  sections (v25.12.6, v24.10.8, v25.12.5, v24.10.4) + historical layer
  (CVE-2018-19630, CVE-2019-12272, CVE-2019-19945, CVE-2019-25015,
  CVE-2020-7248, CVE-2020-7982, CVE-2020-28951). Raw catalog kept in
  `work/security-40/` outside the repo.
- Plan and 40 claim files written; all Proposed.
- User direction: local CodeQL only (no CI); all lanes on the active session
  model (alibaba qwen4-max-preview), thinking level per lane.