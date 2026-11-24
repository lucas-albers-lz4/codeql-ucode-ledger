# Security-40 progress

Resume point for the [Security-40 program](../security-40-20261124.md).
Update after every claim transition; newest entries first.

## State

- Program opened: 2026-11-24
- Claims created: 035–074 (40); base commit `379b172` on main.
  035–040, 046, 048–050, 053–055 Demonstrated (A+B+D+E complete; 13);
  041–045, 047, 051, 052, 056 Blocked (9); 057–074 Proposed (18);
  no lanes running — next category C (057–061).
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
  - proc_e3a216ca2ae9: 039 upgrade lane DONE (exit 0): Demonstrated —
    orchestrator re-ran build_derivation.py (62 citations verified) +
    persistence_inventory.py (exit 0); 14 derived families, 6 grants
  - proc_4fa69f89a8af: 040 fix lane DONE (exit 0) — Demonstrated; D1–D3
    repaired, gate exit 0 (21/21 oracle, 5/5 controls), base byte-identical;
    corrected 15 read-scope mutating grants / 10 packages.
  - Wave 3 D: proc_ebd4e790d96f (048 DONE exit 0: Demonstrated — orchestrator
    re-ran run_pipeline.sh exit 0, spot-checked main.c 549/551/568/790/810/
    818/826/869 + util.c:199; consumer cgi_download.py decides YES same pin);
    proc_e76dbc5f149e (049+050 DONE exit 0: both Demonstrated — pipelines
    exit 0, compare all_match, e37ed9d ancestry + d99f703 fix subject
    confirmed; source-only, no CodeQL).
    047/051 transitioned Blocked (P2 routing + fs sink-model gap).
  - Wave 4 E: proc_6ae83ddca088 (053+054 DONE exit 0: both Demonstrated —
    pipelines exit 0, 40 render sites / 138 JS sinks byte-verified, 3/3
    controls each; luci + odhcpd pins clean; source/syntax only, JS hold
    unchanged); proc_2b9ba58c6c16 (055 DONE exit 0: Demonstrated
    — orchestrator re-ran run_pipeline.sh exit 0/verify 0, cdfc902 ancestry
    confirmed, 5 sites all uh_htmlescape-encoded; source-only, no CodeQL).
    052/056 transitioned Blocked (markup_not_modeled).
  - P2: DONE (proc_4027700a0cc1, exit 0) — verdict not-routed; receipts
    probe-ucode/{VERDICT.md,MANIFEST.yml,logs/,db/p2-slice}
  - 046 lane DONE (proc_0e309702728b, exit 0): Demonstrated — orchestrator
    re-ran run_pipeline.sh (exit 0), oracle 39/39, source spot-checks,
    producer pin clean. Heavy CodeQL slot free.
- Lanes: isolated `hermes chat` on alibaba/qwen4-max-preview (delegate_task
  codex-pipeline routing hit invalidated openai-codex OAuth; smoke SMOKE_OK).
  -Q logs stay empty until exit; progress visible via artifact dirs.
- Shared pinned checkouts (read-only): work/security-40/shared/{luci,rpcd,
  uhttpd,ubus,libubox,uci,mdnsd,procd,packages,openwrt} (last seven blobless,
  no checkout; openwrt/packages working trees dirty — read pins via git show)
- Next: gate 040-fix / 048 / 049+050 / 053+054 / 055 lanes on completion →
  transition → commit; then wave 5 C (057–061): 058/059/060 viable, 057/061
  routing-blocked. F: 062–066 viable (P1 PASS); 067 needs ubusd probe.
  H: 068–071 per-package probes. G: 072–074 shell source oracle. Wave order
  stays A→B→D→E→C→F→H→G.
- **User directive (2026-11-24, mid-run):** after Security-40 (035–074) is
  complete, find and design **3–10 additional waves** of new high-value
  claims (075+) from uncovered interfaces/advisories, then work through them
  sequentially with the same discipline (pinned scope, source-first oracles,
  controls, orchestrator gating, no gate lifts). Candidate surfaces to
  cross-check against catalog.json for unused advisories: uhttpd TLS/HTTP
  parsing, ubusd ACL/peer-creds/blobmsg, luci session/CSRF/sysauth, rpcd
  iwinfo, netifd/firewall4 ucode, dnsmasq/odhcpd, cgi-io upload/exec,
  attendedsysupgrade/opkg verification, procd service/jail. Design happens
  AFTER 074 closes; record plan addendum + claims before dispatch.

## Pins (plan-time observations; re-resolve at execution)

- luci openwrt-25.12: b2e0be4b46ec0fd43394c081fa7c50657af14011
- openwrt openwrt-25.12: 4e9642517b48bae612ff10fb72fb9199e559500e
- packages openwrt-25.12: 07e0d16305d2b5903b37ad7913e33e18795f81a4
- rpcd PKG_SOURCE_VERSION: d99f703e4035d03fbcfbada3cb697db346c2b984
- uhttpd PKG_SOURCE_VERSION: 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- cgi-io PKG_SOURCE_VERSION: 31cb3c89f02d918d7f17bf62a80c852fc38a1ca1
- CodeQL CLI: 2.27.4 (gh extension)

## Log

### 2026-11-24 — 053/054 Demonstrated; category E complete (waves A/B/D/E done)

- Lane proc_6ae83ddca088 (exit 0), source/syntax only (no CodeQL DB; JS UCI
  hold + Track A unchanged). luci @b2e0be4b clean; odhcpd @5d7be43f clean.
- 053: 40 render sites, completeness scan clean (56 chain-hop lines, 0
  uncovered); odhcpd→leasefile→rpcd→LuCI chain end-to-end; odhcpd statefiles
  escapes non-LDH hostname bytes (503–581), hostname cells %h-escaped; one
  hostname-shaped unencoded scalar render 60_wifi.js:307; dnsmasq writer
  outside odhcpd escape (boundary). Controls 3/3.
- 054: 138 dangerous-render sinks (133 innerHTML + 5 d3 .html); 156 grep lines
  = 138 + 18 exclusions, 0 uncovered; classes literal 58 / encoded 0 / raw 80;
  no encoding helper at any sink arg; rustdesk general.js:447 public_key into
  text + onclick attr. Controls 3/3.
- Integrity: oracle revisions logged; pinned-byte re-reads caught transcription
  errors. shared/openwrt tree dirty (pre-existing deletions) — all openwrt
  evidence via git show blobs. Orchestrator re-ran both run_pipeline.sh
  (exit 0); spot-checked statefiles.c 503/581, luci.js 1394, 60_wifi.js 307.
  Claims 053/054 → Demonstrated; README + progress updated.
- Waves A (035–040), B (041–046), D (047–051), E (052–056) closed:
  13 Demonstrated, 9 Blocked. Next: C (057–061), F (062–067), H (068–071),
  G (072–074). Extension waves (075+) designed after 074 closes.

### 2026-11-24 — 049/050 Demonstrated; category D complete

- Lane proc_e76dbc5f149e (exit 0), source-only (no CodeQL DB). rpcd @d99f703e
  clean; file.c sha 03aae01e, uci.c bc3ca56c.
- 049: 8 file methods; 5 re-resolve+re-authorize (realpath 269 → access 274 →
  *path replace 289; dangling rejected 300); lstat/remove/exec textual-only
  (exec derefs before ACL 859/882<1065 and at execv 1172). Residuals: list
  per-entry stat 709 follows symlinks w/o re-auth; sid==NULL skips ACL
  183–184; fnmatch lacks FNM_PATHNAME. Symlink fix e37ed9d ancestor (verified).
- 050: pin IS fix d99f703 "session: stop naming runtime files after the session
  id" (GHSA-r2w2). 17 sites, ZERO token-named; random 32-hex dirname
  (session.c 334/360) independent of id; modes 0700/umask 0077/O_EXCL 0600;
  cleanup purges enumerated; libuci delta-dir context out-of-pin labeled.
- Controls both: positive fail-no-eligible-instance with census (shapes fixed
  at pin), near-miss/negative PASS; compare all_match true.
- Integrity: lane caught read_file rendering divergence from disk bytes;
  re-derived all citations via nl -ba on sha256-verified bytes (oracle revs
  logged). Orchestrator re-ran both run_pipeline.sh (exit 0); spot-checked
  file.c 183/184/269/274/289/300/709, uci.c 311/1537, session.c 334/360,
  main.c 99/101. Claims 049/050 → Demonstrated; README + progress updated.

### 2026-11-24 — 040 Demonstrated; category A complete (035–040)

- Fix lane proc_4fa69f89a8af (exit 0) repaired D1 (C object registry from
  struct ubus_object .name), D2 (both ucode export forms + parsing repairs),
  D3 (per-call-site literal verb classification). Gate not weakened:
  ubus_inventory.py exit 0, 21/21 oracle checks, 5/5 controls.
- Base multiset byte-identical (337/240/97/55/168; grants.json 4d47fe68,
  ubus_grants.json ec861e55). Join 226 resolved / 111 honestly unresolved.
- Substantive correction: 15 read-scope grants across 10 packages cover
  mutating handlers (prior 8/5). A1 ttyd_start flows via docker.* L11 (rpcd
  fnmatch session.c L143–147 doesn't match docker vs docker.container); nine
  file:exec/file:* read grants → file.c rpc_file_exec_run L1034 → execv L1172
  were invisible to the broken registry. GHSA-cq4h shape under READ scope.
- Orchestrator gate: re-ran ubus_inventory.py (exit 0, ORACLE+CONTROLS PASS);
  spot-checked dockerman acl L10/L11, docker_rpc.uc 289/319/387, session.c
  143–147, file.c 1034/1065/1086/1172. Claim 040 → Demonstrated; README +
  progress updated. Category A (035–040) all Demonstrated.

### 2026-11-24 — 055 Demonstrated (uhttpd URI reflection fixed in-pin)

- Lane proc_2b9ba58c6c16 (exit 0): source-only oracle (P1 C extraction viable
  but exhaustive census left no distinct decision; 0 DB/queries). uhttpd
  @93b05e0b clean.
- 5 request-data→HTML sites all pass uh_htmlescape (utils.c:300–323; escape
  set " & ' < > → &#xNN;). No unencoded URI→HTML emission at pin. 24
  fixed-string error pages negative context; 27 emitter sites enumerated.
- CVE-2018-19630 fixed in-pin: cdfc902 ancestor of HEAD (verified).
- Controls: near-miss/negative PASS; positive FAIL-NO-ELIGIBLE-INSTANCE with
  census (no synthetic). Non-HTML header echoes out-of-scope (F territory).
- Orchestrator gate: re-ran run_pipeline.sh (exit 0, verify 0, citation
  checks PASS); spot-checked utils.c 300/318, cgi.c 79/81–83, file.c 727/729,
  client.c 259. Claim 055 → Demonstrated; README + progress updated.

### 2026-11-24 — 048 Demonstrated (cgi-io canonicalize/ACL order)

- Lane proc_ebd4e790d96f (exit 0): source-oracle only (no CodeQL DB). cgi-io
  @31cb3c89 disposable clone clean; codeql-openwrt @cc5f8630 consumer clean.
- Per-endpoint order transcribed (download canon-before-ACL-before-open with
  in-source fix rationale 542–548; upload part-order-dependent ACL; backup no
  path; exec PATH re-resolution between ACL#1 and ACL#2).
- Consumer answer YES: policy/cgi_download.py already decides GHSA-jw5r /
  CVE-2026-62947 shape at the same pin (C double 6/6); stop condition recorded.
- Controls positive/near-miss/negative pass (near-miss eligible only in exec;
  others fail-no-eligible-instance with census); 24/24 three-way battery.
- Residuals recorded as follow-ups: exec canonicalize/ACL/PATH order, upload
  part-order, symlink/cwd resolution (textual canon; UNKNOWN_FS in consumers).
- Orchestrator gate: re-ran run_pipeline.sh (exit 0); spot-checked main.c
  549/551/568/790/810/818/826/869 + util.c:199; cgi-io pin clean. Claim 048 →
  Demonstrated; README + progress updated.

### 2026-11-24 — wave 4 E opened (052/056 Blocked; 053/054/055 lanes dispatched)

- 052/056 → Blocked: markup extractor gate. codeql-openwrt docs/file-routing.md
  l.20 marks markup `markup_not_modeled`; pack-contract.md l.27/29 forbids
  markup extraction in M0–M3 (seven-case gate remains codeql-ucode work).
  Producer extractor.rs has no .ut routing; ucode_markup grammar hidden at
  init; no markup query pack (m3 taint / m4 request-args). 33 pinned .ut
  templates manifestable but unextracted → XSS-class anchor shapes
  (GHSA-p5pg/c6vf/q335) invisible. Detection gap recorded; no gate lifted.
- 053+054 lane (proc_6ae83ddca088): luci @b2e0be4b lease/UCI render chain
  (odhcpd @5d7be43f lease write → LuCI read → render) + JS dangerous-render
  sink syntax inventory. Source/syntax only; JS UCI hold unchanged.
- 055 lane (proc_2b9ba58c6c16): uhttpd @93b05e0b CGI error/URI reflection
  (CVE-2018-19630); C source oracle, optional P1-pattern CodeQL (heavy slot
  free). 5 lanes now running (040fix, D-cgiio, D-rpcd, E-render, E-uhttpd).

### 2026-11-24 — 039 Demonstrated (pinned-layout derivation closed)

- Upgrade lane proc_e3a216ca2ae9 (exit 0) derived the persistence list from
  openwrt @4e9642517b base-files/procd install rules + shipped layout:
  **14 families, 62 machine-verified citations** (+8/−0 vs analyst baseline;
  scope rule E/P fixed before classification). Shared openwrt HEAD ≠ pin —
  read via `git show <pin>:` only, checkout untouched (honesty recorded).
- Multiset 5 → 6 grants (3 packages): +luci-mod-system `/etc/sysupgrade.conf`
  write L168 (P-class). The two `/*` catch-alls now cover all 14 families
  (witness-verified). grants.json sha 4d47fe68… unchanged.
- Controls pass; 61/61 witness expectations; oracle 6/6 exact (rev3 logged).
  7 persistence-adjacent targets remain out-of-list observations.
- Limitations disclosed: glibc-only witness; rcS/inittab consumers external
  to pin; board.d first-boot gated; uci-defaults one-shot.
- Orchestrator gate: re-ran build_derivation.py (62 citations, exit 0) +
  persistence_inventory.py (exit 0, all gates true); spot-checked base-files
  Makefile L204 (crontabs mkdir) + luci-mod-system.json L168. Claim 039 →
  Demonstrated; README + progress updated.

### 2026-11-24 — wave 3 D opened (047/051 Blocked; 048/049/050 lanes dispatched)

- 047/051 → Blocked: same P2 routing gate as 041–045 (application .uc not
  extracted) PLUS fs read-side (open/read/stat/readlink) and write-side
  (write/rename/mkdir) sinks outside the M4 popen/system model. Unblock
  needs routing extension + fs sink-model decision. Receipts probe-ucode/.
- 048 lane (proc_ebd4e790d96f): cgi-io @31cb3c89 (disposable blobless clone;
  no shared checkout existed) — per-endpoint canonicalize/ACL/open order +
  comparison to codeql-openwrt policy/cgi_download.py oracle (repo clean @
  cc5f863021a099437beb8da66f53207712974a47). CodeQL C optional (P1 pattern).
- 049+050 lane (proc_e76dbc5f149e): rpcd @d99f703e file.c symlink
  re-authorization inventory + uci.c session-tmpdir construction/modes/
  cleanup; sequential, separate oracles/controls. Source-oracle default.
- Heavy CodeQL slot free (046 done). Closure lanes 039up/040fix still running.

### 2026-11-24 — 046 Demonstrated; wave 2 fully closed

- 046 (getFeatures templates): 4 substitution sites beyond the five M4
  methods — L268/275 system (hostapd/wpa_supplicant -v${feature}, closed
  literal array L248–262) + L26/37 helper popen (pkg literal-bound 'netifd'
  at sole call site L313). Provenance: 2 literal + 2 other-named-literal-bound;
  **0 request-derived, 0 config-derived**; getFeatures.call has no request
  param/args (L224); no uci value reaches a command string. 3 fully literal
  commands (L278/294/315).
- GetFeaturesDirectExec.ql: 5 rows exact-multiset match on covered slice;
  helper sites oracle-only by lexical boundary (GetFeaturesPopen 2 rows,
  label-only — disclosed). RequestArgsExec reproduces P2 inventory.
- Controls 4/5: named positive (config-derived) FAIL-no-eligible-instance,
  predicted by fixed oracle, full-file census; no synthetic instance.
  Demonstrated with that limit disclosed (bounded question fully answered:
  absence IS the result).
- Receipts: 6.84 s / 319 MB peak; serial ≤389 MB; re-run byte-identical;
  orchestrator re-run exit 0; routed file sha256 6f9d9729… (path
  modules/luci-base/root/usr/share/rpcd/ucode/luci).
- Wave 2 closed: 041–045 Blocked (routing), 046 Demonstrated. Category B done.

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