# MVP bounded corpus v0.3: unetmsg expansion

Status: source-first 99-path manifest prepared before a fresh local run on
2026-11-24. The [manifest](mvp-bounded-corpus-v0.3.json) has SHA-256
`22c0a0434b583913715cdbbd1fbfe0930bb876252fd2823c41cd38bf3a1c870b`.
It retains the 93 v0.2 selected sources and adds all six tracked Ucode
sources in OpenWrt `package/network/services/unetmsg/files/`, for 65 LuCI
and 34 OpenWrt paths. The six proposed installed paths follow
`package/network/services/unetmsg/Makefile` lines 31–33 (`$(CP) ./files/*
$(1)/`). This is source recipe inspection, not an IPK byte comparison.

The isolated clean-checkout verifier matched all 99 source SHA-256 values
and Git blobs and the five recorded exclusions against the pinned LuCI,
OpenWrt and packages-feed commits. The six new route expectations were
derived from their source first lines and suffixes: one Ucode shebang and
five `.uc` extension routes. There are no selected staged-path collisions.
The 17 wifi-scripts paths still assume `CONFIG_WIFI_SCRIPTS_UCODE=y`.

The [fresh macOS source-staged run](../evidence/mvp-corpus-v0.3-local-run/README.md)
subsequently matched every route and successful-file identity once, with
zero extraction errors and zero current-suite SARIF results. It is neither
an installed-byte scan nor the released-producer Linux Gate 6/7 run. The
remaining OpenWrt and packages-feed candidates remain outside this exact
99-path denominator.
