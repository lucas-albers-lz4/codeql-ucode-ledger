# Claim 001: explicit staged-root extraction

**Status: Proposed — not yet demonstrated in this ledger.**

## Claim to investigate

For a valid explicit installed staging root containing an eligible extensionless ucode plugin, the extractor routes the selected file and the database records that exact source as successfully extracted with no extraction errors. An outside-root or otherwise ineligible source must not be mistaken for that successful input.

## Existing starting points

- Reference producer revision: [`7a1ded90962cc85a3e3a94949584c64214426aed`](https://github.com/lucas-albers-lz4/codeql-ucode/tree/7a1ded90962cc85a3e3a94949584c64214426aed).
- [Staged-routing smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/scripts/m4-staged-routing-smoke.sh), [routing controls](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/scripts/staged-routing-controls.py), [query smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/scripts/staged-routing-query-smoke.py).
- [Existing routing issue #90](https://github.com/lucas-albers-lz4/codeql-ucode/issues/90); inspect its current disposition and tests before proposing duplicate work.
- Related diagnostics: [`SuccessfullyExtractedFiles.ql`](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/ql/src/diagnostics/SuccessfullyExtractedFiles.ql), [`ExtractionErrors.ql`](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/ql/src/diagnostics/ExtractionErrors.ql).

## Evidence to collect

1. Choose a pinned producer revision and fixture; record the fixture bytes, explicit root, CLI version, commands and exact source identity.
2. Run existing controls in a disposable producer checkout, with an owned database and build outputs. Inspect the smoke and setup steps first. Verify `CODEQL_UCODE_STAGED_ROOT` reaches the actual indexing invocation when applicable.
3. Retain routing decisions **before database finalization removes temporary TRAP data** if needed; check exact path/status/reason. Separately query successful-file identities and extraction errors, preserving multiplicity. Selection is not the same as successful extraction.
4. Use an appropriate valid outside-root or wrong-identity control, and prove it reaches the intended routing guard; also retain a valid selected positive so an empty or failed database cannot pass as a negative.

## Boundaries

This checks the named source/root and extraction diagnostics. It does not establish semantic correctness, query coverage, Windows behavior, or general routing over every installed layout. No consumer or OpenWrt revision is required for this producer-only claim.

## Run record

None yet. Use [the template](TEMPLATE.md) to record actual evidence.
