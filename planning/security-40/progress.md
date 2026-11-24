# Security-40 progress

Resume point for the [Security-40 program](../security-40-20261124.md).
Update after every claim transition; newest entries first.

## State

- Program opened: 2026-11-24
- Claims created: 035–074 (40); base commit `379b172` on main.
  035–037 Demonstrated (wave 1A, this commit); 038–074 Proposed.
- Wave 0: P1 DONE — **PASS, full-build-extraction** (probe-c/VERDICT.md):
  15/15 uhttpd .c files, 0 extractor diagnostics, semantic queries verified;
  claims 062–066 viable now; 067–071 need per-package P1-style probes.
  Dependency SHAs were probe-time HEADs — claim lanes must re-pin against
  the corpus lock. P3 fnmatch witness DONE. P2 launching (heavy slot).
- Wave 1: lane A DONE — 035/036/037 gated by orchestrator (full pipeline
  re-runs: controls green, witness 0 mismatches, pinned JSON spot-checks,
  shared pins clean) and transitioned to Demonstrated.
  - proc_95e20daccda0: lane B — claims 038–040 — still running, log
    lanes/laneB.log (no notify; wait/poll via process_manage)
  - P2: ucode application-routing probe (gates 041–046), log lanes/p2.log
- Lanes: isolated `hermes chat` on alibaba/qwen4-max-preview (delegate_task
  codex-pipeline routing hit invalidated openai-codex OAuth; smoke SMOKE_OK).
  -Q logs stay empty until exit; progress visible via artifact dirs.
- Shared pinned checkouts (read-only): work/security-40/shared/{luci,rpcd,
  uhttpd,ubus,libubox,uci,mdnsd,procd,packages,openwrt} (last seven blobless,
  no checkout; openwrt/packages working trees dirty — read pins via git show)
- Next: gate lane B → transition 038–040 → commit; P2 verdict → wave 2
  (category B, 041–046) lanes. Wave order stays A→B→D→E→C→F→H→G.

## Pins (plan-time observations; re-resolve at execution)

- luci openwrt-25.12: b2e0be4b46ec0fd43394c081fa7c50657af14011
- openwrt openwrt-25.12: 4e9642517b48bae612ff10fb72fb9199e559500e
- packages openwrt-25.12: 07e0d16305d2b5903b37ad7913e33e18795f81a4
- rpcd PKG_SOURCE_VERSION: d99f703e4035d03fbcfbada3cb697db346c2b984
- uhttpd PKG_SOURCE_VERSION: 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- cgi-io PKG_SOURCE_VERSION: 31cb3c89f02d918d7f17bf62a80c852fc38a1ca1
- CodeQL CLI: 2.27.4 (gh extension)

## Log

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