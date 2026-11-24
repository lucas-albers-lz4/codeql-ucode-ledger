# MVP bounded corpus v0.1: source-first aggregate

Status: preparation for MVP-1 Gate 6, 2026-11-24. The exact selected and
excluded identities are in [the manifest](mvp-bounded-corpus-v0.1.json)
(SHA-256 `7c71634e7a02c5aa5776820f6b141b086935b8cff117d5bbfdd5cced668db601`).
This is a deduplicated aggregate of prior local evidence, **not** a fresh
combined extraction, a Linux scan or a Gate 6 pass.

The source pins are LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`,
OpenWrt `4e9642517b48bae612ff10fb72fb9199e559500e`, and packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`. The current selection has
65 non-symlink, package-mapped LuCI paths from the 69-path census and 11
OpenWrt `package/utils/cli` paths. It lists four LuCI exclusions: two tracked
test fixtures without package install mapping and two symlinks whose targets
were not followed. The packages-feed pin is recorded for the next inventory
step; no packages-feed file is selected in v0.1. Each of the 76 selected
source bytes was rehashed from the clean isolated source checkout and matched
its prior evidence digest; source identity is `(repository, commit, path)`.
The portable [source verifier](../scripts/verify-mvp-corpus-source.py) checks
these hashes and Git blobs against clean exact-pinned checkouts. It passed on
the isolated local LuCI, OpenWrt and packages-feed checkouts; it does not
authenticate extraction or installed output.

Prior separate local claims report successful extraction once and zero errors
for each selected path. That does not prove one coherent run at this manifest
revision. Of the 76 selected paths, 42 previously had plain routes and 34 had
markup-inconclusive routes. The 34 must remain in the coverage denominator as
selected and extracted, and in the unsupported/inconclusive denominator for
modeled markup. A successful-file diagnostic must never relabel them modeled.
Proposed installed paths are source-tree projections; no package build or
installed-byte comparison has verified them.

Next, use this manifest as the predeclared oracle for one fresh isolated Linux
run with the released producer. Compare exact selected paths, routing reasons,
successful-file identities, diagnostics and SARIF with multiplicity. Separately
inspect package install transformations and expand the denominator to other
OpenWrt core and packages-feed ucode-bearing roots. Current source alerts,
performance and missed eligible shapes remain unmeasured at this aggregate
scope.
