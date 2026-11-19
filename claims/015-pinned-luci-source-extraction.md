# Claim 015: pinned LuCI installed-source slice extraction

**Status: Demonstrated for three selected source files and one outside-root control.**

## Scope and expected identities

The selected OpenWrt lock identifies LuCI commit
`b2e0be4b46ec0fd43394c081fa7c50657af14011`; a detached independent upstream
checkout supplied the actual repository bytes, not copies of the producer's
test fixture. The following deliberately small `luci-base` slice was
independently selected from the [consumer inventory](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/c45d0c4f36e66e7927d610d5a92c1186bb910f1f/reports/m4-luci-ssl-files.json)
and pinned `luci.mk` installation rules:

| Upstream path beneath `modules/luci-base/` | Reconstructed installed path | SHA-256 |
|---|---|---|
| `root/usr/share/rpcd/ucode/luci` | `usr/share/rpcd/ucode/luci` | `6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e` |
| `ucode/sys.uc` | `usr/share/ucode/luci/sys.uc` | `0380fba5d843a8950bab0ef70982cb40ab8f475e8d267c873e4199a736b55656` |
| `ucode/zoneinfo.uc` | `usr/share/ucode/luci/zoneinfo.uc` | `54162a073660ea65706aa920a10cfbd3ee4d345e1e4ab3bed8a8d56c9cab3863` |

`luci.mk` SHA-256 is `9716c9a7a1c276b867df5887558e2b63b78f7d3695915adb7fcd0a7f0182ed0d`.
This is a reconstruction of selected installed paths, not an actual package
build, running device or complete inventory of `luci-base` or the profile.
The upstream plugin and sys bytes happen to match earlier test fixtures;
`zoneinfo.uc` adds a distinct upstream source. Files outside this selected
slice, markup, generated build outputs and all other corpus packages remain
unknown for this claim.

## Run: 2026-11-18 UTC

Producer `094a163db1138c83820197180501bd7c78bd9051`, consumer inventory
`c45d0c4f36e66e7927d610d5a92c1186bb910f1f`, clean detached checkouts before
setup; LuCI checkout clean at its lock SHA. Lock SHA-256
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
CodeQL 2.27.4, Cargo 1.100.0, Python 3.15.2, Linux. The producer grammar was
pinned at `4a243af329fae2f4ff01e0fc80133cbab8314600`. Build and CodeQL pack
caches were run-owned; the Cargo cache was copied from a previous local cache.
An initially started setup was interrupted before completion to replace the
shared cache with that private copy, then setup was run again.

The [runner](../evidence/015-016/run.py) reconstructed the paths and verified
source digests, created a fresh database with an explicit staged root, captured
[routing](../evidence/015-016/positive-routing.json) before finalization, and
ran the real extraction diagnostics. Exactly those three source identities
were [successfully extracted](../evidence/015-016/positive-extracted.json);
[errors](../evidence/015-016/positive-errors.json) had zero rows. A separate
direct extractor invocation received the valid selected plugin and an
identical valid plugin outside the explicit root. The
[receipt](../evidence/015-016/outside-routing.json) shows one selected and
one `outside_staged_root` exclusion. Both processes used independent output
paths. See [commands and timings](../evidence/015-016/commands-and-timings.json)
for actual argv and exit statuses; prefixes are normalized. The raw local
artifacts remain under ignored `work/`.

GNU `/usr/bin/time` reported 33.24 s wall for the release build with the copied
cache; pack installs took 9.69 s and 7.32 s. Positive database init/index/
finalize took 0.69/0.58/1.64 s wall; diagnostic query executions took 2.15 s
apiece. Individual peak RSS and CPU measurements are in the timing artifacts.
These are small-slice measurements, not full-corpus scan estimates. A clean
extraction does not establish semantic correctness, runtime registration or
security coverage. See [claim 016](016-pinned-luci-status-query.md) for the
specific query dependency tested on the same database.
