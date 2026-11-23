# Package 7 source-only inventory: selected profile markup inputs

Prepared before any Package 7 CodeQL execution or output inspection. This is a
source syntax inventory, not an extraction or CFG result.

## Pins and selection

- [Producer contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/6010ff2c0f101f7629c6fe117a421f671c311a2b/docs/markup-cfg.md): `6010ff2c0f101f7629c6fe117a421f671c311a2b`, inspected in a clean disposable checkout.
- [LuCI source](https://github.com/openwrt/luci/tree/b2e0be4b46ec0fd43394c081fa7c50657af14011): `b2e0be4b46ec0fd43394c081fa7c50657af14011`, inspected in a clean disposable checkout.
- Profile: `luci-ssl-25.12`, as recorded by the consumer inventory and
  `claims/025-mixed-profile.md`. The 12 markup entries are the eleven `.ut`
  templates and `uhttpd.uc` below. Selection paths and prior source hashes
  come from the [consumer manifest](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/evidence/markup-profile-0a6612f/manifest.json);
  each local source file's bytes and hash were independently read from the
  clean pinned LuCI tree. Source paths map to installed paths by the profile's
  recorded inventory. No build or install transformation was performed here.
- Contract: producer `docs/markup-cfg.md`. `MarkupCFG::isCovered` only admits
  roots limited to raw text, simple identifier expression tags, and
  single-binding lexical declarations initialized by numbers. Comments,
  shebangs, recovered syntax and other constructs are outside that contract.

## Per-file source observations

Each row names a positive disqualifying construct observed directly in the
pinned source. This is not a conclusion from searching for eligible syntax or
from an empty query result. Line numbers are one-based. SHA-256 is over the
unmodified pinned LuCI source bytes.

| Pinned source path | Installed path | SHA-256 | Observed disqualifying construct | Line |
|---|---|---|---|---:|
| `modules/luci-base/ucode/uhttpd.uc` | `/usr/share/ucode/luci/uhttpd.uc` | `a2b2694f52c021af16dd06ac8c988b8a0a726d9e8186d308708268ebb8849493` | `import dispatch from 'luci.dispatcher';` top-level import; also defines a function and has calls | 3 |
| `modules/luci-base/ucode/template/csrftoken.ut` | `/usr/share/ucode/luci/template/csrftoken.ut` | `a2f223208d9ff2c3e1bfa808f11d74636028b4902973afb5b7f336328f7e2160` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/error404.ut` | `/usr/share/ucode/luci/template/error404.ut` | `8fa2306435be3aca3ca59b09adaaa0190292c6cfe2fecda9df4eb3eeac5b8552` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/error500.ut` | `/usr/share/ucode/luci/template/error500.ut` | `6c7a519229524d7a34b18c5da97cb8b05f622ee0938fe1a4b2d2516a6adf1887` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/footer.ut` | `/usr/share/ucode/luci/template/footer.ut` | `5625f938d625ff406e53434d37aa7643cc09e11f74379887a4ba154021240495` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/header.ut` | `/usr/share/ucode/luci/template/header.ut` | `67132f2d1c1cf743f3e4ce11d660a5a2569b461804a63914061fe956171be6c2` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/sysauth.ut` | `/usr/share/ucode/luci/template/sysauth.ut` | `8c1dcf98cd29410021ed4f5f9dc668f8c70c0227f39f97f60f7205f9d52fa5bb` | `{#` template comment block, explicitly outside covered roots | 1 |
| `modules/luci-base/ucode/template/view.ut` | `/usr/share/ucode/luci/template/view.ut` | `785bf7d4cceb5cdd9f113cbede0bde5b69e35b69cc1b51d2e498665d50091d62` | `{% include('header') %}` is a call expression statement in a statement tag, outside the graph allowlist | 1 |
| `modules/luci-mod-status/ucode/template/admin_status/index.ut` | `/usr/share/ucode/luci/template/admin_status/index.ut` | `652842b1e54f8a2904458ae1f5693ddfc68b97f106d8b8ff48a4d8747d673019` | `{#` template comment block, explicitly outside covered roots | 1 |
| `themes/luci-theme-bootstrap/ucode/template/themes/bootstrap/header.ut` | `/usr/share/ucode/luci/template/themes/bootstrap/header.ut` | `eca05b1e4d8391e36a08bcd0b3d0135d2addb37b9e574bd7db98d56f4835e0a3` | `{#` template comment block, explicitly outside covered roots | 1 |
| `themes/luci-theme-bootstrap/ucode/template/themes/bootstrap/footer.ut` | `/usr/share/ucode/luci/template/themes/bootstrap/footer.ut` | `b5cb417ca73c02226679ab2412e272dcf6851eee134c521fc316c39a81ecfa4e` | `{% if (!blank_page): %}` conditional control flow | 1 |
| `themes/luci-theme-bootstrap/ucode/template/themes/bootstrap/sysauth.ut` | `/usr/share/ucode/luci/template/themes/bootstrap/sysauth.ut` | `7e4702c063c95734ec3157121dc59802ff51ed2c1b73c405cd9831ddd2e0c337` | `{#` template comment block, explicitly outside covered roots | 1 |

## Bounded conclusion

No whole-root eligible positive exists among these twelve inspected files under
the producer's ordinary markup CFG contract: every file has at least one
specific disqualifying construct and source line listed above. This only rules
out these twelve exact source roots as full-root positives for this particular
contract. It does not characterize unselected LuCI sources, establish parser
routing, predict extraction diagnostics, or rule out covered substructures.
In particular, source selection/routing and the CFG graph are separate: the
expected parser route for each is `markup`, while the corresponding route
status/reason are `inconclusive` / `markup_not_modeled`; this inventory does not
reproduce or verify that extractor routing.

No CodeQL command, database query, extraction scan, or consumer step was run.
No tracked project files were edited.
