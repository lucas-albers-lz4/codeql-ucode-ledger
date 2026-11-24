# MVP bounded corpus v0.2: conditional wifi-scripts expansion

Status: source-first preparation for MVP-1 Gate 6, 2026-11-24. The exact
[93 selected and five excluded identities](mvp-bounded-corpus-v0.2.json)
have manifest SHA-256
`7c3e055ece88c13684efb100c2c248b35a448027d836697063c5d79a32a200fe`.
The manifest was prepared from separate prior local slices. A later
[fresh combined local source-staged run](../evidence/mvp-corpus-v0.2-local-run/README.md)
matched it; neither is a Linux scan or Gate 6 pass.

The pinned source commits are LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, OpenWrt
`4e9642517b48bae612ff10fb72fb9199e559500e`, and packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`. The selection combines
65 LuCI paths, 11 OpenWrt CLI paths and the 17 OpenWrt wifi-scripts Ucode
paths from the [corrected source-first oracle](../evidence/mvp-wifi-scripts-extraction-20261124/source-first-oracle.json).
The latter 17 are selected only under `CONFIG_WIFI_SCRIPTS_UCODE=y`; the
competing shell source copied first at `lib/netifd/wireless/mac80211.sh` is
recorded as excluded under that condition. Four LuCI census exclusions remain.
No packages-feed file is selected yet.

The selected source identities are unique. The source verifier checked all
93 source SHA-256 values and Git blobs, the five excluded source identities,
and clean exact-pinned isolated checkouts. Its command was:

```sh
python3 -B scripts/verify-mvp-corpus-source.py \
  --manifest planning/mvp-bounded-corpus-v0.2.json \
  --luci work/stage6-luci --openwrt work/stage6-openwrt \
  --packages work/stage6-packages
```

It exited 0 with 65 LuCI and 28 OpenWrt selected paths. Prior separate local
extraction evidence reports each selected source once and zero errors. The
expected route classes are 59 plain and 34 markup-inconclusive; successful
extraction of a markup path does not establish modeled markup support. This
source check does not reauthenticate those separate runs.

The combined macOS run selected all 93 once, matched 59 plain and 34
markup-inconclusive routes with multiplicity, reported 93 successful
extraction identities and zero errors, and produced zero default-suite SARIF
results. Its nine phase times sum to 23.106 seconds, without peak RSS. This
does not establish a Linux cost or a security-negative result.

Next, freeze the wifi-scripts configuration and run this exact aggregate in
one fresh isolated Linux database with the released producer. Compare each
route, extracted identity, diagnostic and SARIF result with multiplicity.
Separately compare package staging/IPK or rootfs bytes to source; proposed
installed paths in this manifest are not byte-verified. The remaining core
and packages-feed candidates stay outside this 93-path denominator.
