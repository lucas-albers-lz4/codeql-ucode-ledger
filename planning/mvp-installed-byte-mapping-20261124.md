# MVP installed-byte mapping: next experiment

Status: read-only package-rule inspection at pinned clean source checkouts,
2026-11-24. This is an implementation guide for MVP-1 R3 and Gate 6, not an
installed-byte result. The bounded selection is
[corpus v0.1](mvp-bounded-corpus-v0.1.md).

Pins: LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`, OpenWrt
`4e9642517b48bae612ff10fb72fb9199e559500e`, packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`. Their isolated source
checkouts under ignored `work/` were clean when inspected. No package build,
IPK, rootfs or installed file was available or compared.

At the LuCI pin, `luci.mk` lines 214–218 copies package `ucode/*` recursively
to `usr/share/ucode/luci/` and then invokes `SubstituteVersion`. Lines
225–228 copy `root/*` directly into the package root. The substitution macro
at lines 286–296 handles `.htm` and `.ut`; the `.ut` patterns substitute
`{# ... PKG_VERSION #}` and selected quoted media/resource CSS or JS URLs.
`modules/luci-base/ucode/template/header.ut` has a version-token candidate;
bootstrap and bmx7 templates have media/resource URL candidates. Thus
`.ut` installed bytes may differ from source, and a projected installed path
alone is insufficient. Ordinary package `ucode/*.uc` and `root/` rpcd files
appear to be direct copies under these rules, conditional on package-specific
preparation and generated inputs; this is a rule inspection, not an output
hash comparison. LuCI `luci-base/Makefile` lines 57–62 and 71–74 do not
replace these file-copy rules for the selected ucode files.

At the OpenWrt pin, `package/utils/cli/Makefile` lines 31–33 uses
`$(CP) ./files/* $(1)/`, mapping its selected `files/usr/share/ucode/cli/`
sources and `files/usr/sbin/cli` to matching package-root paths. This likewise
does not prove the bytes in an actual package.

The smallest discriminating build should use an isolated, configured OpenWrt
buildroot with the pinned LuCI feed, owned `TOPDIR`, `HOME`, `TMPDIR`, download
and build directories. First inspect package-specific `Build/Prepare` and
feed wiring. Build one LuCI package with a plain `.uc`, a `.ut` matching a
substitution pattern and a no-pattern `.ut` control; build `package/utils/cli`
separately. For each file, record the source Git blob/SHA-256, prepared
`PKG_BUILD_DIR` bytes, package staging bytes, IPK member bytes after unpacking
and final installed path. Record actual make commands, exits, phase timing,
peak memory where available, package version/architecture and every mismatch.
Do not count this mapping as done if the package target cannot be configured
or an IPK/rootfs file cannot be obtained. Stage 7's scan may still use a
clearly labeled source-staged corpus while this independent provenance gate
continues.
