# v0.6 full-tree source-inventory control

The disposable consumer selector checkout at base commit
`453da0d2592f64ba15cef380f0a7a3edd59e0594` now accepts the exact v0.6
manifest SHA-256
`9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`
alongside its v0.4/v0.5 pins. The change remains local and uncommitted.
Eleven selector tests pass, including prior-schema and digest rejection
controls.

On the captured OpenWrt PR #26933 base/head pair, the selector reports 52
candidates: 51 selected and one excluded, with no unreviewed identity,
missing baseline or event reason. The pinned LuCI same-SHA control reports
69 candidates: 65 selected and four excluded, also with no review event.
Every source hash and status, plus every available policy Git blob, was
compared against the v0.6 manifest. The [summary](summary.json) records exact
source/tree commits and raw report hashes; the [121-row table](identities.csv)
preserves path, blob, content hash, signals and status across both projects.
Raw reports and command notes remain under ignored
`work/gate8-v06-openwrt-20261124/`.

This is source candidate inventory, not an event scan. The selector does not
accept packages-feed input or infer recipes and installed bytes. The separate
[v0.6 CodeQL run](../mvp-corpus-v0.6-local-run/README.md) failed extraction
on two wifi files and produced no SARIF. Gate 8 remains open.
