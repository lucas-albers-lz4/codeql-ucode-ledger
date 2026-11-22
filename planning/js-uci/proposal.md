# Planning proposal: bounded JavaScript UCI reference inventory

Planning only. No CodeQL run, upstream edit, issue update, or execution-hold
change is authorized or performed here.

## Decision and why this is worth planning

The named decision is the remaining UCI-reference slice in OpenWrt
[issue #69](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/69):
which UCI property-access sites appear in the existing pinned JavaScript file
set, including direct `uci.*` and the observed `L.uci.*` form, while preserving
computed or otherwise unresolved property names as candidates. This would
complete a bounded source inventory family alongside the already retained RPC,
filesystem, and CGI syntax inventories. It would answer a source-inventory
question only; it would not establish calls, bindings, configuration effects,
authorization, runtime behavior, or security impact.

Issue #69 remains open. Its acceptance text explicitly asks for `uci.*`
references, and its latest logged status says the UCI inventory is undelivered.
Current consumer remote `main` is `5f8bd2658483c0c06c0ebfced98fd09b1f57aeff`.
The selected LuCI source pin is `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
The fixed input boundary is the existing 88-path `ql-js/manifest.json`
selection, not a new profile or a wider source corpus. Its recorded SHA-256 is
`3161274241e086d121fd5122e0dfe0c5fb5d97872710d79c87f86244be2b2627`; the
consumer lock SHA-256 is
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.

## Source-first anchors

All three anchors are members of the existing manifest, with matching pinned LuCI
bytes in the disposable checkout `work/wave4-prep/luci-pinned`:

| Role | Pinned path and source identity | Independently visible source sites |
|---|---|---|
| Positive | `modules/luci-mod-system/htdocs/luci-static/resources/view/system/reboot.js`; blob `92e1dd49208f465f0d91099fa69c64b74b800161`; SHA-256 `dd7e1ad72d2da510e53b194d40d9b45ec2a901939cdf655a4fc930cf42fba079`; installed `/www/luci-static/resources/view/system/reboot.js` | Line 15: `uci.changes()`; the `uci.changes` property-access span is columns 10–20. The file declares `'require uci'` at line 5. |
| Positive and receiver-form control | `modules/luci-mod-network/htdocs/luci-static/resources/view/network/dhcp.js`; blob `a0c589fcbac98a9781a4eb80c44af35f8120a0d6`; SHA-256 `b02c16b896a31789d24e615452de0596bb6b52ff4f82061172ce27e6e567f8b2`; installed `/www/luci-static/resources/view/network/dhcp.js` | Lines 943–944: direct `uci.set`; line 958: direct `uci.get`; lines 616 and 1104: `L.uci.sections`. The file declares `'require uci'` at line 6. The direct accesses and namespaced accesses should both be represented with distinct receiver-form labels. |
| Real non-match for the proposed UCI receiver forms | `modules/luci-base/htdocs/luci-static/resources/uci.js`; blob `f53b548e3eeb3ae45dfe9c8e3a09fdb77f30c78f`; SHA-256 `c14a05d8bd458d57e855513f1397132f73ce8af82ab3d1be8e102df1d22e29f3`; installed `/www/luci-static/resources/uci.js` | The implementation has `this.set` at line 676 and `this.get` at line 713. They are valid property accesses in the selected JS set but do not have either proposed receiver shape (`uci` or `L.uci`). They must not be included merely because the property name matches. |

These lines establish useful anchors, not the complete source oracle. Before any
query result is inspected, the full expected site multiset for the selected
88-file manifest must be independently enumerated and reviewed against exact
pinned bytes. The existing `rg` observations help locate candidates but are not
a completeness oracle.

## Proposed inventory contract

Use the existing family contract `rpc_surface` / `candidate` required by #69.
The query should return each `PropAccess` whose immediate receiver is either:

1. a `VarAccess` named exactly `uci`, after stripping only enclosing
   parentheses; or
2. an inner dot access `L.uci` with bare `L` as receiver, after stripping enclosing parentheses. This excludes `L['uci']`.

Classify each access as dot or index and preserve statically known property
names; use `<unknown>` when the name is not statically known. If the query
claims an index is a string literal, check the `StringLiteral` AST kind
explicitly rather than assuming every statically known name is literal. Report the
source path and inclusive access span. Keep distinct AST entities/multiplicity
before normalization; do not key raw evidence solely by rendered text or
method name. A property read such as `const methodRef = uci.get` remains a
candidate reference, but the record must not call it an invocation. A shadowed
identifier named `uci` remains syntactically eligible and must not be presented
as a resolved binding.

Optional-chain accesses are excluded from the first proposed slice; verify their
AST representation before execution. Aliases such as `const cfg = uci; cfg.set(...)`, `L['uci'].set(...)`, deeper
namespace chains, and generated/dynamic references are outside this first
receiver-shape contract. If encountered in the source-first inventory, list
them as exclusions/unknowns rather than treating their absence from results as
proof they do not exist. The `L.uci` form is included explicitly because it
occurs in the selected source; narrowing the contract to bare `uci` would miss
that source shape.

The planned fixture is [uci-surface-controls.js](uci-surface-controls.js),
SHA-256 `11562a17f9c35dc5a6f779871dac06e6c23cb7a63ed4b3b320f5575deb0098b0`.
Its predeclared positives are direct dot (`uci.set`, line 1, columns 1–7), a
property read (`uci.get`, line 2, columns 19–25), literal index
(`uci['unset']`, line 3, columns 1–12), computed index (`uci[key]`, line 4,
columns 1–8), exact namespace receiver (`L.uci.sections`, line 5, columns
1–14), and a shadowed syntactic `uci` (`uci.commit`, line 9, columns 24–33).
A parenthesized bare receiver `(uci).set` is another syntactic positive, with source span 14:1–9; its CodeQL span remains to be verified. Parenthesization is a source annotation and the normalized receiver-form label is `bare`.
The shadowed case is deliberately included as a candidate with unresolved
binding status even though its lexical shadowing is visible in the fixture. Negative controls are `other.set`, `uci2.set`, `object.uci.set`,
`L['uci'].set`, `cfg.set` after `const cfg = uci`, optional-chain access,
and `uci.*` text in a comment or string. The optional-chain example is
excluded by the proposed scope; the other cases lack a supported receiver
form or an eligible AST property access.

## Why planning proceeds; why execution does not

The issue supplies a concrete outstanding source-inventory need and pinned
scope, while the manifest contains real positive examples and receiver-form
controls. Preparing this proposal is therefore useful. However,
[the pinned inventory bridge](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/5f8bd2658483c0c06c0ebfced98fd09b1f57aeff/docs/issue-69-inventory-bridge.md)
states: “UCI inventory remains held. Its prior approval was withdrawn.” The
inspected issue history and bridge do not explain why that approval was
withdrawn. Do not infer a reason or treat this planning choice as reversing the
hold. Execution remains pending separate review/authorization.

If that review later authorizes execution, the first run should use a new
isolated workspace, exact pins and owned database/output/cache paths; establish
the full source oracle before inspecting query output; check exact selected
file identities and parse diagnostics; compare the query multiset including
controls; and retain the actual tool/lock/source identities and timings. It
must not reuse the fixture as evidence of real-source completeness, promote
Track A, or add grants or semantic conclusions.
