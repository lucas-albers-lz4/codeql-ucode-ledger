# MVP bounded corpus v0.4: packages-feed base exporter

Status: source-first 111-path manifest prepared before a fresh local run on
2026-11-24. The [manifest](mvp-bounded-corpus-v0.4.json) has SHA-256
`1e25cf9c2adc40c854502fed8d1ccc0977a3c4825d6ee4a1c0a543ffe0a76699`.
It retains the 99 v0.3 paths and adds the 12 tracked Ucode files installed
by the **base** packages-feed `prometheus-node-exporter-ucode` package:
11 `files/base/*.uc` modules and `files/metrics.uc`. The recipe at
`utils/prometheus-node-exporter-ucode/Makefile` lines 33–35 installs the
base files under `usr/share/ucode/node-exporter/`. Its eight `files/extra`
collectors have separate optional packages and are recorded as exclusions
from this base-package denominator.

All 111 selected and 13 excluded source identities were checked against
clean exact-pinned LuCI, OpenWrt and packages-feed checkouts. Each selected
SHA-256 and Git blob matched; staged paths are unique. The 12 new route
expectations came from the source and producer routing order: 11 `.uc`
extension plain routes, and `metrics.uc` as markup-inconclusive because it
begins with a markup tag. The 17 wifi-scripts paths still assume
`CONFIG_WIFI_SCRIPTS_UCODE=y`.

The [fresh local macOS source-staged run](../evidence/mvp-corpus-v0.4-local-run/README.md)
matched all 111 route and successful-file identities with multiplicity, had
zero extraction errors and zero current-suite SARIF results. This is a
source-staged denominator, not a configured package/IPK byte comparison or
released-producer Linux Gate 6/7 result. Remaining core/packages-feed
candidates, including the eight optional collectors, stay outside this
111-path denominator.
