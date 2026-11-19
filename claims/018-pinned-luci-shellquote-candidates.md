# Claim 018: pinned LuCI shellquote candidate output

**Status: Demonstrated for one pinned upstream source file and the named controls.**

## Claim and boundary

At producer `8376a6d72a2879de24e68a28c6ef1e02b319df83`, `ShellInjection.ql`
emits exactly seven `request.args`-to-`popen`/`system` candidate rows for the
single pinned LuCI rpcd plugin file. Four rows go through the same-function
locals `getRealtimeStats.flags` and `setPassword.u`/`p`; the other rows are the
two direct `swconfig` templates and `setLocaltime`. `CompleteQuotedArg` and
`ShellquoteTemplateShape` emit zero rows for the actual plugin: its local
`shellquote` binding is not treated as a known helper, and no trusted quoting
barrier is modeled. These are query outputs under a bounded static model, not
vulnerability findings or runtime shell behavior.

## Pins and independently established expectations

- Producer: `8376a6d72a2879de24e68a28c6ef1e02b319df83`.
- LuCI: `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Consumer context only: `1d025213c102dfa68a0f1a5cb46de65f5b0c4e33`.
- LuCI `luci` file SHA-256:
  `6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
- Consumer corpus-lock SHA-256:
  `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.

Before querying, the selected upstream source was read and the expected tuples
were recorded in
[the source-first receipt](../evidence/019-20261118-shellquote-actual-source/source-first.json).
The source/line expectations were:

| Method | Sink line | Source line | Source expression |
|---|---:|---:|---|
| `getSwconfigFeatures` | 343 | 343 | `request.args.switch` in the `popen` template |
| `getSwconfigPortState` | 400 | 400 | `request.args.switch` in the `popen` template |
| `getRealtimeStats` | 585 | 575 | interface-branch `request.args.device` → `flags` |
| `getRealtimeStats` | 585 | 577 | wireless-branch `request.args.device` → `flags` |
| `setPassword` | 474 | 470 | `request.args.username` → `u` |
| `setPassword` | 474 | 471 | `request.args.password` → `p` |
| `setLocaltime` | 111 | 108 | `request.args.localtime` → `t` |

The fresh source file is byte-identical to the LuCI fixture used by the
producer's quote smoke. The model/query/control files relevant to this run are
unchanged from producer `094a163db1138c83820197180501bd7c78bd9051`.

## Fresh producer runs: 2026-11-18 UTC

The current producer extractor was built from the pinned checkout. The
producer's `scripts/m4-quote-smoke.sh` then passed on its separate 31-file
control database: exact selected-file multiset, zero extraction errors,
`taint_pos` present, `taint_neg` absent, supported-shape controls recognized,
malformed/unsupported quote shapes retained as candidates, and no
`CompleteQuotedArg` rows. The actual LuCI fixture in that database has the
same SHA-256 as the pinned upstream file.

A second fresh database used the real LuCI source at its package-layout path
and selected exactly that one file. Diagnostics reported one successful file
and zero extraction errors. The three analysis queries and decodes exited 0;
the exact output and multiplicity are preserved in
[the query artifacts](../evidence/019-20261118-shellquote-actual-source/):
`ShellInjection` had seven rows matching the source-first table,
`CompleteQuotedArg` had zero, and `ShellquoteTemplateShape` had zero. The
focused producer smoke took 35.37 s wall / 628,904 KiB peak RSS; timings for
actual extraction, each query and decode are in the run receipt. CodeQL was
2.27.4.

The current consumer's focused quoted-locals report test also passed (7 tests).
That test checks a retained *inventory* whose `evidence_status` is not
`path_found`; it does not ingest the fresh producer output. The consumer report
is explicitly pinned to producer `step3:shellquote-barrier-v2` at
`ae946190661eb221bc1f562fdba02088ef83de2d` and says it is not a fresh query
run. This claim therefore records a current query result alongside a prior,
non-handoff consumer snapshot; it does not claim that the consumer accepted or
rejected these seven rows. The current owner is [ucode #75](https://github.com/lucas-albers-lz4/codeql-ucode/issues/75), whose broader
query-control and reconciliation criteria remain separate work.

## Limits

Only one pinned LuCI file was selected for the actual-source database. The
control database is separate, although its LuCI bytes are identical. The query
is an experimental static candidate query; its same-function binding model is
not CFG/SSA or complete shell semantics. No output was passed through a fresh
producer-to-consumer adapter. No device, RPC session, shell command, firmware,
full corpus, reachability, exploitability, safety, or authorization conclusion
was tested. The historical consumer report's scope and absence of rows are not
negative evidence about this fresh run.
