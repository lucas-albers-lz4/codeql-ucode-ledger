# First hosted `luci-base` package-byte attempt: pre-build failure

Manual downstream [run `45503598387`](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45503598387)
used consumer main `8215fc7931fa62309bc2a5dd861ebfa10ba07a24` and the
pinned OpenWrt, LuCI and packages revisions in the merged manual workflow.
Its contract job passed. The experiment job started at 22:43:48 UTC and
failed at 23:43:25 UTC. Its always-run upload retained artifact
`luci-ipk-byte-45503598387-1`; I downloaded it into new ignored
`work/luci-ipk-byte-failure-45503598387/`. The raw run log, configs, source
digests and GNU time files are not committed. [summary.json](summary.json)
records their checked hashes and phase outcomes.
The workflow invoked `tools/installed-byte/run.sh
"$RUNNER_TEMP/luci-ipk-byte"` on Ubuntu 24.04. The script's retained log
contains the source fetch, feed/config and timed build commands; no local
replay of the heavy package build is claimed here.

Source checkout, feeds setup, defconfig, host-tools build and cross-toolchain
build completed. The command labeled `target-probe` then exited 2 in 6.43
seconds. It invoked `make -n package/feeds/luci/luci-base/compile`, but the
pinned OpenWrt `include/toplevel.mk` uses recursive `+` recipes, which GNU
Make executes even in dry-run mode. The retained log reached a generic
`package/libs/libjson-c failed to build` message. This probe omitted `V=s`,
so the underlying dependency error is not visible. No `build.time`, IPK,
prepared/staged comparison receipt or installed-byte result exists. This
run cannot establish the two-file transformation or an installed denominator.

Downstream [PR #163](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/163)
removed the executing probe and kept one verbose serial package build. Its
local shell, comparator and actionlint checks and exact-head hosted tests
passed; it merged as `9018c7633e9dce303d48e2a3ee8d9d78054d03de`.
Manual [rerun `45513606386`](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45513606386)
was dispatched on that main revision. Its result must be inspected
independently; the first run's failure is retained rather than reinterpreted
as a package build or a successful comparison.
