# Pinned LuCI package-byte experiment

Status: corrected preparation scaffold, 2026-11-24. No OpenWrt package has
been built and no IPK member has been observed. The first version of this
scaffold assumed an `ar` outer IPK; source review of pinned OpenWrt
`scripts/ipkg-build` showed it creates a **gzip-compressed outer tar** with
`debian-binary`, `data.tar.gz` and `control.tar.gz`. The local comparator and
synthetic tests were corrected. Earlier preparation receipts describe the
then-current scaffold, not evidence that its archive assumption was true.

The executable hosted version is
[codeql-openwrt draft PR #161](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/161),
which runs the same corrected comparator plus an isolated Ubuntu build script.
Its manual workflow is the next intended experiment after hosted contract
checks and review. A fresh `workflow_dispatch` can run only once that workflow
exists on the repository default branch. Keep the build informational; do
not treat a contract test or a synthetic archive as installed-byte evidence.

## Fixed source and output decision

| Repository | Full commit |
|---|---|
| OpenWrt | `4e9642517b48bae612ff10fb72fb9199e559500e` |
| LuCI | `b2e0be4b46ec0fd43394c081fa7c50657af14011` |
| packages feed | `07e0d16305d2b5903b37ad7913e33e18795f81a4` |

Use x86/64, `CONFIG_PACKAGE_luci-base=m`, disabled APK output, and local
`src-link` LuCI/packages checkouts at those pins. The `luci-base` recipe
copies `ucode/http.uc` directly and applies `SubstituteVersion` to
`ucode/template/header.ut`. The experiment requires exact, unique paths and
compares pinned Git blobs, prepared build files, package-stage files and
the retained IPK data members for each. `http.uc` must be identical at all
four points. `header.ut` must be identical through preparation, then match
the inspected package-version substitution at stage and IPK. Parse the IPK
control `Package`, `Version`, and `Architecture` fields and match the exact
archive bytes retained with the receipt.

The host tools and cross-toolchain must be built before the package target;
an individual package compile target on a fresh OpenWrt tree does not
bootstrap them. The workflow records run-owned `HOME`, `TMPDIR`, source and
feed status, config/feed digests, GNU time phases, command output, the exact
IPK and a comparison receipt. A missing or duplicated path, failed build,
unexpected archive format, wrong substitution, source/config/feed drift or
control metadata mismatch is a failed experiment. The generated target and
stage layout are still unverified on Linux and may fail closed.

Local helper check from this directory:

```sh
python3 -B -m unittest -v test_compare.py
```

These synthetic tests exercise archive parsing and comparison controls; they
do not produce installed bytes. A successful Linux job would establish only
the two selected package members at these exact pins, not an installed root
filesystem, a deployed device, or the whole Ucode corpus.
