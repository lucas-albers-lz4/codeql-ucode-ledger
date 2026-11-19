# Claim 019: shell-injection query on a selected LuCI source slice

**Status: Demonstrated for eight selected installed-source entries and the stated controls.**

## Claim and selection

At producer `8376a6d72a2879de24e68a28c6ef1e02b319df83`, the current
`ShellInjection.ql` emits exactly the seven source/sink tuples in the table
below when run over the eight selected plain ucode sources listed by the pinned
`luci-ssl-25.12` inventory for package `luci-base`: the extensionless rpcd
plugin plus its seven selected `.uc` libraries/controllers. All seven rows
originate in the plugin; the other seven files produced no rows for this
query. This is a bounded result for this selection, not a statement about the
remaining profile or runtime behavior.

The query's expected rows were derived from the pinned upstream source and
recorded before querying in the
[source-first receipt](../evidence/020-20261118-luci-shellquote-slice/source-first.json):

| Method | Sink line | Source line |
|---|---:|---:|
| `getSwconfigFeatures` | 343 | 343 |
| `getSwconfigPortState` | 400 | 400 |
| `getRealtimeStats` | 585 | 575 |
| `getRealtimeStats` | 585 | 577 |
| `setPassword` | 474 | 470 |
| `setPassword` | 474 | 471 |
| `setLocaltime` | 111 | 108 |

## Pins and fresh run

- Producer: `8376a6d72a2879de24e68a28c6ef1e02b319df83`.
- Consumer inventory/lock: `1d025213c102dfa68a0f1a5cb46de65f5b0c4e33`.
- LuCI source: `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Lock SHA-256:
  `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Selected source identities, installed paths and SHA-256 values are recorded
  in the source-first receipt; the upstream `luci.mk` installation rules and
  the consumer's pinned source inventory were checked.

A fresh database selected exactly eight files; extraction diagnostics reported
eight successes and zero errors. `ShellInjection` returned seven rows with
exact expected identity and multiplicity. `CompleteQuotedArg` and
`ShellquoteTemplateShape` returned zero rows for this source set. A separate
fresh 31-file quote-control database passed the exact selected-file and
zero-error gate: `taint_pos` was present, `taint_neg` absent, supported shape
controls were recognized, unsupported shapes remained candidates, and no
trusted quote barrier was emitted. See the [CSV outputs](../evidence/020-20261118-luci-shellquote-slice/)
and [timing/identity receipt](../evidence/020-20261118-luci-shellquote-slice/commands-and-timings.json).

## Near misses and limits

The seven other selected sources contain no `request.args` property expression
under the source audit. `sys.uc` does contain `popen` calls and a parameterized
`system` call; it receives values through function parameters. The rpcd plugin
also calls `init_action(request.args.name, request.args.action)`. This query's
same-file `RequestArgsAccess` model does not establish that imported-callee
path, so the absence of a `sys.uc` row is **not** a `no_path`, safety, or
reachability result. Keep the imported-callee boundary partial under claim 005
and existing ucode #50/#54 ownership.

The eight selected sources exclude the profile's CGI script, generated version
source, markup/uncertain paths, other packages, native C plugins, and every
other OpenWrt component. Dispatcher/runtime semantics were not analyzed. No
fresh producer output was passed to a consumer adapter. The seven rows are
experimental static candidates, not vulnerability findings; no shell, device,
RPC session, exploitability, authorization, full-profile completeness, or
full-corpus runtime was tested. This adds bounded pinned-source impact evidence
for ucode #75, but does not complete that issue's broader acceptance criteria.
