# Planning: newer wifi Ucode parse gaps

This note investigates the two extraction failures recorded in [claim 089](../claims/089-newer-openwrt-wifi-parse-boundary.md). It is a grammar/producer design note only: no patch was made, no CodeQL run was performed, and no runtime-validity conclusion is claimed.

## Pins inspected

- Producer source: `work/mvp-corpus-v0.6-run-20261124-b/producer-checkout`, clean at `9166af76cf6944e1b3ea5856a9176366a1f7a6ee` (as recorded by claim 089).
- Grammar: `work/wave2-prep/tree-sitter-ucode`, at `4a243af329fae2f4ff01e0fc80133cbab8314600`, clean.
- OpenWrt source: `work/incoming-live-pr26933-20261124/source`, clean at `bce40f6a15c273778061e8fceced7b9e0f58d99b`.

## Grammar causes

### `import("provision")` in `lib/wifi/mac80211.uc:17`

The source is an expression assignment: `provision = import("provision");`. In `common/define-grammar.js`, `import_statement` (around lines 271–278) accepts only static import syntax: either an import clause with `from` and a string, or a side-effect string. `import` is globally reserved, and the primary-expression alternatives do not provide a dynamic-import expression. The grammar corpus `ucode/test/corpus/modules.txt` has a named case “Dynamic import expression — not in the targeted release, produces ERROR”; it explicitly says only static `import` statements are supported in that grammar snapshot. Thus the parse failure is an intentional version-boundary gap in the pinned grammar, rather than the producer misrouting the `.uc` file.

Minimal grammar option: add a dynamic-import expression production for `import ( expression )`, in the expression/primary-expression hierarchy, and preserve the existing static declaration production. Avoid representing it as a normal identifier call unless the produced tree shape is intentionally a `CallExpression` and all downstream consumers can tolerate that conflation. A dedicated node or explicit import callee node is easier to distinguish, but may require node type/schema regeneration and CodeQL AST mapping changes. If the intended AST is a normal `CallExpression`, inspect the generated grammar and query contracts for reserved-word/callee representation before choosing that route. The public grammar corpus itself establishes this feature is outside its targeted release; it does not establish which grammar branch/runtime version first accepts it.

### Exported functions in `usr/share/ucode/wifi/utils.uc:72,76`

The two declarations are `export function board_wlan() { ... }` and `export function rename_phy_by_name(...) { ... }`, each without a trailing semicolon. `function_declaration` (around lines 754–762) permits `optional($._automatic_semicolon)`, but `export_statement` (around lines 216–233) wraps a function declaration in a separate alternative ending in a required literal `';'`. This export wrapper is the restrictive production. The corpus case “Export named function (requires trailing semicolon)” demonstrates the accepted form; the grammar comment says exported functions require `;` and optionality exists only on Ucode master.

Minimal grammar option: replace the wrapper's literal `';'` with the same semicolon policy used by ordinary function declarations, likely `optional($._automatic_semicolon)` after checking scanner/ASI behavior. Avoid blindly using broad `$._semicolon`: its choices include block-end, which may admit EOF-only cases beyond the desired source form. A narrowly tested optional automatic semicolon matches the ordinary function production, subject to the intended grammar version's actual syntax contract.

## AST/model implications

- The export change should retain the existing `export_statement` → `function_declaration` tree shape and fields, making it primarily a parse-acceptance expansion. Verify it does not change semicolon ownership or statement boundaries for adjacent declarations.
- Dynamic import adds a new expression shape. If modeled distinctly, regenerate `ucode/src/node-types.json` and the producer's generated CodeQL AST bindings, then determine whether it belongs under existing call/import abstractions. Do not assume imported-callee resolution, module identity, or dataflow follows from parsing it.
- Both fixes change the pinned grammar inputs and generated parser/schema. The producer's extractor pack and generated language model must be rebuilt/revalidated against that grammar. Existing parse-error diagnostics must remain visible for malformed controls.

## Local mechanism and test design

The pinned grammar has an offline corpus harness: `package.json` scripts `test` and `build`; `scripts/run-tests.js` generates/builds when stale, runs `tree-sitter test` for each grammar and query/tag checks. The checked tree has no `node_modules/.bin/tree-sitter`, so this mechanism is not presently ready to invoke without dependency setup. The corpus files are the intended place for focused positive and negative cases. The producer checkout also documents `cargo test` and its parser-load smoke in `README.md`, but that only validates the producer's loaded parser and existing smoke fixture; it does not exercise these two sources or assert exact AST identities. No targeted producer regression for either source was found in the inspected tests/docs. No specific existing issue assigning these two precise syntax gaps was found in the producer's local roadmap/docs; avoid duplicating general parser/extractor work without checking current upstream issue ownership.

Discriminating grammar/producer controls for a future patch:

1. Positive: exact `import("provision")` expression and assignment context; retain positive static side-effect and clause imports.
2. Negative: malformed dynamic import (missing close paren, missing argument if disallowed, or trailing unexpected token), and an identifier named similarly such as `importer("provision")` to ensure no broad keyword rewrite.
3. Positive: exported function with no semicolon followed by another declaration, matching the two source shapes; also retain the semicolon-terminated export.
4. Negative: malformed exported function body and a deliberately incomplete export, plus a bare ordinary function and lexical export as parse controls.
5. Run corpus tests first, then producer parser tests on a disposable checkout built against the revised grammar. Finally recheck exact extraction success and diagnostics for the two source identities plus `wireless.uc` and `wireguard.uc` controls. This is a future verification plan, not a result.

## Boundary

The grammar corpus and exact source text support the production-level explanation above. They do not establish runtime validity of the OpenWrt sources, which runtime version accepts these forms, semantic correctness of any AST representation, or that a producer patch is safe. Claim 089 remains an extraction observation at its recorded pins until a separately pinned grammar/producer change is tested.
