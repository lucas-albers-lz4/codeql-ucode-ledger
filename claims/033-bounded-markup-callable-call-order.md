# Claim 033: bounded markup callable call ordering

**Status:** Demonstrated for three synthetic markup fixtures at the pinned producer revision.

**Scope:** Fresh extraction and exact creation-graph observation for a now-supported direct identifier call in one callable, with a valid computed-callee near miss and a numeric all-covered regression control.

**Out of scope:** Runtime call behavior, call target resolution, reachability, full markup CFG or data flow, rendering, security, policy, or general support for arbitrary callable bodies.

## Revisions and context

- Ucode commit: `11a53fd8e911573860950ee8e549b337a8742438`, clean before and after the run.
- Corpus/source/fixture pin: three source-first synthetic fixtures, exact SHA-256 values in [the oracle](../evidence/033-creation-call-order-delta/ORACLE.md).
- Tools: CodeQL CLI 2.27.4; grammar source `4a243af329fae2f4ff01e0fc80133cbab8314600`.
- Existing issue/contract: [ucode #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57) remains open and deferred for broader markup CFG/dataflow. The observation uses the bounded creation graph contract in the pinned producer.
- Prior comparison: [claim 028](028-creation-sibling-scopes.md) recorded the call-bearing body as unsupported at producer `6010ff2c0f101f7629c6fe117a421f671c311a2b`.

## Evidence

The independent [source-first oracle](../evidence/033-creation-call-order-delta/ORACLE.md) was prepared and passed Terra's independent review before execution. It specifies the exact three fixture bytes, root and callable scope identities, selected AST witnesses, graph nodes, ordered edges, and per-tuple multiplicity. The actual run output is preserved in [the evidence package](../evidence/033-creation-call-order-delta/README.md), including route decisions, successful file identities, diagnostics, decoded query output, assertions, timing, memory, and normalized receipt hashes.

At this pin, `siblings.ut`'s second callable body `call();` is covered by a five-node, four-edge callable path. `siblings-computed-callee.ut` changes that expression to `obj[key]();`: the AST confirms a computed `SubscriptExpression` callee, but the second callable is unsupported and contributes no callable nodes. The sibling numeric callable remains covered. `siblings-all-covered.ut` supplies the matching numeric control for both callable scopes. Across the full outputs, the three roots are only top-observed by this creation graph and remain unsupported by the foundation markup CFG.

All three fixtures routed exactly once as markup (`ut_markup_extension`, `inconclusive` / `markup_not_modeled`), extracted successfully once, and had no extraction errors or diagnostics. Exact oracle comparisons passed for three roots, six callable scopes, ten selected AST entities, 51 nodes, and 43 ordered edge rows. Every projected node identity had count one. Edge rows use literal `1`, not an aggregate count; uniqueness follows from unique counted node endpoints and the binary edge relation.

## Run record

- Date/environment: 2026-11-23, macOS; CodeQL 2.27.4. Disk, CPU, binary and pack provenance appear in the run receipt.
- Exact launch: `python3 -B <LEDGER>/work/creation-delta-oracle-20261123/run.py <LEDGER>/work/creation-delta-oracle-20261123/run-01`. The normalized exact CodeQL argv and all 20 successful command statuses are in the portable evidence package.
- Timings: extraction indexing 0.82 s; finalization 1.18 s; query evaluations 16.15 s total; decodes 1.87 s total. Peak query RSS was 438,665,216 bytes. Per-command values are retained.
- Pack: reused the validated extractor pack built at `8375887ed14825dd59addbfd0df43616d9e684fb`; relevant build inputs and installed pack manifest matched, but this run did not rebuild the pack.
- Environment: `HOME` was inherited without override. TMP and configured CodeQL/package caches were run-owned. This is a documented isolation limitation.
- Failed CodeQL attempts/retries: none in this run.
- Status limit: the output demonstrates only this bounded source-order graph behavior on these fixtures and this producer revision. No whole-root or runtime semantics follow.

See [portable evidence and normalization details](../evidence/033-creation-call-order-delta/README.md). Raw database and BQRS files remain local under ignored `work/`; portable snapshots do not authenticate execution independently.
