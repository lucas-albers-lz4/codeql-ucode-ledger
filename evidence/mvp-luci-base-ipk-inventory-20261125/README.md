# Complete `.uc`/`.ut` member inventory of one pinned `luci-base` IPK

Status: demonstrated for the suffix-defined regular-file members of the
single [run 45513606386](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45513606386)
IPK. This follows the [two-file staged-byte comparison](../mvp-installed-byte-luci-base-20261125/README.md)
and does not broaden that comparison's preparation/staging checks to every
member. The inventory was motivated by inspecting the completed artifact,
then checked against the pinned source and build rules; it is retrospective,
not a source-first CodeQL extraction oracle.

The retained artifact `luci-ipk-byte-45513606386-1` contains
`luci-base_26.284.22350~8125d12_x86_64.ipk` with SHA-256
`1a2188f5206ce61c993fdcc451781a06994ae2175b489eef56595858ef22b363`.
The exact IPK remains in the Actions artifact and ignored `work/`, not Git.
The independently checked LuCI source is clean at
`b2e0be4b46ec0fd43394c081fa7c50657af14011`.

`verify.py` opens the gzip outer tar and its `data.tar.gz` without writing
members to disk. It enumerates every `.uc` or `.ut` member, rejects duplicate
or nonregular suffix members, compares the member identity set with all 15
tracked suffix files under `modules/luci-base/ucode/`, checks source bytes,
and checks the exact `header.ut` version-token substitution. The command was:

```sh
python3 -B evidence/mvp-luci-base-ipk-inventory-20261125/verify.py \
  work/luci-ipk-byte-success-45513606386/luci-base.ipk \
  work/stage6-luci > evidence/mvp-luci-base-ipk-inventory-20261125/inventory.json
```

It exited 0 and produced the committed [exact identity and hash inventory](inventory.json):

| Class | Members | Observation |
|---|---:|---|
| Source bytes equal IPK bytes | 14 | Eight `.uc` files and six `.ut` files map exactly to pinned tracked source paths. |
| Version substitution | 1 | `template/header.ut` replaces `{# PKG_VERSION #}` with `26.284.22350~8125d12`; the resulting bytes equal the IPK member. |
| Generated | 1 | `version.uc` has no `ucode/` source file. The IPK member contains revision `26.284.22350~8125d12` and branch `LuCI openwrt-25.12 branch`. |

There are **16 unique regular suffix members** in total: nine `.uc` and seven
`.ut`. `modules/luci-base/src/Makefile` lines 15–16, 27 and 34 generate and
install `version.uc` from `LUCI_VERSION` and `LUCI_GITBRANCH`; the retained
build log records the corresponding `echo` and install commands. The script
reports its actual member bytes and SHA-256 but does not claim an independently
predeclared expected branch string. The 14 equal files and transformed
`header.ut` are exact comparisons to the clean source checkout.

This denominator excludes extensionless Ucode, files of other suffixes,
other packages and different build configurations. It does not show which
members a CodeQL extractor selected or scanned, nor establish a released
Linux handoff. Source-stage analysis of `header.ut` is not byte-identical to
this installed package. `SHA256SUMS` checks the small portable files here;
the IPK hash above links them to the retained raw artifact.
