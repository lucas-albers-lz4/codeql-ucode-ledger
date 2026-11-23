# Planning-only parser differential for the 88-file UCI inventory

This receipt compares two independent parser inventories of the fixed JavaScript
scope proposed for OpenWrt issue #69. It records a source-level parser
mismatch; it does not establish CodeQL extraction or query behavior.

## Inputs and reproducibility

- LuCI source commit: `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Consumer source commit used for the manifest: `48c6a65b7578234644c6b06780fc82ccf6d61a8b`.
- Scope: `ql-js/manifest.json`, 88 paths; manifest SHA-256
  `3161274241e086d121fd5122e0dfe0c5fb5d97872710d79c87f86244be2b2627`.
- Consumer lock SHA-256:
  `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Independent implementation used `@babel/parser` 7.28.5 (package JSON SHA-256
  `06e89556fea2851b071797c63c0565725ba8b889014a07ac6ad62dbde52157de`, parser
  entry SHA-256 `4fad5d076afb8c346159a06bb942d6e14c6167d590082b7c3bdebd4c108af201`,
  npm archive SHA-256 `d69b0c78b14cfef7d9ac3e933473839ba61080fdc8c9f0a787ac8bf0ea18bea7`).
  The inventory script SHA-256 is
  `3068a4f2af2367e256347578e81bd98639eb853967fb5baee1d6f20b51da45fb`.
- Comparator: Acorn 8.15.0 candidates from the same manifest and source tree;
  candidate JSON SHA-256
  `be4c86883e2f3c70cfd536681d150b6a1eb95f95838508ff5213cb6a109e3e21`.
- Node `v26.13.1`; npm `11.20.0`. The source check verified each input's
  manifest SHA-256 before parsing.

The raw parser result and script remain under ignored `work/js-uci-babel/` for
local reproduction. The portable, normalized tuple receipt is
[parser-differential.json](parser-differential.json), SHA-256
`289563d65c848f570eb8e866f87d43cdb6ab0ecbfa00fb269553c1844339fe8e`.
It contains no machine-specific absolute paths. No CodeQL command was run and no
query output was inspected.

## Result

Babel parsed 88/88 files without parser failures and emitted 576 candidate
property accesses. Acorn emitted 573. The multiset key was path, inclusive
1-based source span, receiver form, access kind, and property name. There were
zero Acorn-only tuples and three Babel-only tuples; the other 573 matched.

| Pinned source path | Source SHA-256 | Inclusive access span | Candidate |
|---|---|---:|---|
| `modules/luci-base/htdocs/luci-static/resources/tools/views.js` | `ccfcae2d0917a3fd44c54dbba3f57cec526a508e20c52e8e280f89b0ee4202a7` | 75:16–22 | bare `uci.get` (dot, `get`) |
| `modules/luci-mod-status/htdocs/luci-static/resources/view/status/include/10_system.js` | `4001ac4a10e1cdbe7ff3fb5a883d47dc203e81cc40d47254c3717832e99f2a75` | 53:10–16 | bare `uci.get` (dot, `get`) |
| `modules/luci-mod-system/htdocs/luci-static/resources/view/system/system.js` | `7a79896707f11d126b264ce3a14de034f550c5699786a04bfdc24911c78164dc` | 50:13–19 | bare `uci.get` (dot, `get`) |

Each site has the form `uci.get(... )?.replaceAll(...)`. The optional access
operator is applied to `.replaceAll` on the result of the call. The `uci.get`
member access itself is nonoptional. The Acorn walk propagates an optional-chain
flag down to child nodes, so it omits that enclosing access; the Babel walk
excludes only the optional member itself. Thus the difference is in treatment
of an inner nonoptional access inside an optional-chain expression, not in
property-name or span normalization.

## Contract and evidence limits

The proposal says optional-chain accesses are excluded, but it does not yet
settle whether that means only a member node marked optional or every access
nested in an optional-chain expression. These three rows expose that unresolved
boundary. They are eligible under a per-access reading and excluded under a
whole-expression reading. Resolve that contract before treating either parser's
count as the intended expected set.

The Babel helper strips enclosing parentheses and recognizes a finite list of
computed static forms (string/numeric/boolean/null/bigint literals, no-substitution
templates, and unary numeric literals). It is not a general constant evaluator;
other reducible expressions such as `uci['ge' + 't']` would remain `<unknown>`.
The proposal's phrase “statically known property names” needs a bounded rule for
such expressions. Parenthesized literals themselves are recognized by the
helper. No computed `uci[...]` candidate appeared in the 88-row corpus inventory,
so this limitation did not create a tuple difference here.

Neither parser inventory has been mapped to CodeQL AST node classes or spans.
Agreement or disagreement between these source parsers cannot establish which
CodeQL entities are emitted, which markup/plain routing path applies, or what a
query returns. This is planning-only evidence; it has no runtime, binding,
invocation, configuration-effect, authorization, security, or reachability
implication.
