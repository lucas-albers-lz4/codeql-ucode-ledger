# Claim 014: conservative `fs` binding guard on named controls

**Status: Demonstrated for the named fixture cases.**

## Claim and boundary

At the pinned producer, the experimental library-callable test identifies the
unaliased direct `fs` `popen` call in `popen__direct.uc`, and leaves the named
formal-shadow, local-shadow and sibling-formal cases unresolved. These are
source-level attribution controls, not proof of runtime binding. The sibling
case illustrates deliberate conservative loss of recall: an unrelated or
expired competing binding can cause a genuine imported call to be omitted.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4. The
[contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-imported-fs-popen.md)
requires a conservative source-declared unaliased import and excludes files
with relevant competing bindings. Inspected the four named source fixtures and
expected manifest before running. In the disposable producer clone, ran
`HOME=<isolated-home> bash scripts/m4-fs-binding-smoke.sh`; exit 0. It built a
fresh database, retained routing before finalization and ran the real
`FsBindingTargetsTest.ql` and extraction diagnostics. Its verifier checked the
pinned fixture hashes, full exact call and target identity multisets and
routing decisions: **109 routed files, 108 successful files, one extraction
error, 583 call entities and 83 fs targets**. The one
[error](../evidence/014/errors.json) is the deliberately malformed
`readfile__malformed.uc`, not one of the four named popen controls.

[Selected actual rows](../evidence/014/selected-targets.json) include the
positive direct `popen` at `2:28–2:52` with library target `popen`; the
formal-shadow (`2:46–2:70`), local-shadow (`2:70–2:94`) and sibling-formal
(`3:28–3:52`) call entities have no target. The valid near misses were
successfully extracted and had actual CFG-backed call entities, so absence of
a target is not an absent input. The producer's manifest is a mixture of
frozen earlier entity inventories and manually specified cases, not a blinded
independent review; this claim relies only on the four inspected shapes. The
reviewed evidence normalizes temporary paths and selects those rows from the
larger output. Raw outputs and log remain local under ignored `work/`.

The Models-backed `NamedFsPopenCall` uses the shared conservative guard, but
this test alone does not establish every query's behavior or complete lexical
resolution. Excluded calls remain unknown, not safe. Existing broader modeling
is tracked by [ucode #51](https://github.com/lucas-albers-lz4/codeql-ucode/issues/51)
and gated query work by [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54).
