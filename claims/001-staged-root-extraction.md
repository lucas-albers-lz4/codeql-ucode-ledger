# Claim 001: explicit staged-root extraction

**Status: Demonstrated for the bounded run recorded below.**

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

See the bounded run below and [the template](TEMPLATE.md) for future runs.

### Run: 2026-11-18 UTC — ordinary Linux staging root

**Status: Demonstrated for the named fixture and controls below.** This is a
producer-only observation, not a statement about current or future revisions.

- Producer: `d3588ca6821fe983d240fcbb2e80692fabcc6aab` (clean detached clone
  before setup). Since the reference commit, the tracked delta changes only
  the quote smoke and its Python tests. OpenWrt was not used. Issue #90 was
  closed when checked; this run does not independently verify every acceptance
  criterion in that issue.
- Linux, CodeQL 2.27.4, Cargo 1.100.0, Python 3.15.2; grammar commit
  `4a243af329fae2f4ff01e0fc80133cbab8314600` (the setup script modifies
  its local dev dependency). Fixture
  `ql/test/extractor-smoke/usr/share/rpcd/ucode/luci` SHA-256
  `6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
- In the disposable clone, with a private `HOME` and `CARGO_HOME` and
  `CARGO_BUILD_JOBS=4`, ran `bash scripts/clone-grammar.sh`,
  `bash scripts/create-extractor-pack.sh`, and
  `bash scripts/m4-staged-routing-smoke.sh`; each exited 0. The smoke's five
  direct controls passed, as did its ordinary and recognized root checks and
  its missing-input mutation. The shell indexing wrapper forwards
  `CODEQL_UCODE_STAGED_ROOT` as `--staged-root`.
- Ran the retained [direct control](../evidence/001-20261118/routing-evidence.py)
  (exit 0). Identical fixture bytes inside `stage/usr/share/rpcd/ucode/luci`
  and outside the root were passed together to the extractor. The
  [receipt](../evidence/001-20261118/direct-routing.json) shows one
  `plain_route_selected` with `rpcd_raw_mode_full_path` and installed identity
  `usr/share/rpcd/ucode/luci`, and one `excluded` with
  `outside_staged_root`; one source TRAP was produced.
- Ran an [evidence-preserving copy](../evidence/001-20261118/ledger-staged-routing-query.py)
  of the upstream query smoke, placed in the clone's `scripts/` directory and
  invoked with `LEDGER_RUN_DIR` set to a fresh absolute canonical directory.
  It uses `database init`, `index-files` with the explicit root in the
  environment, saves the routing receipt before `finalize`, then runs and
  decodes the successful-files, errors and AST queries. Exit 0. The
  [database receipt](../evidence/001-20261118/database-routing.json) records
  exactly one selected input; [successful files](../evidence/001-20261118/extracted.json)
  contains exactly that input, and [errors](../evidence/001-20261118/errors.json)
  contains zero rows. The script also verified one function declaration at
  lines 17–19. The direct and database runs use separate copies of the same
  pinned fixture, not the same database.
- A first evidence-preserving run exited 1 in its path assertion because the
  supplied run directory contained `..`, while the extractor returned a
  canonical path. It had produced the expected routing decision; a fresh run
  with a canonical directory passed. No production code was changed.

The checked-in JSON is a reviewed transcription of the decoded output with
only the private workspace prefix replaced by `<RUN>`; it is not the raw
byte-for-byte artifact. The generated databases, raw outputs, build logs and
failed run remain local under ignored `work/` and are not portable evidence.
This result does not establish general language semantics, query coverage,
Windows behavior, or all installed layouts. Re-run against a newly selected
revision and inspect its delta before carrying the observation forward.
