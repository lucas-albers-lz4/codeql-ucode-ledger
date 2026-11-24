# Installed-byte package experiment preflight

Status: read-only recipe/tool inspection plus a temporary filesystem case
probe, 2026-11-24. No package build, IPK or installed byte was produced.
Later the source-corrected manual Linux experiment merged through
[codeql-openwrt PR #161](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/161)
at `8215fc7931fa62309bc2a5dd861ebfa10ba07a24`. Hosted
[run `45503598387`](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45503598387)
later failed before package compilation because a `make -n` probe executed
recursive OpenWrt recipes. The retained
[failure receipt](../evidence/mvp-installed-byte-first-linux-failure-20261124/README.md)
records exact phase outcomes. Fix PR #163 merged and manual rerun
`45513606386` is live; neither run has an installed-byte result yet.
The source pins are clean LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, OpenWrt
`4e9642517b48bae612ff10fb72fb9199e559500e` and packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4` in isolated `work/`
checkouts. The OpenWrt checkout has no `.config`, staging tree or pinned
feed setup.

The smallest discriminating LuCI package is `luci-base`:
`modules/luci-base/ucode/http.uc` is a direct-copy source candidate and
`modules/luci-base/ucode/template/header.ut` contains a
`{# PKG_VERSION #}` substitution token at line 10. Pinned `luci.mk` lines
179–187 prepare `ucode/`; lines 214–218 install it under
`usr/share/ucode/luci/` and invoke `SubstituteVersion`; lines 292–295 define
the `.ut` substitution. Compare source Git bytes, prepared build bytes,
package staging bytes and the extracted IPK member for both paths. A
no-pattern `.ut` control should first be checked against all substitution
rules before inclusion. The expected `build_dir/target-*`,
`staging_dir/target-*/root-*` and `bin/packages/*/luci/luci-base_*.ipk`
locations are recipe projections; exact paths require a selected target,
subtarget and package version.

The OpenWrt README lines 34–48 requires a **case-sensitive filesystem** and
GNU Make 4.1+. `/usr/bin/make` is GNU Make 3.81, but
`/opt/homebrew/bin/gmake` is GNU Make 4.4.1, so the version requirement has
a local executable. A temporary two-name probe in ignored `work/` showed
that this volume is **case-insensitive**: `CaseProbe` and `caseprobe` resolved
to one file. That is the immediate local build-environment blocker. A fresh
case-sensitive volume or a Linux runner is required; neither was prepared.
The host reports 16 GiB memory with 64% system-wide free by
`memory_pressure -Q`; roughly 122 GiB disk was free during preflight, but
these are point-in-time resources, not build measurements.

The default OpenWrt feeds file uses moving branches. A build must bind
LuCI/packages feeds to the exact pinned source commits, create a disposable
case-sensitive build tree with run-owned `HOME`, `TMPDIR`, downloads and
output paths, select a concrete target and `CONFIG_PACKAGE_luci-base=m`,
then inspect generated package targets before invoking GNU Make 4.4.1.
`luci-base` has host-build hooks for `po2lmo`/`jsmin` at its Makefile lines
64–77; toolchain and network bootstrap may be substantial. Record the
actual commands, exits, timings and peak memory if a build is attempted.

The lighter packages-feed alternative is `adblock-fast`: Makefile lines
51–57 copies `cli.uc` and `adblock-fast.uc`, then rewrites the latter's
`version:` line. This can discriminate direct and transformed bytes without
LuCI `.ut` behavior, but still requires a configured package build on a
case-sensitive filesystem. Neither recipe alone establishes IPK bytes.

## Next Linux build receipt

Use a fresh Linux run root and record the full OpenWrt, LuCI and packages-feed
SHAs, clean states, Git trees, tool versions and checksums before building.
The three source commits alone do not pin a package result: freeze the target
and subtarget, an archived `.config` or deterministic defconfig inputs,
`CONFIG_PACKAGE_luci-base=m`, feed wiring and package version inputs. Replace
the moving LuCI/packages feed entries with local `src-link` checkouts at the
recorded SHAs, then verify the resolved feed/package paths and resulting
`.config`. Confirm the generated `package/feeds/luci/luci-base/compile`
target before running it. Keep downloads, staging, temporary files and
outputs owned by that run, and retain command exits, wall times and peak
memory where available.

Find exactly one `luci-base_*.ipk` in the configured package output and
extract its data archive into a run-owned directory. Require exactly one
member each at `usr/share/ucode/luci/http.uc` and
`usr/share/ucode/luci/template/header.ut`; inspect the actual IPK format
before extraction. For both members, record SHA-256 of the exact Git source
blob, prepared build file, package staging file and IPK member. The direct
copy rule predicts identical `http.uc` bytes across those points. The
`SubstituteVersion` rule predicts a changed `header.ut` at the package stage;
record the resolved package version and substituted line. Treat either
prediction as unproven until the observed hashes and bytes agree. Missing or
duplicate archives/members, unexpected feed/config/source revisions, or an
unexplained hash mismatch fail the experiment.
