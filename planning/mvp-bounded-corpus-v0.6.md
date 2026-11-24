# MVP bounded corpus v0.6: source-staged OpenWrt PR #26933 additions

Status: source-first manifest used by a [failed local v0.6 extraction run](../evidence/mvp-corpus-v0.6-local-run/README.md). The oracle and controls were prepared without inspecting v0.6 analyzer output. The manifest SHA-256 is `9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`. It carries forward v0.5 and adds exactly five reviewed OpenWrt candidates at captured PR #26933 head `bce40f6a15c273778061e8fceced7b9e0f58d99b` (tree `aad77be60ad2931cfc99f6eb49afd7d72843325e`). Total selected: 128; excluded: 13. Route expectations: 93 plain and 35 markup.

The LuCI and packages-feed pins remain unchanged. OpenWrt selected and excluded source identities were independently rehashed from the captured clean checkout at the new head. The five additions are:

| Source | Proposed installed path | Package/option condition | Recipe | Route expectation |
|---|---|---|---|---|
| `package/base-files/files/usr/libexec/duid-generate` | `/usr/libexec/duid-generate` | package selected: base-files for an image | `Package/base-files/install:172-173` | `ucode_shebang` |
| `package/network/config/netifd/files/lib/netifd/proto-ucode.uc` | `/lib/netifd/proto-ucode.uc` | package selected: netifd | `package/network/config/netifd/Makefile:42-45` | `ucode_shebang` |
| `package/network/config/netifd/files/lib/netifd/proto.uc` | `/lib/netifd/proto.uc` | package selected: netifd | `package/network/config/netifd/Makefile:42-45` | `ucode_extension` |
| `package/network/config/wifi-scripts/files/lib/netifd/wireless-macaddr.uc` | `/lib/netifd/wireless-macaddr.uc` | package selected: wifi-scripts and CONFIG_WIFI_SCRIPTS_UCODE=y; no same-path files-ucode override in captured tree | `package/network/config/wifi-scripts/Makefile:45-50` | `ucode_extension` |
| `package/network/utils/wireguard-tools/files/wireguard.uc` | `/lib/netifd/proto/wireguard.uc` | package selected: wireguard-tools | `package/network/utils/wireguard-tools/Makefile:55-60` | `ucode_shebang` |

Each new manifest row also records its Git blob and SHA-256. These are pinned source bytes. The recipes support proposed package staging paths; configured image membership, runtime use, and equality of built/installed bytes to the Git blob are not established. `installed_bytes_verified` is false for every row.

The source-first expected identities and route decisions are frozen in [the oracle](../evidence/mvp-corpus-v0.6-source-first-oracle.json); [independent controls](../evidence/mvp-corpus-v0.6-controls.json) preserve the competing wifi-shell near miss and add the five new eligible positive identities. These expectations were prepared without inspecting the first v0.6 CodeQL output.

## Source revision delta review

Rehashing all prior OpenWrt identities found 30 byte changes: 29 of 46 previously selected identities and the one previously excluded identity changed between the v0.5 pin `4e9642517b48bae612ff10fb72fb9199e559500e` and captured head. The source-first oracle lists every path with old/new blob and SHA-256, current first line, and selected/excluded route disposition. All selected changed paths retain their previous route expectation, checked against the current first line and file suffix; changed `.uc` files remain extension-routed unless a Ucode shebang is present. The excluded competing shell file remains excluded. This delta is separate from the five additions: their byte stability between the PR base and head does not imply stability against the older v0.5 pin.

The first control draft incorrectly carried forward a v0.5 near miss that expected `wireguard.uc` to be absent. That file is selected at the v0.6 pin; independent review removed the stale negative before any v0.6 CodeQL output. The corrected control digest is recorded in the run preflight.

Independent pre-run review also found five leading slashes in proposed staged destinations and stale hashes in carried-forward positive controls. The manifest now stores stage-relative destinations, the controls match the captured head, and the corrected manifest/oracle/control digests were frozen before any v0.6 analyzer output. The earlier draft digests are not run inputs.

The source verifier also caught the excluded shell row retaining its older-pin digest despite the current controls using the new blob. The manifest and oracle were corrected to the captured head and reverified before the first v0.6 run. Current frozen SHA-256 values: manifest `9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`, oracle `c30bbd8108c44519b8f63f0861d14dbbb5ef8f533f09a20b79942181ec360c64`, controls `cb6bc3beb59a21e83c9c906ec2d77019b04513d8f93f467f502485259c625c93`.

A full oracle-to-manifest projection check caught the same five absolute destinations in extra oracle fields. Those were corrected to stage-relative paths before analyzer output; the final oracle digest above includes that correction.

The first fresh local run matched all 128 route decisions but stopped after diagnostic queries: 126 exact successful identities and four parse diagnostic rows on two changed wifi sources. No suite or SARIF result was produced. See the linked failure receipt for exact locations and phase timings.
