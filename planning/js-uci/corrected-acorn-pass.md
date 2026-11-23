# Corrected Acorn pass for the planning-only UCI inventory

This pass repairs the earlier Acorn candidate traversal while preserving the
original script and 573-row output in ignored `work/js-uci-static-prep/`. It is
planning-only source evidence. It does not revise the proposal, lift the issue
#69 execution hold, or establish CodeQL behavior.

## Provenance

- LuCI source: `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Consumer source: `48c6a65b7578234644c6b06780fc82ccf6d61a8b`.
- Scope: `ql-js/manifest.json`, 88 paths; SHA-256
  `3161274241e086d121fd5122e0dfe0c5fb5d97872710d79c87f86244be2b2627`.
- Consumer corpus lock SHA-256:
  `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Acorn 8.15.0 archive SHA-256
  `e46eae89bd9761f16d1d25563b837b55b4b78f3ece06ee0b9789cb2644f523b3`, package
  metadata SHA-256 `9e422c8225c9cc4c774e9a9392d0ecac7f766b46122ef2db99db0fc4bbedc247`,
  bundled parser SHA-256
  `fdb08546776ec6228b03e8d02b40d4ab3255bae5f401adba7ff5dad927ac5c9c`.
- Independent comparator: Babel parser 7.28.5; its candidate output SHA-256
  `0cf4d6dbb8ca4eb09efca2f6bbf56f058024a70968bc08f0d8149c3e1c40d4da`.
- Corrected implementation SHA-256
  `60704b7043be52e5f72c820b2e1470bf40d91c755253c12dc711e4408b6b173e`.
  It excludes only a `MemberExpression` marked optional and does not propagate
  a `ChainExpression` marker to descendant accesses. It strips Acorn
  `ParenthesizedExpression` nodes before recognizing supported computed
  literals.
- Raw corrected candidates SHA-256
  `75a63d76144a9bc61f266f7b026747b8ce403ef3896f2e510633d33cb5ac6715`.
- The original Acorn script/output are preserved: script SHA-256
  `068775df2688f9f51ace5f94ad1ca789b2146bfd9d90bfac4b33c6a6815d7d7f`, output
  SHA-256 `be4c86883e2f3c70cfd536681d150b6a1eb95f95838508ff5213cb6a109e3e21`.

## Commands and result

Node `v26.13.1`, npm `11.20.0`. Commands were run from the ledger root, with
input and output paths relative to it:

```sh
node --check work/js-uci-acorn-corrected/inventory.cjs
node --check work/js-uci-acorn-corrected/check-controls.cjs
/usr/bin/time -lp node work/js-uci-acorn-corrected/inventory.cjs work/wave4-prep/luci-pinned work/pkg1-codeql-openwrt/ql-js/manifest.json work/js-uci-babel/babel-candidates.json work/js-uci-acorn-corrected/corrected-candidates.json
node work/js-uci-acorn-corrected/check-controls.cjs work/js-uci-acorn-corrected/synthetic-controls.js
```

All four exit statuses were 0. The corpus pass parsed all 88 files with zero
failures, emitted 576 candidate tuples, and matched Babel's 576 tuples exactly
by the multiset key `(path, inclusive 1-based span, receiver form, access kind,
property)`: zero Acorn-only and zero Babel-only. `/usr/bin/time` reported 0.18 s
real and maximum RSS 148,668,416 bytes. The portable result receipt is
[corrected-acorn-pass.json](corrected-acorn-pass.json), SHA-256
`14cb1147a6ff2f0e41015751b8b1ca80cbae2988607b208de21e6c7ff103e0ca`.

## Corrected rows and focused controls

The three rows missing from the original Acorn inventory are now present and
match Babel. In each source, `uci.get` is the nonoptional member access; `?.`
applies to the later `replaceAll` member on the call result.

| Pinned source path | Source SHA-256 | Inclusive span | Tuple |
|---|---|---:|---|
| `modules/luci-base/htdocs/luci-static/resources/tools/views.js` | `ccfcae2d0917a3fd44c54dbba3f57cec526a508e20c52e8e280f89b0ee4202a7` | 75:16–22 | bare, dot, `get` |
| `modules/luci-mod-status/htdocs/luci-static/resources/view/status/include/10_system.js` | `4001ac4a10e1cdbe7ff3fb5a883d47dc203e81cc40d47254c3717832e99f2a75` | 53:10–16 | bare, dot, `get` |
| `modules/luci-mod-system/htdocs/luci-static/resources/view/system/system.js` | `7a79896707f11d126b264ce3a14de034f550c5699786a04bfdc24911c78164dc` | 50:13–19 | bare, dot, `get` |

The synthetic fixture (`synthetic-controls.js`, SHA-256
`95e1cc0b48e0ad4f2e46926b18708a163122a05157df02d0dfdbcff8cbcb7570`) asserted
six expected candidates:

- `uci?.get` and `uci?.['get']` are excluded as optional member accesses.
- `uci.get()?.replaceAll(...)` and `uci.get?.()` retain the nonoptional `uci.get`
  member access. The downstream optional member/call is not itself a candidate
  for the `uci` receiver contract.
- `uci[('get')]` and `uci[(42)]` retain computed-index kind and resolve names to
  `get` and `42` after stripping parentheses.
- `uci['ge' + 't']` remains an eligible index candidate with property
  `<unknown>`; this pass does not constant-fold arbitrary expressions.
- `L.uci.get` is recorded with receiver form `L.uci`.

The assertions passed; the detailed six rows are in the ignored
`work/js-uci-acorn-corrected/synthetic-result.json` (SHA-256
`0a79cf2da120dd019cf215a47c5e6a46d5dd772d3763d744b4435ffe847ecf4f`).

## Limits and interpretation

The earlier parser differential's three-row Acorn deficit was caused by its
recursive optional-chain suppression, not a parsing difference: correcting the
walk makes the two parser inventories agree on these pinned sources. The
synthetic test exercises per-member optional exclusion; the proposal now
selects that interpretation for planning. The finite computed literal
recognizer is not a general evaluator, and the phrase “statically known
property names” still needs a bounded contract for reducible expressions.

Exact CodeQL AST identity/span mapping, routing, extraction, and query behavior
remain unverified. These parser results are not a complete CodeQL oracle and
make no claims about binding, invocation, runtime behavior, configuration
effects, authorization, security, or reachability. No CodeQL command was run
and no query output was inspected.
