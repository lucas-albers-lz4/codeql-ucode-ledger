# Nested RPC query on hosted Linux producer PR #166

The hosted [producer PR #166 run 45544165223](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45544165223) completed its Linux candidate workflow for requested PR head `b8ca433dd49cc16155bf1b831f529ae07f36cb06`. The runner checked out synthetic merge commit `9add2d61f90d5bfead7700b27a3842fa3420de93`; its tree is `004159c0aeff3ecc9de04537d69710a56a658739`, matching the PR head tree. The preflight records a clean producer checkout at that merge commit.

## Nested RPC observation

The source-first oracle selected the following 11 staged inputs. Each was routed as plain Ucode, appeared exactly once in the successful-file multiset, and had zero extraction errors. The receipt records the source SHA-256 for each input:

| Installed path | Source SHA-256 |
|---|---|
| `usr/share/rpcd/ucode/different_object_same_method.uc` | `343210b52c00c857538bea54a1c9a3c47a380a5143d0811772dde3177c4c2668` |
| `usr/share/rpcd/ucode/fixed.uc` | `12bffca1f06aae14363f12d98680c0ca3a07223babd26131cc7c1612baf8fc4e` |
| `usr/share/rpcd/ucode/helper_other_replacement.uc` | `7a600182a7fd39869f6a645d19089e5a6107fefdabed27cf27a37b001cfc95bb` |
| `usr/share/rpcd/ucode/nested_helper_decoy.uc` | `7a6f3a36a92bd2ad05de9e7bcdabc9c97ea15841c93cf86bc9d7cddcc9fa5835` |
| `usr/share/rpcd/ucode/parent.uc` | `3029c32d7ccd18efb95355aa915841e2bf467b0de147ce1a65b68c55fec9d280` |
| `usr/share/rpcd/ucode/push_after_join.uc` | `8d131e58591bc6ab99c813a5cd74919ac4fb7f07aa113af56a7c09efbf54e13f` |
| `usr/share/rpcd/ucode/renamed_constant.uc` | `df201dde2634b95ccf0ce81bbb5f5e42220b185b1b5623390196f52b534c7f37` |
| `usr/share/rpcd/ucode/renamed_fixed.uc` | `e30898d14dc318f45cea509878c3685a9aac19e662be81bdb809a014f6e5f52e` |
| `usr/share/rpcd/ucode/renamed_pos.uc` | `5325abaab7fdf84a857b9bf6b2183ada72749af67f0a961f1250db6b94be4e3e` |
| `usr/share/rpcd/ucode/renamed_reassigned.uc` | `23dc041e7f2cdd500b1ec99701ed5c167bc3df537bcd93dd60b961b73178ba59` |
| `usr/share/rpcd/ucode/unreturned_method.uc` | `e953873d38476ed21c5ff31fbbf1164084eca15130437da9d412d8ec701aa458` |

The explicit `NestedRpcShellCommand.ql` run reported two SARIF results, each once: `parent.uc` at line 164, columns 3–49, and `renamed_pos.uc` at line 18, columns 5–51. The ending columns are SARIF-exclusive and matched the source-first expected locations. The other nine selected inputs had no result. Receipt SARIF SHA-256: `a0c0d820f2588a552c06c19fdd0d293a900c01631cfad3d5617a9a4c49035837`; query SHA-256: `eba4b5b732fdc205220c5eadd23ba992f911285b002e0beebda65f7c9b477e79`; manifest SHA-256: `767d6f91020f664bdacf1df9ec96329d50036d6ac41ffbd6df8407eadf2e7ecd`.

## Run and controls

The independently prepared source oracle SHA-256 is `0f1977349bd4d18529b0c32d1f62c067c9c6380660cf02cc7f1a3f4314d3a12e`. It was prepared before result inspection. The run used CodeQL CLI 2.27.4, grammar revision `4a243af329fae2f4ff01e0fc80133cbab8314600`, Rust 1.100.0 and Cargo 1.100.0. Preflight records pinned lock hashes (Cargo: `20678c3cbb29632a9369bdb3c735af9ee63c9443879db38847fbda9813aa0a77`; QL library and query locks: `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`) and isolated per-run HOME, TMP, and cache locations. The grammar build made a recorded single dependency pin transformation, `tree-sitter = "0.27.1"` to `tree-sitter = "=0.26.8"`; this is part of the run provenance.

All 126 commands in the hosted command receipt have exit status zero. For the nested sample, recorded phase wall times and peak RSS were: database init 0.880 s / 123,957,248 bytes; index 0.695 s / 113,913,856 bytes; finalize 2.059 s / 260,644,864 bytes; successful-files query/decode 2.811 / 0.391 s; extraction-errors query/decode 2.798 / 0.379 s; explicit query analysis 8.223 s / 508,104,704 bytes. The separately measured successful/error query and decode peak RSS values were 268,623,872 / 94,121,984 and 278,069,248 / 93,798,400 bytes respectively. Timings describe these bounded Linux samples only.

The normal default suite resolved to `DirectRpcShellWord.ql`, `ExtractionErrors.ql`, and `SuccessfullyExtractedFiles.ql` (resolved suite SHA-256 `e699e0829d2edb7b58213868c3a55158d5bcdb3883be3a4d9a7e419eadd945d9`). It remained unchanged by the separate nested query. In that default suite, the OpenVPN historical parent produced one direct-RPC alert; the fixed OpenVPN source and pinned LuCI swconfig source produced zero direct-RPC alerts. Each of those three sources extracted once with zero errors. The testing-tagged nested query was run explicitly against its isolated 11-file control corpus, not added to or asserted as a default-suite rule.

## Portable receipt digests and limits

The ignored raw artifact directory was `work/prod166-linux-gate-45544165223/direct-rpc-release-45544165223-1/`. It is not included here. Downloaded receipt digests are:

| Raw file | SHA-256 |
|---|---|
| `preflight.json` | `18324ec1f101dc983ac4059814c4b035fbd06c8d7cb273b2836b77b91ea1e858` |
| `receipt.json` | `1c732eb857a38e29c25e8d714edcb864785f7640bbc74b18139c8d7415e278a9` |
| `commands.json` | `755b43da8d87d80a85b4c36831c51f035893b50c80ee838aa93dd64ffc5813b6` |
| `artifact/codeql-ucode-linux.tar.gz` | `01d04cd0425e25e01133ee3a1ac9af0d0daf1353061b1a4da0babb3899f6dcd1` |

The candidate archive identifies itself as `ci-candidate`; its native extractor rebuild identity is recorded, not asserted byte-reproducible. This is evidence from a hosted Linux producer workflow and its downloaded receipts, not an independently rerun local result. Source staging and the recorded hashes do not establish installed package bytes. There was no downstream consumer handoff. This bounded query/control run makes no release, default-suite nested-rule, completeness, or security guarantee claim.
