# Bounded callable call ordering at producer 11a53fd

This package records a fresh extraction and query run for three source-first
markup fixtures against producer `11a53fd8e911573860950ee8e549b337a8742438`.
The frozen oracle in [`ORACLE.md`](ORACLE.md) and [`expected.json`](expected.json)
was independently reviewed before launch. Its generator and fixture hashes are
retained here. The query sources are in [`queries/`](queries/).

## Observed result

All three fixture files routed once as markup with reason `ut_markup_extension`
and status `inconclusive` / `markup_not_modeled`. All three exact identities
were successfully extracted once. Extraction errors and fixture diagnostics
were empty.

| Fixture | Second callable | Graph result | Total nodes | Total edges |
|---|---|---:|---:|---:|
| `siblings.ut` | `call();` | covered | 19 | 16 |
| `siblings-all-covered.ut` | `let m = 2;` | covered | 18 | 15 |
| `siblings-computed-callee.ut` | `obj[key]();` | unsupported | 14 | 12 |

In the direct-call case, the second callable has the path `entry → Identifier
→ CallExpression completion → ExpressionStatement completion → exit`. In the
computed-callee near miss, the AST contains the `SubscriptExpression` callee,
`CallExpression`, and enclosing statement, but that callable scope has no graph
nodes. In all three files the first numeric callable remains covered and the
top-level creation path remains observed. No projected node crosses scope or
file. Each projected node identity has entity count 1. The edge query selects
ordered endpoints with literal `1`; it does not aggregate edge pairs. Edge
uniqueness follows from the unique counted node projections and the binary
edge relation, as in claim 028.

The root remains `unsupported` by the foundation markup CFG and only
`top-observed` by the creation graph. This is a bounded static source-order
observation. It does not establish execution, runtime call targets, full CFG
support, data flow, output behavior, security, or policy meaning.

## Revisions, tools, and provenance

- Producer: `11a53fd8e911573860950ee8e549b337a8742438`; clean before and after.
- Prior claim 028 pin: `6010ff2c0f101f7629c6fe117a421f671c311a2b`.
- The pinned grammar source is `4a243af329fae2f4ff01e0fc80133cbab8314600`.
  Its staged build dependency was changed from tree-sitter `0.27.1` to
  `=0.26.8`; the transformation digest is in `receipts/preflight.json`.
- `Cargo.lock` SHA-256: `20678c3cbb29632a9369bdb3c735af9ee63c9443879db38847fbda9813aa0a77`.
  Both QL lockfiles have SHA-256
  `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`.
- CodeQL CLI 2.27.4; binary SHA-256
  `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
- Reused extractor pack build pin `8375887ed14825dd59addbfd0df43616d9e684fb`.
  The run verified the pack against its retained build manifest and found no
  relevant extractor, grammar, tool, schema, or lock input changes between
  that build and the selected producer. This run reused the pack; it did not
  rebuild it. Its installed extractor SHA-256 and aggregate pack/dependency
  digests are in `receipts/preflight.json`.
- Process gate: no other CodeQL process was observed at launch. Disk, CPU and
  memory preflight values are in `receipts/preflight.json`.

## Commands, results, and timing

The run launch was `python3 -B <LEDGER>/work/creation-delta-oracle-20261123/run.py <LEDGER>/work/creation-delta-oracle-20261123/run-01`.
The normalized exact CodeQL argv, working directories, exit statuses and
elapsed times are in [`receipts/commands.json`](receipts/commands.json). All 20
CodeQL/version/decode commands exited 0. The run did not rebuild the extractor.

Measured wall time was 0.82 s for extraction indexing and 1.18 s for database
finalization. Extraction identity, error, diagnostic and five graph/AST query
evaluations totaled 16.15 s; their decodes totaled 1.87 s. These are separate
CLI-command elapsed times, not a full-corpus benchmark. `/usr/bin/time -l`
recorded peak resident memory per command; the highest query peak was
438,665,216 bytes for the roots query. Per-command timings and memory are
retained in `outputs/*.stderr-time.txt`.

The runner inherited `HOME`; it did not override it. It set per-run
`TMPDIR`/`TMP`/`TEMP`, `XDG_CACHE_HOME`, CodeQL compilation cache and common
package cache under the new run directory. Explicit cache paths do not prove
that every possible writable location was isolated. The inherited HOME value
is withheld from the portable receipt.

No failed CodeQL commands or retries occurred in this run. Raw databases and
BQRS files remain in the ignored local `work/` run directory and are not part
of this package. The runner is retained for inspection, but it relies on local
workspace provenance and is not a standalone reproduction bundle.

## Portable files and provenance limits

[`outputs/`](outputs/) contains all decoded JSON/CSV, assertions, routing and
command stdout/time outputs. The JSON routing and diagnostic entity URIs have
staged paths normalized to `/STAGED_SOURCE`; local workspace paths in receipts
are replaced with placeholders. [`receipt-index.json`](receipt-index.json)
records raw and portable SHA-256 for the normalized run receipts and outputs;
source-first oracle, fixture and query files are retained byte-for-byte. The
raw hashes identify files in the local run only; the portable copies are the
reviewable evidence in this repository. Neither the hashes nor the snapshots
authenticate execution independently.

Issue [ucode #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57)
remains open and deferred for broader markup CFG/dataflow. The bounded graph
implementation is documented in the pinned producer; this fixture result does
not broaden that issue's scope.
