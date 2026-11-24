# Exploratory full-tree Ucode candidate inventory

2026-11-24 local macOS run. The isolated consumer implementation at
`453da0d2592f64ba15cef380f0a7a3edd59e0594` (based on draft PR #156
`3a2197cd087bb5b76e4ffaaa3fe2df3e829a3f55`) enumerated Git-tracked
source candidates at exact commits. It used Python 3.15.2, Git 2.56.1 and
the v0.4 policy manifest SHA-256
`1e25cf9c2adc40c854502fed8d1ccc0977a3c4825d6ee4a1c0a543ffe0a76699`.
The seven synthetic controls passed. No CodeQL database, package build or
consumer handoff was run.

The OpenWrt base `727d8d2f8e5b19a2121e2cf05824e9e5cac35310` and PR
#26933 head `bce40f6a15c273778061e8fceced7b9e0f58d99b` each yielded 52
candidate paths. At the head, 34 matched reviewed selected policy, one was
excluded, and 17 were **unreviewed**; the selector exited 1 for review. The
[portable OpenWrt identity summary](openwrt-summary.json) lists each exact
path/blob/content hash and has the raw report digest
`edfdce4cba8133dcb71d6accddcd99243a868983f11c4d0076ce2391f351c279`.
The pinned LuCI source `b2e0be4b46ec0fd43394c081fa7c50657af14011`
used as both base and head yielded 69 paths: 65 selected, four excluded and
none unreviewed; the selector exited 0. The [LuCI identity summary](luci-summary.json)
has raw report digest
`3baf444d09fd558075be21978fde0c398a9699117fcb7b026c02cf8496c15df7`.
The raw JSON outputs remain under ignored
`work/incoming-live-pr26933-20261124/` on this machine; the portable summaries
normalize them to current head identities and pin the raw hashes.

To reconcile the later PR head with the v0.4 OpenWrt pin, the same selector
also ran with base=head at `4e9642517b48bae612ff10fb72fb9199e559500e`
(tree `328d4df01c038d365176b72753b778e10c3ff413`). It found 47
candidates: 34 selected, one excluded and 12 unreviewed, with zero missing
baseline paths; exit 1 as expected. The
[pinned OpenWrt identity summary](openwrt-pinned-summary.json) lists all 47
path/blob/content hashes and pins the raw report SHA-256
`3194fb7834b1d0d4f1707b8a600e576498f592d020ef6c8270a52ea3c8179c27`.
These 12 are exactly the paths present at that pin from the 17 later-PR
unreviewed paths. Their package/target mappings still require review before
selection.

The substantive commands from the isolated consumer checkout were:

```sh
python3 -B tools/full_tree_candidates.py docs/current-corpus-source-v0.4.json openwrt ../incoming-live-pr26933-20261124/source 727d8d2f8e5b19a2121e2cf05824e9e5cac35310 bce40f6a15c273778061e8fceced7b9e0f58d99b ../incoming-live-pr26933-20261124/full-tree-openwrt.json
python3 -B tools/full_tree_candidates.py docs/current-corpus-source-v0.4.json luci ../stage6-luci/collections/luci b2e0be4b46ec0fd43394c081fa7c50657af14011 b2e0be4b46ec0fd43394c081fa7c50657af14011 ../incoming-live-pr26933-20261124/full-tree-luci.json
python3 -B tools/full_tree_candidates.py docs/current-corpus-source-v0.4.json openwrt ../stage6-openwrt 4e9642517b48bae612ff10fb72fb9199e559500e 4e9642517b48bae612ff10fb72fb9199e559500e ../openwrt-pinned-full-tree.json
python3 -B tools/test_full_tree_candidates.py -v
```

This was exploratory discovery against a reviewed v0.4 baseline, not a
source-first oracle for all possible candidates. The signal union includes
suffixes, first-line Ucode shebangs, extensionless paths under installed
Ucode roots, and explicit v0.4 identities. It cannot infer package recipes,
configuration conditions, generated sources or actual installed bytes. The
17 OpenWrt rows need source/recipe disposition before an event scan can pass.
Neither the LuCI zero-unreviewed result nor these local exit statuses prove
full selection coverage, a Linux Gate 6/7 result or MVP Gate 8.
