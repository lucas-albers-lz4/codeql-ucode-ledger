# Package 10 preliminary source review: copied popen receivers

Prepared from pinned source and query contracts only. No CodeQL scan, database,
query result, or consumer execution was performed.

## Scope and pins inspected

- Producer source/query contract, inspected in a clean disposable checkout, at
  `6010ff2c0f101f7629c6fe117a421f671c311a2b`.
- Consumer query/policy scope, inspected in a clean disposable checkout, at
  `48c6a65b7578234644c6b06780fc82ccf6d61a8b`.
- LuCI source, inspected in a clean disposable checkout, at
  `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Selected source scope: the 21 pinned source rows used by the existing
  `luci-ssl-25.12` mixed-profile slice in
  [claim 025's source oracle](../../evidence/025-mixed-profile/source-first-oracle.json) (9 plain and 12 markup rows). The review read
  each selected plain source that contained `popen`/receiver uses; the only
  relevant files are listed below. This is a bounded selected slice, not every
  LuCI file or every package in the repository.

The exact relation in `docs/m4-receiver-direct-copy.md` requires a direct
variable declarator initialized by source-declared `fs` `popen`, a separate
single direct identifier copy of that variable, and a direct non-optional
`read`/`close` member call whose receiver read may flow from that copy. A
popen result read directly through its original variable is not this alias-copy
shape.

## Source candidates reviewed

| Source identity | Source shape observed | Assessment for direct-copy query |
|---|---|---|
| `modules/luci-base/root/usr/share/rpcd/ucode/luci`, blob `64caf75c08bc0fa54520a0ef262dfd6f339dc89e`, SHA-256 `6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`; imports `{ ..., popen, ... } from 'fs'` at line 6 | Direct declarations `fd = popen(...)` at lines 26, 37, 278 and 585; `swc = popen(...)` at 343 and 400; and `block = popen(...)` at 481. The handles are read/closed directly: `fd.read`/`fd.close` at 29/32, 40/43, 281/290, 297/309, 318/332; `swc.read`/`swc.close` at 350/384 and 405/454; `block.read`/`block.close` at 486/500. The line 585 `fd.read` is at 591; this function does not show a corresponding close in the selected source. The `fd` assignments at 294 and 315 reuse the earlier `fd` variable and are not declarator initializers. | Relevant direct source-handle/member-call sites, but the inspected uses are through the same variable, without a separate direct identifier copy before `.read()`/`.close()`. The later `fd` reassignments are not the query's direct initializer form. No copied-receiver positive candidate identified in this source. |
| `modules/luci-base/ucode/sys.uc`, blob `35b5fcdebfaf1210be16ab1552752cb249346899`, SHA-256 `0380fba5d843a8950bab0ef70982cb40ab8f475e8d267c873e4199a736b55656`; imports `{ ..., popen, ... } from 'fs'` at line 4 | `const top = popen(...)` line 7; direct `top.read` line 10 and `top.close` line 27. `nfct` is first declared from `open(...)` at line 47, then assigned `popen(...)` at line 49; `nfct.read` line 54 and `nfct.close` line 112 use that same variable. | `top` is a direct source handle with member calls, but no extra copy variable is present. `nfct` has an open initializer and later popen assignment, so it does not meet the direct popen-declarator initializer condition. No copied-receiver positive candidate identified in this source. |

Precise source positions of the most relevant direct sites (one-based lines;
columns count source characters, with tab occupying one source character):

- `luci`: line 481 `const block = popen(...)` begins `popen` at column 18;
  `block.read(...)` is on line 486 and `block.close()` on line 500. This is
  the `getBlockDevices.call` source.
- `sys.uc`: line 7 `const top = popen(...)` begins `popen` at column 14;
  `top.read(...)` is line 10 and `top.close()` line 27. In `conntrack_list`,
  line 49 assigns `popen(...)` to existing `nfct` (popen begins column 10),
  followed by `nfct.read` line 54 and `nfct.close` line 112.

## Broader pinned-tree adjacent case, outside selected slice

`applications/luci-app-lxc/ucode/controller/lxc.uc` is not among the 21
selected profile source rows. Its Git blob is
`1f4f041c7da60886c0e8b6696632e553ab86cc1b`, SHA-256
`19b5dc5d2db606ac90053409eaf9031c1fc69b229b4c0e875ddfcbbbf2a9ca70`.
At line 31, `let p = fs.popen('df -kP ' + path);` begins `fs.popen` at column
10; `p.read('line')` occurs on lines 32 and 33 and `p.close()` on line 34.
This is an adjacent direct-handle example, not a separate copied alias, and it
is outside the named selected slice. Other LXC calls at lines 54 and 177 chain
`.read()` directly onto `fs.popen(...)`; they do not introduce a copied
receiver variable.

## Named query/consumer dependencies inspected

- `ql/src/m4/ReceiverDirectCopy.ql` is the explicit experimental query for a
  direct copied receiver. It emits the relation itself; no other QL query in
  the inspected producer query roots imports or consumes this query's result.
- `ql/src/m4/FsReceiverProvenance.ql` imports `FsReceiverOrigin.qll`. That
  predicate associates direct `.read()`/`.close()` calls with the variable
  declarator initialized by `popen`; it does not model the extra copied
  identifier relation described by `ReceiverDirectCopy.ql`.
- Named sink/effect queries inspected include `BlockDeviceExec.ql`,
  `GetFeaturesDirectExec.ql`, `LuciSysStatusExec.ql`, `RequestArgsExec.ql`, and
  `ShellInjection.ql`. Their predicates select `NamedFsPopenCall` and/or
  command arguments, method containment, and request-argument taint. They do
  not consume the copied-receiver relation. The inspected consumer `policy/`
  and `ql-js/` trees likewise exposed no query/API consuming that producer
  relation.

## Preliminary conclusion and limit

No copied-receiver case with a named affected analysis query was discovered in
the 21-source selected slice. The visible cases are direct receiver uses or
an existing-handle reassignment, and the named analysis queries inspected do
not consume the experimental copied-receiver relation. This is not proof that
no such source or consumer exists elsewhere in LuCI, in other packages, in
uninspected query roots, or at other revisions. It is not evidence that the
production receiver-model hold is resolved, and it does not establish runtime
resource identity, call targets, or security behavior.
