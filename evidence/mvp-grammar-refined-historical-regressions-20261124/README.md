# Refined grammar historical source regressions

The refined producer-owned grammar candidate used clean pinned LuCI
checkouts for OpenVPN parent `b45584b4e6068b9b096872dd02494a048d869c36`
and fix `e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`, and Tailscale
parent `46cd82328dfb7fbb15961c63f9e674a41cef2500` and fix
`507ab5e45c304543d4111af9a331db0f03be6bcb`. The source-first
expectations and 11 Tailscale controls were frozen before database creation.
The [normalized receipt](receipt.json) records source commits, Git blobs,
hashes, producer patch and extractor identities, exact commands, routes,
extraction rows, SARIF locations and raw artifact hashes. `$RUN`,
`$PRODUCER` and `$CODEQL` stand for recorded absolute paths. Raw artifacts
remain under ignored `work/mvp-grammar-refined-historical-regressions-20261124-b`.

Five fresh databases extracted all 15 selected sources exactly once with
zero errors. The default suite found the exact OpenVPN parent alert at
`luci.openvpn.uc:71:115–132` and no alert in the fix. The separately named
Tailscale query found its exact parent candidate at
`tailscale.uc:164:3–49` and none in the fix. The 11 Tailscale controls
produced only the predeclared candidate at `nested_pos.uc:18:5–51`.
All 40 CodeQL commands exited zero; their phase times sum to 35.934
seconds. Peak RSS was unavailable on this local macOS run.

A setup attempt stopped before any database was created because its run
parent directory was missing; the successful run used a new path. This is
modified-producer source-staged evidence, not merged producer behavior,
Linux release behavior, installed OpenWrt bytes, or general vulnerability
coverage.
