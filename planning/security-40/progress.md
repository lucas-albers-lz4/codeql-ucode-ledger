# Security-40 progress

Resume point for the [Security-40 program](../security-40-20261124.md).
Update after every claim transition; newest entries first.

## State

- Program opened: 2026-11-24
- Claims created: 035–074 (40); base commit `379b172` on main.
  035–040, 046, 048–050, 053–055, 058–060, 062–074 Demonstrated (29);
  041–045, 047, 051, 052, 056, 057, 061 Blocked (11).
  A/B/C/D/E/F/H/G all closed — Security-40 complete (40/40 evaluated).
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
- Wave 5 C: proc_71c3742a3480 (058 DONE exit 0: Demonstrated — GATE PASS,
    7 uci_write_literal sites, two-pass agreement, 0 uncovered/0 phantom,
    controls 3/3; hold unchanged; tokenizer-revert incident caught by gate);
    proc_f3837a0c8487 (059+060 DONE exit 0: Demonstrated — VERDICT PASS;
    059: 34 eligible chains/65-script manifest; 060: 17 eligible/14-writer;
    controls 3/3 each; second-pass 34/34 + 17/17; packages @07e0d163 blobs,
    working tree never read). 057/061 Blocked (application-ucode routing gate).
    CATEGORY C COMPLETE (058/059/060 Demonstrated).
- Wave 6 F (light source-oracle lanes; heavy slot free): proc_b4e13b5c0d4b
    (062/063/065 DONE exit 0: all Demonstrated — advisory shapes FIXED-IN-SOURCE
    at uhttpd @93b05e0b, fail-no-eligible-instance WITH census; 062 TE
    strcasecmp:272/unknown-501, 063 CL guard :608→400 before :612 cast +
    chunk-reset close :779, 065 reuse guard client.c:139-145 + ubus close
    ubus.c:1161; fix ancestry confirmed; controls 2/2 + POS absence census;
    2nd pass 20/20,30/30,30/30; no DB, peak RSS ~17-18MB; orchestrator re-ran
    3 pipelines exit 0 + spot-checks), log lanes/laneF-uhttpd-parse.log;
    proc_3eaeb1f75860 (064/066 DONE exit 0: Demonstrated — 064 params UNSPEC
    copied verbatim, only type-sensitive consumer guarded ubus.c:638-639 before
    :641 iterator, fix e76736e ancestor, 18 chains/controls 3/3/2nd 18/18;
    066 enumeration complete, BYPASS BRANCH observed error-handler dispatch
    file.c:924 no realm call :920-928 (config-gated, NOT claimed exploitable),
    normal-path fixed 3aa7e1c ancestor, 5 branches/controls 3/3/2nd 4/4;
    orchestrator re-ran 2 pipelines exit 0 + spot-checks + ancestry), log
    lanes/laneF-uhttpd-auth.log; proc_2730fa24420d (067 DONE exit 0: Demonstrated
    — FIXED-IN-PIN, 50 census sites pass A==B 50/50, 29 chains/34 sinks, 169
    citations machine-verified; event zero-guard ubusd_event.c:87-88 before
    :99 calloc/:107 strcpy; fix ancestry d31effb/60e0404/aa4a7ee/f92ffd2;
    controls 3/3 incl real pre-fix blob POS; ubus @24864e78 blobs, dirty tree
    never read; orchestrator re-ran pipeline exit 0 + spot-checks + ancestry),
    log lanes/laneF-ubusd.log. CATEGORY F COMPLETE (062–067 Demonstrated).
- H/G pre-staged (prompts in lanes/, launch after F gates): laneH-px5g (068,
  luci @b2e0be4b clean, libs/luci-lib-px5g/src); laneH-mdnsd-libubox (069 mdnsd
  @defe7ccfd20281b9ef4dfa45437813386a64f8ba — shared HEAD, mdnsd LEFT the feed,
  disclosed; 070 libubox @ff13b89e82e64cdd7853419504e51ec0c7e487e0); laneH-uci-procd
  (071 libuci @66127cd76c5d0bd46d5a90302cc6110f53a4e2f8; 072 procd
  @58eb263d5abe03f8c1280bdfa65a3b052614215d); laneG-shell (073 banip + 074
  travelmate, packages @07e0d163 blobs). libubox/uci/procd pins reachable;
  shared trees dirty → git show blobs. All light source oracles.
- Next: gate F lanes on completion → transition → commit; then H 068–071
  (luci/rpcd source oracles), G 072–074 (shell source oracle). Wave order
  A→B→D→E→C→F→H→G. After 074 closes, design extension waves 075+.
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

### 2026-11-28 — Coverage-gap wave follow-through: grammar census #180 CLOSED, fail-open #181 filed

- Measurement layer executed per the #154-era plan: pinned census of grammar node
  kinds vs dbscheme/AST/flow layers (ucode 83: 54 flow-modeled / 29 audit set / 0
  absent; ucode_markup 101: 53 / 29 / 19 extracted-only).
- Evidence: `evidence/census-180-20261128/` (census.py, census.json, census.md) at
  commit `147d37f1995cc7902f5b0e2a8293d1da62be024d`; producer pin `9166af76…`,
  grammar pin `4a243af…`. Results comment `7243360250`.
- #180 closed; follow-up #181 (fail-open audit of the 29 ucode kinds, 3/3 witnesses
  per rule, standing unmodeled-traversal diagnostic) filed and staffable. markup's
  19 extracted-only kinds stay gated on the #160 dataflow-integration decision.
- No gates lifted; no `path_found`. This run performed no CodeQL execution —
  pinned-source measurement only, safe to run alongside other tracks.

### 2026-11-24 — H/G gated: 068–074 Demonstrated; Security-40 complete (29D/11B)

Refreshed ledger (concurrent MVP advanced 075–090). The H/G source-oracle lanes
(068–074) had completed with full evidence under work/security-40/ but were never
gated. Orchestrator gated all seven: re-ran each run_pipeline.sh (exit 0),
spot-checked pinned blobs (luci/packages/uci pins reachable; 068 x509write.c
make_sign → asn1_add_obj confirmed), merged lane draft Results into claim bodies
(Status → Demonstrated; source pin recorded; README rows flipped).

- 068 px5g signing bounds: Demonstrated (source-shape observability,
  present_in_pin_unfixed; GHSA-jgc3-4q3p-g6xh shape is in the ASN.1 BIT STRING
  wrap, not the correctly-sized RSA signature buffer); controls 3/3.
- 069 mdnsd PTR stack / 070 libubox blobmsg-JSON / 071 libuci parse lifecycle /
  072 procd PATH-env: FIXED-IN-PIN fail-no-eligible-instance WITH census;
  controls 3/3; citations + ancestry verified (069: 32 chains / 169 citations /
  59 census sites).
- 073 banip first-IP / 074 travelmate f_check: FIXED-IN-PIN WITH census;
  controls 3/3 (+ informational controls); residual config-opt-in `first:` /
  unvalidated script_args source shapes documented as observations, not
  exploitability claims.

All source oracles (no CodeQL database; shell/C not extracted by the analyzer).
No gate lifted; no runtime/exploit/vulnerability verdicts. Security-40 final:
29 Demonstrated / 11 Blocked. The 11 Blocked are analyzer coverage gaps ticketed
as ucode#154/#155/#156, openwrt#151, and markup investigation ucode#160. Evidence
local under work/security-40/ (gitignored), matching the 062–067 pattern.

### 2026-11-24 — Follow-up coverage-gap wave filed in both analyzer repos

The 11 Blocked claims trace to two analyzer blind spots (9 application-routing,
2 markup). Filed as `later:` coverage-gap tickets + evidence comments, preserving
each repo's do-not-staff / none-honest discipline (no gate lifted, no production
taint authorized). Public-safe bodies: advisory IDs + pinned public source links;
no internal scratch paths or model refs.

- codeql-ucode#154 — route luci-app application .uc backends (extractor
  file_globs L45–64 + RequestArgsExec.ql L18 basename gate). later,extractor,dataflow.
- codeql-ucode#155 — application-scope fs read/write/exec sink models
  (043/047/051). later,dataflow,queries.
- codeql-ucode#156 — uci.commit → service-restart adjacency query (061).
  later,queries.
- codeql-openwrt#151 — consumer application exec/fs effect + grant coverage
  (043/047/051), gated on ucode#154/#155. later,policy,queries.
- Evidence comments: ucode#50 (application request-args named cases:
  CVE-2026-69096 docker_rpc run_ttyd, tailscale do_login), ucode#53 (application
  uci.set dependency note — no extractable .uc write asserted; travelmate anchor
  is shell), ucode#57 + openwrt#68 (33 .ut census + markup reconciliation),
  openwrt#64 (application fs/exec downstream). Epic audit-trail: ucode#43,
  openwrt#56.
- Reconciliation question (raised on #57/#68) → investigation filed as ucode#160.
  Grounding at producer CURRENT main 9166af76 (2026-11-24, incl. immutable release
  #159): probe pin 734555a9 is STALE (not an ancestor of current main). Current main
  DOES classify .ut (extractor.rs L151-152 Classification::Markup / ut_markup_extension)
  and ships Markup.qll/MarkupCFG.qll/MarkupCreationCFG.qll + markup AST/CFG queries
  via merged PRs #142/#144/#147/#148/#151/#152. So the gap is NOT "AST unmerged."
  #160 RESOLVED. Empirical fresh-pack 33-file run at current main (independently
  audited; evidence/issue160-20261124-markup-33-reconciliation/): all 33 .ut extract
  (classification markup / ut_markup_extension), zero ExtractionErrors, every route
  inconclusive / markup_not_modeled. Source corroboration posted to #160 (comment
  7149464328): MarkupCFG.qll L1 "No data flow is modeled"; docs/markup-cfg.md L16-18
  "Routing remains inconclusive / markup_not_modeled"; all ql/src markup queries are
  *-test.ql; production m3/m4 queries import no Markup. Remaining gap is production-
  dataflow integration (a feature gap), NOT an unmerged AST. 052/056 stay Blocked on
  a current, design-grounded basis. 629a708 unverified (cause unknown). No gate lifted.
- All four tickets OPEN with verified labels + companion cross-links; seven
  comments read back on intended targets. H/G lanes (068–074) still in flight.

### 2026-11-24 — 067 Demonstrated; category F complete; H/G launched

- Lane proc_2730fa24420d (exit 0): source oracle, ubus @24864e78 (2026-06-28;
  shared tree dirty 83, pinned blobs only). FIXED-IN-PIN (fail-no-eligible-
  instance WITH census): peer intake validates before copy (fixed 40-byte
  hdrbuf recvmsg; ubus_validate_hdr ubusd_proto.c:149/152 before alloc; bounded
  body read; blob_parse_untrusted + typed policy). Advisory site
  ubusd_alloc_event_pattern (ubusd_event.c:56): strlen :86 → zero-guard :87-88 →
  wildcard strip :90-93 → LISTEN ACL :96 → calloc :99 → strcpy :107; empty-
  pattern underflow guarded before alloc. 50 census sites (pass A==B 50/50), 29
  chains/34 sinks, 16 local-only dispositions, 169 citations machine-verified.
  Fix ancestry d31effb/60e0404/aa4a7ee/f92ffd2 all ancestors. Controls 3/3 (POS
  real pre-fix blob d31effb^ UNGUARDED historical; NEAR pinned GUARDED; NEG fixed
  hdrbuf). Gaps: pass B in-session procedure not independent model (OAuth 401);
  stale citations rebuilt (R5 43/111 + 5 builder); libubox internals out-of-pin;
  feed drift db20eff not evaluated; summary prose shifted event lines (chains.json
  correct). Orchestrator re-ran pipeline (exit 0) + spot-checked ubusd_event.c:
  86/87/90/96/107 + ubusd_proto.c:149 + ancestry. Claim 067 → Demonstrated.
  CATEGORY F COMPLETE (062–067). H/G (068–074) launched: laneH-px5g,
  laneH-mdnsd-libubox, laneH-uci-procd, laneG-shell (light source oracles).

### 2026-11-24 — 064/066 Demonstrated (uhttpd auth)

- Lane proc_3eaeb1f75860 (exit 0): source oracle, uhttpd @93b05e0b (clean).
  064 FIXED-IN-PIN (fail-no-eligible-instance WITH census): params UNSPEC
  (ubus.c:68) copied verbatim by blob_memdup (:893); only type-sensitive consumer
  blobmsg_for_each_attr (:641) guarded :638-639 (fix e76736e ancestor); 18
  chains, controls 3/3, 2nd pass 18/18; scanner fixed 3× (chain data unchanged).
  066 enumeration complete + BYPASS BRANCH OBSERVED: error-handler check_url
  dispatch uh_invoke_handler file.c:924 (inside is_error_handler:920) has NO
  realm call in :920-928; normal-path shape fixed (3aa7e1c ancestor, :1038
  uh_auth_check_url before :1039). 5 branches (3 checked/1 bypass/1 non_handler),
  controls 3/3 (POS :924 bypass EXISTS), 2nd pass 4/4 + registrations 4/4.
  Bypass reachability config-gated (conf.error_handler matches check_url prefix)
  — recorded as condition, NOT asserted exploitable. Orchestrator re-ran 2
  pipelines (exit 0) + spot-checked ubus.c:68/638-639/641/893 + file.c:920/924/
  941/1038/1039 + ancestry e76736e/3aa7e1c. Source-shape only, no vuln verdict.
  Claims 064/066 → Demonstrated; README + progress updated. 067 (ubusd) running.

### 2026-11-24 — 062/063/065 Demonstrated (uhttpd parse fixed-in-source)

- Lane proc_b4e13b5c0d4b (exit 0): source oracle, uhttpd @93b05e0b (clean).
  All THREE advisory shapes FIXED-IN-SOURCE — fail-no-eligible-instance WITH
  census (049/050/055 pattern). 062 TE case-insensitive (client.c:272 strcasecmp,
  unknown codings 501), 20 entries / 2 chains / 24-site census. 063 negative-CL
  guard (client.c:608 length<0||>INT_MAX → 400 before :612 cast) + invalid-chunk
  reset forces close (:779), 30 entries / 3 chains / parse census 10; fix
  ancestry 2c869c0/9404e6c/b78f518/893fed8. 065 reuse single uh_request_done
  (client.c:125-148), unread-body guard :139-140 forces close before :145 INIT;
  CL.0 precondition :684-685 neutralized; ubus parse-error close ubus.c:1161;
  funnel 22/22, census 12; fix ancestry 15346de/d6205aa/7b1bec4. Controls 2/2
  each (+POS absence census); 2nd pass 20/20,30/30,30/30; no oracle revisions;
  uhttpd clean; no DB (peak RSS ~17-18MB). Orchestrator re-ran 3 pipelines
  (exit 0) + spot-checked guards/closes + ancestry. Source-shape only, no
  runtime/exploit/vuln verdict. Claims 062/063/065 → Demonstrated; README +
  progress updated. F auth (064/066) + ubusd (067) still running.

### 2026-11-24 — 059/060 Demonstrated; category C complete; wave 6 F opened

- Lane proc_f3837a0c8487 (exit 0): source oracle, packages @07e0d163 pinned
  blobs only (working tree dirty, never read); shell not CodeQL-extracted.
- 059: 85 chains → 34 eligible (16 direct/18 indirect), 33 near-miss/18 neg;
  1618-path shell universe, 179 census rows, 65-script manifest. ddns anchor:
  lucihelper has NO eval at pin; machinery in dynamic_dns_functions.sh fed by
  updater.sh:145 (eval "$ip_script" :893 etc.). Controls 3/3; second pass
  34/34 (caught+fixed snort-mgr citation :287/:429); 65/65 blobs sha-verified.
- 060: 19 chains → 17 eligible (14 direct/3 indirect); YAML 7/line-conf 6/
  dnsmasq 1/cron 1/hosts 2. ser2net anchor: options list filtered (tr -cd
  ' -~' :19) but value/accepter/led/gensio paths render UCI WITHOUT newline
  rejection → advisory shape present on device/value paths. Controls 3/3;
  second pass 17/17; 14/14 blobs sha-verified.
- Both bounded declared manifests (not whole-feed); indirect sources declared.
  Orchestrator gate: re-ran both run_pipeline.sh (exit 0, VERDICT PASS);
  spot-checked dynamic_dns_functions.sh:893 + ser2net.init:19/54/63/189.
  Claims 059/060 → Demonstrated; README + progress updated. CATEGORY C COMPLETE.
- Wave 6 F opened: 3 light source-oracle lanes — uhttpd parse (062/063/065),
  uhttpd auth (064/066) @93b05e0b clean; ubusd (067) @24864e78 blobs. Heavy
  slot free. H 068–071 / G 072–074 next.

### 2026-11-24 — 058 Demonstrated (JS rpc.declare UCI-write census)

- Lane proc_71c3742a3480 (exit 0): syntax-only (no CodeQL DB / JS execution;
  JS UCI hold + Track A unchanged). luci @b2e0be4b clean.
- 7 uci_write_literal declares (uci.js order/add/set/delete/apply/confirm +
  wireless.js rename); absence census commit/set_list/etc 0; no literal commit
  declare (commit via apply+confirm). 420-file manifest; 308 grep lines = 7 +
  301 exclusions; 0 uncovered/0 phantom; two independent passes agree on 303
  calls; 127 files sha256-verified. Controls 3/3.
- Incident logged: pass_b tokenizer reverted mid-lane (cause unknown),
  detected by pipeline, rewritten; 2 regressions caught by two-pass agreement
  gate; script sha256s recorded + re-verified. rpcd uci.c taxonomy ref is
  upstream master (disclosed), family split corroborated by pinned uci.js docs.
- Orchestrator gate: re-ran run_pipeline.sh (exit 0, GATE PASS); luci pin
  clean; spot-checked all 7 rpc.declare lines. Claim 058 → Demonstrated;
  README + progress updated.

### 2026-11-24 — Wave 5 C opened (057/061 Blocked; 058/059/060 lanes)

- 057 (request→uci.set) + 061 (uci.commit→restart adjacency) → Blocked:
  application-ucode routing gate (same receipts as 041–045/047/051); only
  luci-base luci.uc routed, application backends (travelmate anchor) skipped.
- 058 (JS rpc.declare UCI-set enumeration under hold) → proc_71c3742a3480,
  source/syntax census like 054; no CodeQL, no JS execution, hold unchanged.
- 059 (shell eval/sh -c config chains; ddns anchor) + 060 (newline UCI→
  line-format; ser2net anchor) → proc_f3837a0c8487, sequential separate
  oracles. packages @07e0d163 reachable; shared/packages working tree DIRTY
  (HEAD 45ad85cb, ~5356 deletions) → lane reads pinned blobs via git show only.
  Shell not CodeQL-extracted (stated honestly); source oracle, no DB.
- Heavy slot free (all C lanes light). README 057/061 → Blocked.

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