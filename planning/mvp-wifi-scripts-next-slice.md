# Next bounded OpenWrt slice: wifi-scripts

Status: initial source-first selection, corrected and run on 2026-11-24. The
[initial 17-file selection](mvp-wifi-scripts-next-slice.json) has SHA-256
`f3fb3f2c53f7f905d3f8a4a612300d9a5ab2a6ef32874b15d2d3dcd93949c41e`.
Its selected bytes and Git blobs were checked against the clean isolated
OpenWrt source checkout at
`4e9642517b48bae612ff10fb72fb9199e559500e`. Its initial route expectation
was wrong for three `.uc` files with Ucode shebangs: the extractor checks the
shebang before the extension. The original selection is retained for
provenance; use the [corrected source-first oracle](../evidence/mvp-wifi-scripts-extraction-20261124/source-first-oracle.json)
for later runs. The fresh [route and extraction result](../evidence/mvp-wifi-scripts-extraction-20261124/README.md)
matched that corrected oracle. No package build or installed-byte comparison
was performed for this slice.

This package contributes 15 tracked `.uc` files and two Ucode-shebang
extensionless or `.sh` scripts. `package/network/config/wifi-scripts/Makefile`
lines 44–50 first copies `files/*` and then copies `files-ucode/*` only when
`CONFIG_WIFI_SCRIPTS_UCODE=y`. In that configuration, the Ucode-shebang
`files-ucode/lib/netifd/wireless/mac80211.sh` overwrites the shell script
at the same installed path from `files/lib/netifd/wireless/mac80211.sh`.
The source-first oracle records that competing shell source separately.
Without a frozen config and package output, neither variant can be called
the installed bytes.

The next package or Linux run should freeze the config value,
package Makefile/source SHA, all 17 source hashes and proposed installed
paths. Use the corrected oracle's 12 extension and five shebang routes as its
expectation; compare actual package staging or IPK bytes where possible.
Revisit route/extraction only for a relevant producer, source or installation
delta rather than repeating the completed local slice. This slice is a
natural follow-on
to [corpus v0.1](mvp-bounded-corpus-v0.1.md), not part of its 76-file
denominator until a new versioned manifest adds it.

## Paired package-byte decision (2026-11-25 preflight)

At the same clean OpenWrt commit, source review of the package recipe and
`Config.in` selects a paired Linux IPK experiment: build `wifi-scripts` once
with `CONFIG_WIFI_SCRIPTS_UCODE=y` and once with it unset, keeping the target,
package, source revision and all other resolved configuration fixed. The
corrected oracle projects 17 Ucode-looking members in the enabled package
and seven common Ucode members in the disabled package. The distinguishing
`lib/netifd/wireless/mac80211.sh` should match the Ucode-shebang source
SHA-256 `f7d6ae091777a8eb77ba55c2c1f09bf8caff1a4364dc6de4f19a1ecb322801aa`
when enabled and the shell source SHA-256
`5f87f07cca56b20b0cf08cf02711c1c4fc4ddbbb17de7c8780282625c8d3be07`
when disabled. These are source predictions, not observed package bytes.

The build must resolve and compare both final configs before expensive
toolchain work, then retain source Git blobs, stage paths, exact IPKs and
member byte hashes separately for both variants. A missing or duplicate
member, changed source/config, ambiguous archive, extra Ucode-looking member,
or source/stage/IPK mismatch fails the experiment. The existing LuCI
installed-byte build is a process precedent only; it does not establish
wifi-scripts bytes or a CodeQL scan. A successful pair would add a conditional
package-member slice to Gate 6, with an explicit config denominator.
