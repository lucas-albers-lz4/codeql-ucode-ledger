# Wave 1 source inventory receipt

Scope: mechanical, source-first inventory for the `luci-ssl-25.12` profile. No CodeQL command, extractor, database, or query was run. The portable manifest is [`source-first-manifest.json`](source-first-manifest.json); it records exact source paths, Git modes/blob IDs, byte SHA-256 digests, intended installed paths, routing classification from the consumer contract, package membership, symlinks, controls, collisions, and transformation findings.

## Revisions and source identity

- Producer `codeql-ucode`: `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`, clean disposable clone.
- Consumer `codeql-openwrt`: `d37adeadaf836ba97049f75087a348165027f7f9`, clean disposable clone.
- LuCI: `b2e0be4b46ec0fd43394c081fa7c50657af14011`, matching `corpus/lock.json`, clean disposable clone made with `--no-hardlinks` from a pre-existing clean local clone at the identical SHA; its `origin` was reset to the canonical GitHub URL.
- Consumer lock SHA-256: `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Consumer profile seed: `arch=x86_64`, `CONFIG_IPV6=y`, `CONFIG_PACKAGE_luci-ssl=y`.

The consumer inventory transcribes 11 `.ut` candidates. A separate `git ls-tree -r --name-only HEAD` enumeration, filtered to all package directories in the profile dependency closure and `.ut` suffix, returned exactly the same 11 paths. No extra/missing `.ut` identity was found. The pinned LuCI Makefiles' `LUCI_DEPENDS` edges agree with the inventory closure when the profile's `CONFIG_IPV6=y` conditional is applied. The 11 source files map via `luci.mk` `ucode/` installation to distinct `/usr/share/ucode/luci/...` paths; no collisions were found.

## Transformation and boundary findings

`luci.mk` copies each package's `ucode/*` into `$(LUCI_LIBRARYDIR)` and calls `SubstituteVersion`. The `.ut` rewrite replaces `{# ...PKG_VERSION #}` with `PKG_VERSION` or `PKG_SRC_VERSION`, and adds `?v=...` to quoted `{{ media }}` / `{{ resource }}` references ending in `.js` or `.css`. The selected `luci-base` `header.ut` contains the version token; bootstrap theme `header.ut` contains matching asset references. The profile seed does not resolve `PKG_VERSION` or `PKG_SRC_VERSION`. These two installed files therefore cannot be equated byte-for-byte to their raw staged source from this inventory. The other nine selected templates have no matching `SubstituteVersion` token at this pin. No package installation was performed.

The extensionless `bootstrap-dark` and `bootstrap-light` entries are Git symlinks to `bootstrap/`, not source files; both are recorded as exclusions. The separate `uhttpd.uc` source used by claim 020 is not part of the 11 `.ut` set. The generated `version.uc` is not a source blob. The actual pinned `modules/luci-base/htdocs/cgi-bin/luci` source is a shebang plain-route control at `/www/cgi-bin/luci`.

Producer-side fixture controls are predeclared from its markup smoke: `tests/data/markup/usr/share/ucode/controls/mixed.ut` is the valid markup positive; `.../plain.uc` is the eligible plain `.uc` control. Their known smoke expectations and hashes are retained in the manifest. Those expectations were read from the smoke source and docs; they were not rerun in this wave.

Routing expectation is the consumer contract's `.ut` => `markup` rule; this receipt does not observe extractor routing, extraction success, or per-file diagnostics. `markup_not_modeled` remains the stated analysis status. No inference is made about completeness, runtime behavior, rendering, CFG, or security.

## Commands, status, and elapsed time

All commands ran from the ledger root `<LEDGER_ROOT>`; no credentials were used.

| Command | Status | Elapsed/output |
|---|---:|---|
| `mkdir -p work/wave1-luna` | 0 | completed |
| `/usr/bin/time -p git clone https://github.com/lucas-albers-lz4/codeql-ucode.git work/wave1-luna/codeql-ucode` | 0 | `real 0.58`, `user 0.07`, `sys 0.09` |
| `/usr/bin/time -p git clone https://github.com/lucas-albers-lz4/codeql-openwrt.git work/wave1-luna/codeql-openwrt` | 0 | `real 0.72`, `user 0.15`, `sys 0.07` |
| `/usr/bin/time -p git clone https://github.com/openwrt/luci.git work/wave1-luna/luci` | 130 (interrupted) | `real 78.04`, `user 0.51`, `sys 0.48`; full network clone was stopped while still running |
| `git -C work/claim020/luci rev-parse HEAD` and `git -C work/claim020/luci status --porcelain=v1` | 0 | exact lock SHA; no dirty output |
| `/usr/bin/time -p git clone --no-hardlinks work/claim020/luci work/wave1-luna/luci` (followed by `git remote set-url origin https://github.com/openwrt/luci.git`, SHA/status/remote verification) | 0 | `real 0.82`, `user 0.44`, `sys 0.56`; SHA equals lock and tree clean |
| `/usr/bin/time -p python3 work/wave1-luna/build_manifest.py` | 0 | `real 0.27`, `user 0.10`, `sys 0.18`; exact 11-path comparison passed |

No retry was made against the interrupted network clone. The fallback used a separate checkout with no hardlinks, not a shared writable working tree. No extraction/query/consumer timing exists because wave scope ends at source inventory.

## Tool and resource snapshot

- Git: `2.56.1`.
- Python: `3.15.2`.
- `codeql` was not found on `PATH`; no CodeQL run was attempted.
- At preflight: filesystem reported 132 GiB available, 16 GiB physical memory, 10 CPUs.
- Peak memory was not measured; this was a lightweight clone and source-inventory task.

## Reproduction

From the ledger root, run `python3 work/wave1-luna/build_manifest.py` after the three source checkouts are available at the manifest's recorded revisions. The manifest generator only reads the checked-out source trees and writes within this ignored work directory.
