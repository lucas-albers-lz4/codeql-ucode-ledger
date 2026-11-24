# v0.5 full-tree selector control

The disposable consumer checkout `work/gate8-full-tree-selector` was updated
locally to accept the exact v0.5 source manifest digest alongside the v0.4
digest. It is based on consumer commit
`453da0d2592f64ba15cef380f0a7a3edd59e0594` and remains uncommitted and
unpublished. Nine focused selector tests pass. The source checkout was clean
at OpenWrt `4e9642517b48bae612ff10fb72fb9199e559500e`.

With that OpenWrt SHA as both base and head, v0.5 enumerated 47 candidates:
46 selected, one excluded, zero unreviewed, zero missing baselines and no
fail-closed event. The same tree with the pinned v0.4 policy had 34 selected,
one excluded and 12 unreviewed, and failed closed. The [summary](summary.json)
records exact source/tree and policy identities and hashes of both raw reports;
the [identity table](identities.csv) preserves all 47 source paths, blobs,
content hashes, signals and classifications. Every v0.5 blob and content hash
was independently compared to the reviewed manifest, and the 12 v0.4
unreviewed paths are exactly the v0.5 additions. Raw event reports remain
under ignored `work/gate8-v05-openwrt-20261124/`.
The pinned LuCI same-SHA control also remained ready: 69 candidates, 65
selected and four excluded, with no unreviewed paths. All 69 content hashes
and statuses, plus available manifest blob IDs, matched the reviewed policy.

This is a source candidate inventory on one unchanged pinned tree. The
selector still lacks recipe inference, installed-byte verification, CodeQL,
SARIF and an actual incoming-change handoff. Gate 8 remains open.

The same local selector was then run on the captured OpenWrt PR #26933
[base/head pair](pr26933-summary.json). It found 52 candidates at each
revision: 46 selected by v0.5, one excluded and five unreviewed. The only
event reason was `no_reviewed_disposition` for those five; no selected content
changed. It returned exit 1 and `review_required`, as intended. The
[exact 52-row table](pr26933-identities.csv) preserves paths, blobs, hashes,
signals and reasons. This captured pair does not authenticate the PR's
current head or establish a running upstream CI trigger.
