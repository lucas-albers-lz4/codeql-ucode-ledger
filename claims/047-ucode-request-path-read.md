# Claim 047: Request-controlled paths into ucode fs read/stat

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (historical routing probe P2; see current reconciliation)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-8qcq-jgrj-gvmj (BMX7 unchecked query traversal)
- GHSA-jjcx-c284-2qv8 (openvpn path traversal → root RCE)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends pass request-controlled path strings to fs.open/fs.read/fs.stat/fs.readlink within the supported same-function slice, and is any canonicalization observed in-source?

## Method

Bounded slice over manifested application set; record path-construction chains and any observed `..` handling; canonicalization absence is a source observation, not a traversal verdict.

## Required evidence

- Site multiset with chain identities
- Predeclared oracle
- Canonicalization observation per site

## Controls

- Positive: request.args.path into fs.read without observed checks
- Near miss: path joined under a fixed prefix with observed `..` rejection
- Negative: literal path

## Out of scope

- No traversal exploitability claim
- No runtime filesystem state

## Notes

None.

## Historical result at 734555a9

Blocked — producer routing gate (probe P2, orchestrator-verified) plus a
sink-model gap. Security-40 lifts no gate.

- P2 at codeql-ucode `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean):
  extractor `file_globs` accepts literal basenames only; application `.uc`
  backends skipped ("No matching language found, skipping file");
  `RequestArgsExec.ql` l.18 gates `getBaseName() = "luci"`. The manifested
  application set this claim's method requires is therefore not extracted
  (7/8 slice files skipped; receipts probe-ucode/{VERDICT.md,MANIFEST.yml,
  logs/}).
- Additionally `fs.open` / `fs.read` / `fs.stat` / `fs.readlink` are outside
  the M4 request-args sink model (NamedFsPopenCall / BuiltinSystemCall only),
  so even routed files would not surface read-side path flows.
- No source canonicalization observation was made (claim method is the
  bounded producer slice, not a hand inventory).
- Unblock: producer routing extension to application `.uc` + a read-side fs
  sink model decision in codeql-ucode; then re-run this claim's slice.
- Evidence: `/root/workspace/work/security-40/probe-ucode/` (P2 receipts);
  gates verified in producer `extractor/src/extractor.rs` and
  `ql/src/m4/RequestArgsExec.ql`.


## Current reconciliation (2026-11-24)

[Scratch evidence](../evidence/application-source-observations-20261124/README.md) at producer `9166af76cf6944e1b3ea5856a9176366a1f7a6ee` and pinned LuCI shows one source-staged DDNS `stat` shape and two synthetic positives, with eight bounded negative-control mutations. The 11-file extraction and exact observations are separate from the historical P2 result above; they do not establish application-wide routing or coverage. The attribution uses a conservative source-declared import subset, not a modeled imported `stat` binding. No fs sink, request-to-path flow, canonicalization verdict, authorization or runtime claim follows.

**Status remains Blocked.** [#155](https://github.com/lucas-albers-lz4/codeql-ucode/issues/155) retains its routing, honesty and modeled-control prerequisites. The applicable [#49](https://github.com/lucas-albers-lz4/codeql-ucode/issues/49) Grok honesty gate and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) promotion gate are not represented as passed. [Routing PR #162](https://github.com/lucas-albers-lz4/codeql-ucode/pull/162) was draft at this observation; no merge is assumed.
