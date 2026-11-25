# Security extension — 2026-11-25

Supplement to `security-40-20261124.md`. Security-40 claims 035–074 are closed
(29 Demonstrated / 11 Blocked). This extension uses the eight catalog advisories
not yet claimed, preserves every existing gate, and adds no analyzer grant.

## Scope and pins

| Claim | Advisory | Surface | Pin |
|---|---|---|---|
| 091 | GHSA-jf59-v86x-fwf2 / CVE-2026-55278 | luci-app-lxc ACL + path validation | luci `b2e0be4b46ec0fd43394c081fa7c50657af14011` |
| 092 | GHSA-ggpf-xrph-wg5v / CVE-2026-45767 | luci-app-adblock-fast cron writer | luci `b2e0be4b46ec0fd43394c081fa7c50657af14011` |
| 093 | GHSA-9558-77jp-g3fw / CVE-2026-55608 | EAD `handle_send_a` length underflow | openwrt `4e9642517b48bae612ff10fb72fb9199e559500e` |
| 094 | GHSA-h427-frpr-7cqr / CVE-2025-65123 | ltq-ptm ioctl capability/user-copy | openwrt `4e9642517b48bae612ff10fb72fb9199e559500e` |
| 095 | GHSA-rcc6-v4r6-gj4m / CVE-2026-30873 | jsonpath token string leak | jsonpath `b9034210bd331749673416c6bf389cccd4e23610` (from `package/utils/jsonfilter/Makefile:9`) |

Producer reference: `codeql-ucode` `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`.
Shared working trees are dirty/blobless; lanes read pinned blobs only.

## Waves

- **I — application ACL/injection source oracles:** 091, 092. Application `.uc`
  routing remains blocked under #154; these claims measure pinned source shape,
  not analyzer path coverage.
- **J — native parser/kernel source oracles:** 093, 094. Source census suffices;
  optional C probes must use the single host-wide heavy slot.
- **K — upstream jsonpath token-lifetime oracle:** 095. Disposable blobless
  clone under `work/security-extension-20261125/shared/jsonpath`.
- **L — deferred uhttpd decision packet (investigation only, no claim):**
  GHSA-wvgh-cm54-q6f6, GHSA-83vv-qrc6-h3hx, GHSA-vhx4-3p5q-m59q. The original
  plan defers resource-lifecycle claims until a distinct static-observation
  decision exists. This lane may produce a decision packet and controls
  proposal, but must not create claims, lift gates, or assert `path_found`.

## Rules

1. One heavy CodeQL run host-wide at a time; light source-oracle lanes may run
   in parallel while RAM headroom allows. Record peak memory where supported.
2. No gate lift: JS UCI hold, markup no-dataflow gate, template-argument
   deferral, application-ucode routing gap all remain intact.
3. Fixed-in-pin results require fail-no-eligible-instance plus an explicit
   census and positive/near-miss/negative controls. Never fabricate an instance.
4. Advisory text motivates source shape only; no runtime/exploit/vulnerability
   verdict is inferred from the advisory.
5. Workers write only their claim evidence directories; orchestrator gates,
   updates claim status, README, progress, and commits.
