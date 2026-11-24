# Five unreviewed OpenWrt candidates at PR #26933

Read-only source mapping for the five v0.5-unreviewed candidates in the
captured OpenWrt PR #26933 base/head pair. The disposable checkout
`work/incoming-live-pr26933-20261124/source` is clean at head
`bce40f6a15c273778061e8fceced7b9e0f58d99b` (tree
`aad77be60ad2931cfc99f6eb49afd7d72843325e`); base is
`727d8d2f8e5b19a2121e2cf05824e9e5cac35310` (tree
`8396fc6de47e8e208dd52b725d327742ab1e0838`). Each listed path is present
with identical blob and content digest at both commits. Digests below identify
source Git blobs/content only; no package or image was built and installed
bytes were not inspected.

| Candidate path | Git blob / SHA-256 | Recipe, condition, proposed destination | Source-first policy decision |
|---|---|---|---|
| `package/base-files/files/usr/libexec/duid-generate` | `2318239feb7b41dd44d92a0b1b363f5075376d8c` / `b1bd9cd34dc960f22eb65cfb666b3746dae21143f3b83668e26354c4f48a7af0` | `Package/base-files/install` recursively copies `files/*` to package root (`package/base-files/Makefile:172-173`). Proposed `/usr/libexec/duid-generate`; conditional on building/selecting `base-files` for an image. | **Selected; freeze defensibly.** Product package source, destination preserved by the recipe. |
| `package/network/config/netifd/files/lib/netifd/proto-ucode.uc` | `7db61cdb2c16a608c2e13a5d6408d2a17f38ec1d` / `798f452425e7f0dd48774588fec9753c20bfc6ae74622f370ca1eb24cab6e399` | `Package/netifd/install` copies `files/*` to package root (`package/network/config/netifd/Makefile:42-45`). Proposed `/lib/netifd/proto-ucode.uc`; conditional on selecting `netifd`. | **Selected; freeze defensibly.** Product package source with path-preserving copy. |
| `package/network/config/netifd/files/lib/netifd/proto.uc` | `b1a4e2ee1269c439dd4d64eadb74d85a3ccd8657` / `de46a4cf72156d5364ed91d150fd710203d64a8772df03e6ff2cd783490afee6` | Same `netifd` tree-copy recipe. Proposed `/lib/netifd/proto.uc`; conditional on selecting `netifd`. | **Selected; freeze defensibly.** Product package source with path-preserving copy. |
| `package/network/config/wifi-scripts/files/lib/netifd/wireless-macaddr.uc` | `8ff487629760ca239c78fa947b79f01084b5fb7a` / `7f1c7e78220b0062f876bf48f5251bbe02850b634340e2cfc23543da33b9644c` | `wifi-scripts` copies `files/*`; when `CONFIG_WIFI_SCRIPTS_UCODE=y`, it overlays `files-ucode/*` (`package/network/config/wifi-scripts/Makefile:45-50`). Proposed `/lib/netifd/wireless-macaddr.uc`, conditional on package and ucode option. No same-path file exists under `files-ucode/` in this tree. | **Selected; freeze defensibly with the option condition recorded.** No same-destination override was found in the conditional overlay. |
| `package/network/utils/wireguard-tools/files/wireguard.uc` | `fe876ebdbbc8e1b66328c5fcad60acf3680ac810` / `5b895085d72c3feb297d18f378676daae596ab40145113d354ff345d8d8b5d39` | `Package/wireguard-tools/install` installs `./files/wireguard.uc` to `$(1)/lib/netifd/proto/` (`package/network/utils/wireguard-tools/Makefile:55-60`). Proposed `/lib/netifd/proto/wireguard.uc`; conditional on selecting/building `wireguard-tools`. | **Selected; freeze defensibly.** Recipe explicitly installs this source file to the proposed destination. |

## Conclusion

All five can be added as selected source-stage inputs in a next manifest, with
package/option conditions retained as metadata. The recipes establish a
source-to-package staging rule, not configured image membership, runtime use,
or equality of built/installed bytes to these Git blobs. No CodeQL or
extraction result is claimed.

## Reproduction and scope

The candidate identities were read from
`work/incoming-live-pr26933-20261124/full-tree-openwrt.json`; recipes and
overlay presence were inspected in the clean disposable checkout. For each
candidate the report contains the same blob and SHA-256 at base and head.
The v0.5 candidate report identifies these as `unreviewed` because the five
paths were absent from the older v0.5 OpenWrt pin and have no explicit
disposition there, not because they are absent or changed in this PR. This
note records source and recipe review only.
