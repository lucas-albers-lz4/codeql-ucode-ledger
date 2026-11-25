# Pinned LuCI `luci-base` package-byte experiment

Status: **demonstrated for two selected files only**, 2026-11-25. This is a
fresh hosted Linux package build and byte comparison, not a CodeQL scan or a
whole-LuCI installed-file denominator. [GitHub Actions run 45513606386](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45513606386)
completed successfully on consumer `9018c7633e9dce303d48e2a3ee8d9d78054d03de`.
The retained artifact is `luci-ipk-byte-45513606386-1` (artifact ID
`14979253876`). Its raw IPK and 24.8 MB `run.log` are available in that
artifact and were independently downloaded under ignored
`work/luci-ipk-byte-success-45513606386/`; they are not committed here.
This directory preserves the small original comparison receipt, hashes and
two timing files. `SHA256SUMS` relates these copies to the reviewed bytes.

## Inputs and run

- Clean source pins observed by the job: OpenWrt
  `4e9642517b48bae612ff10fb72fb9199e559500e`, LuCI
  `b2e0be4b46ec0fd43394c081fa7c50657af14011`, packages feed
  `07e0d16305d2b5903b37ad7913e33e18795f81a4`. The local retained LuCI
  checkout independently has that commit and the two recorded Git blob OIDs.
- Ubuntu 24.04.5 x86_64; Git 2.56.1, GNU Make 4.3, Python 3.12.3, GCC 13.3.0.
  The run began with 85 GB free and 14 GiB available RAM. `run.log` records
  the tool versions, resource preflight, exact clone/build/comparison commands,
  exit statuses and clean tracked source statuses. Comparator SHA-256:
  `8f71c4f4460b89aeac6d8226ad1c0b679794c70b1e85ae58d29eeceff37b47bd`;
  runner script SHA-256:
  `891e90f98db98ad34ba461c07d931cefcf3ef7c966b2dde70f55cdf8c03a8423`.
- The input config selected x86_64, `CONFIG_PACKAGE_luci-base=m` and IPK
  rather than APK. The final `.config` SHA-256 was
  `e0dc30db2219dfbf503042a7403419f181a6ed38a922e95fb9097bddffecb9ff`;
  `feeds.conf` SHA-256 was
  `52b3e3c257411fc5de4caf088d2fab73a242ca33dfe182088113f217d0239848`.
  The feed list resolved LuCI and packages to local checked-out feeds.
- Host tools: 15:51.33 wall, 534,732 KB peak RSS; toolchain: 29:04.23 wall,
  1,483,316 KB peak RSS. `make -j1 package/feeds/luci/luci-base/compile V=s`
  exited 0 in 1:22.05 wall with 180,804 KB peak RSS (that command only).
  The comparison command exited 0 in 0:00.18 wall with 20,336 KB peak RSS.
  These phases do not constitute a full CodeQL scan time.

## Exact byte results

The generated package was
`luci-base_26.284.22350~8125d12_x86_64.ipk`, with SHA-256
`1a2188f5206ce61c993fdcc451781a06994ae2175b489eef56595858ef22b363`.
Its control metadata reported package `luci-base`, architecture `x86_64`
and version `26.284.22350~8125d12`. The comparator reported `PASS` and no
unexpected file identity. Independent standard-library extraction of the
retained gzip outer tar and `data.tar.gz` confirmed both selected IPK member
hashes and paths:

| LuCI source → IPK member | Source and prepared SHA-256 | Staging and IPK SHA-256 | Observation |
|---|---|---|---|
| `modules/luci-base/ucode/http.uc` → `usr/share/ucode/luci/http.uc` | `68f8a7dffc7bccdfe98956cb3b6e0e087592c86049a2b83d061e5be3585fa5fa` | same | All four byte stages match. |
| `modules/luci-base/ucode/template/header.ut` → `usr/share/ucode/luci/template/header.ut` | `67132f2d1c1cf743f3e4ce11d660a5a2569b461804a63914061fe956171be6c2` | `6fb25a4ddb6038a3ffc207906157db2503cc1bff7dd230fd588776cde329c02e` | Preparation preserves source; staging substitutes the package version and matches the IPK. |

The exact changed line in `header.ut` replaces `{# PKG_VERSION #}` in the
`luci.js?v=` URL with `26.284.22350~8125d12`. That is a three-byte increase;
the version substitution is a build transformation, not an extraction error.
The source Git blob OIDs are `e7f64ae6e9fe00bd1981518927565829a14b11ba`
for `http.uc` and `f23e5e45c88211d3d500193407f9277f1912c784` for
`header.ut`.

The receipt's `elapsed_seconds: 0.142548` covers only its comparison helper.
The package build does not establish bytes for other LuCI packages, OpenWrt
core or the packages feed. The later R3 Linux scan must choose whether to
stage the actual transformed `.ut` bytes or explicitly qualify source-staged
analysis; this result alone does not satisfy R3, Gate 6's full denominator,
or Gate 8.
