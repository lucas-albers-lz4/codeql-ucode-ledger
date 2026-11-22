# Claim 022: selected mixed-template AST boundaries

**Status:** Demonstrated for the selected pinned source and controls.

**Decision and scope:** Can the markup AST distinguish selected expression,
call and literal-text syntax in a clean real template from a tag-like string
literal? This is a bounded AST observation, not a rendering, flow, call-target
or security claim.

## Inputs and expectations

The producer was the clean tracked tree at
`0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`, with three ledger-authored queries
added only in its disposable checkout. LuCI source
`modules/luci-base/ucode/template/view.ut` came from
`b2e0be4b46ec0fd43394c081fa7c50657af14011`; its SHA-256 was
`785bf7d4cceb5cdd9f113cbede0bde5b69e35b69cc1b51d2e498665d50091d62`.
It was staged at its expected installed-relative path, not obtained from a
configured installation. Claim [021](021-pinned-luci-template-extraction.md)
records the profile's selection and installation-transform limits.

The [source-first oracle](../evidence/022-mixed-template-ast/oracle/source-first-oracle.json)
identified `{{ view }}` at `7:24–7:33`, its `view` identifier at
`7:27–7:30`, `include('header')` at `1:4–1:20`, and two neighboring literal
text nodes with source-derived positions and expected parent kinds/indexes.
The valid near miss contains `{{ include('header') }}` inside a ucode string;
the oracle identified that string and expected no expression-tag or call
node in the control. Parent index 2 for the string was corrected from 1 by
source/grammar review **before** querying because the extractor includes the
unnamed `=` child.

## Run and observations

A fresh four-file database used the pinned `view.ut`, the literal-lookalike
control, the producer's known `mixed.ut` extraction positive, and a plain
`.uc` control. [Routing](../evidence/022-mixed-template-ast/outputs/routing.json)
matched the four predeclared identities and routes; the three markup routes
remain inconclusive. The upstream
[successful-file output](../evidence/022-mixed-template-ast/outputs/extracted.json)
listed each file once, while
[extraction errors](../evidence/022-mixed-template-ast/outputs/errors.json)
and the separate all-diagnostics query both returned zero rows. The
successful-file diagnostic selects file identities without a `parse_error`;
it is not a separate per-file execution attestation.

The [ledger-authored broad inventory](../evidence/022-mixed-template-ast/queries/Wave2MarkupViewInventory.ql)
returned 15 rows. Each of the six predeclared target identities appeared once
with its expected span, parent kind and index; the actual
[output](../evidence/022-mixed-template-ast/outputs/markup-view-inventory.json)
and [comparison](../evidence/022-mixed-template-ast/outputs/wave2-query-comparison.json)
retain all nine additional rows. The view identifier's reported parent has
`ExpressionTag` kind and the expected `7:24–7:33` span. The selected text
nodes and tag report matching `TextStatement` parent descriptors; the query
did not select parent entities, so those descriptors do not prove a shared
parent identity. Entity URLs describe file locations and are not unique
internal AST identifiers.

The [broad control audit](../evidence/022-mixed-template-ast/outputs/markup-nearmiss-audit.json)
returned zero `ExpressionTag` or `CallExpression` rows in the lookalike file,
while the main query positively identified the enclosing `String` at
`1:18–1:42` under `VariableDeclarator` index 2. The `mixed.ut` fixture was an
extraction control, not a queried semantic positive. Neither an empty audit
nor a successful-file row alone would establish the control.

All extraction and query commands exited 0. The broad inventory query took
2.52 seconds wall and 451,444,736 bytes maximum RSS; the near-miss audit took
2.69 seconds and 545,652,736 bytes. The [receipt](../evidence/022-mixed-template-ast/README.md)
records individual commands, diagnostic and decode timing, pack provenance,
and setup/reporting failures. Results are local observations, not execution
attestation. They do not establish template rendering or escaping, the runtime
binding of `include`, dispatcher behavior, markup CFG/dataflow, authorization,
or a vulnerability. OpenWrt
[#68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68) retains
integration and ucode [#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57)
retains deferred CFG/dataflow. No consumer was invoked.
