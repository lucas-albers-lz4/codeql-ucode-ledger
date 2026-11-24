# Preparation receipt

Historical preparation note: the original synthetic comparator here assumed
an `ar` outer IPK. Later inspection of pinned OpenWrt `scripts/ipkg-build`
proved the emitted IPK is a gzip-compressed outer tar. The comparator and
[runbook](RUNBOOK.md) were corrected on 2026-11-24; the older test counts in
this receipt apply only to the superseded prototype and do not verify the
actual package format.

Status: scaffold and helper tests passed; package experiment not run.

## Inputs and source state

Pins were checked against the ledger's pre-existing read-only inspection
checkouts, then a **new full, non-shallow OpenWrt checkout** was cloned under
`work/luci-ipk-byte-linux/openwrt`. No existing checkout was modified.

| Checkout | HEAD | Tree | Dirty | Shallow |
|---|---|---|---|---|
| new `openwrt/` | `4e9642517b48bae612ff10fb72fb9199e559500e` | `328d4df01c038d365176b72753b778e10c3ff413` | no | no |
| source LuCI | `b2e0be4b46ec0fd43394c081fa7c50657af14011` | `34b39b1f15d8a68898d84cab7f48e87f1ba80ac6` | no | no |
| source packages | `07e0d16305d2b5903b37ad7913e33e18795f81a4` | `a6b0fc0935cbfeedb810e6e991b6940f71548ea7` | no | no |

Exact checkout commands were `git clone --no-hardlinks --no-checkout
work/stage6-openwrt work/luci-ipk-byte-linux/openwrt` and `git -C
work/luci-ipk-byte-linux/openwrt checkout --detach
4e9642517b48bae612ff10fb72fb9199e559500e`; combined shell exit status: 0.
The pinned local source checkouts reported empty `git status --porcelain=v1
--untracked-files=all` output. They were read only. The new OpenWrt checkout
also reports empty status; the experimental helper/runbook are siblings of
the project checkout so its pinned clean-state check remains meaningful.

## Machine and run limits

Preparation host: macOS Darwin 24.6.0, arm64. `df -h .` reported 460 GiB
total, 301 GiB used, 121 GiB available at inspection time. This filesystem is
case-insensitive (confirmed by the earlier case probe in the preflight), so
this host was not used for OpenWrt build/configuration. No Linux host resources
or build-tool versions are claimed here. Local command versions were Python
3.15.2, Homebrew GNU Make 4.4.1 (`gmake`) and `/usr/bin/make` 3.81. No `make`,
feed installation, toolchain bootstrap, package build or IPK extraction was
invoked.

The exact helper test command was `/usr/bin/time -l python3 -m unittest -v
test_compare.py`; after the header-assertion review fix, exit 0, seven tests
passed, 0.05 s wall, peak RSS 36,651,008
bytes as reported by macOS `time -l`. `time -l` also printed a denied
`sysctl kern.clockrate` diagnostic; it did not affect the test command's exit
status. The synthetic IPK tests cover a correctly version-transformed header
and rejection of a wrong transformed header. A synthetic `false | tee`
pipeline under the runbook's `bash -o pipefail` wrapper exited 1, confirming
failure propagation. `python3 compare.py --help` exited 0. These test timings are helper
test costs only and say nothing about a Linux package build.

After adding config/feed/path preflight assertions, the exact command
`/usr/bin/time -l python3 -m unittest -v test_compare.py` was rerun on this
preparation host: exit 0, 14 tests passed, 0.05 s wall. `time -l` printed a
denied `sysctl kern.clockrate` diagnostic; it did not affect the test exit.
These tests cover helper controls only and remain no-build evidence.

## Evidence boundary

No prepared package bytes, staging files, package archive or installed root
were observed. The runbook is a manual proposal and its Linux config/feed
resolution and generated paths remain unverified. Therefore there is no
installed-byte conclusion or package-build pass. `compare.py` is a fail-closed
comparison helper, not a builder; only a fresh successful Linux run can
produce its package-byte receipt.
