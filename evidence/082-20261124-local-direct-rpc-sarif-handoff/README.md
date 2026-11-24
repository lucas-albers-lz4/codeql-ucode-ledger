# Claim 042 evidence

Run-b is the fresh local handoff. The source-first manifest, exact source/stage digests, diagnostic results, resolved suite query IDs, SARIF and accepted result identities are in `handoff-results.json`. `commands-normalized.json` preserves all 30 command argv, exit codes, wall times, peak RSS and stdout/stderr hashes. `raw/` carries the exact manifests, receipts, SARIF, accepted outputs and diagnostic JSON bytes used or returned. `raw-hashes.json` lists their original digests.

The raw files retain the run machine's absolute `/Users/lalbers/.../work/`
paths because they are the exact bytes passed between producer and consumer.
Those paths identify this one local execution; they are not portable artifact
locations or evidence that another machine can access `work/`. The normalized
files map those local stage paths to `usr/share/rpcd/ucode/...` identities
while retaining hashes of the raw files, so the relationship is explicit.

Parent accepted one `ucode/m4/direct-rpc-shell-word` warning for `req.args?.cl_meta` at `usr/share/rpcd/ucode/luci.openvpn.uc` line 71 columns 115–132; fixed and swconfig accepted no results. All three had one exact successful-file identity and zero extraction errors. The suite resolved the direct rule and two diagnostics queries; only the direct rule is a SARIF descriptor.

`run_b.py` orchestrated run-b; `run.py` remains the superseded run-a prototype. The temporary producer workspace starts from a prior 29d8 snapshot plus both final queries from integrated commit 299731d. Executed queries, suite, diagnostics and locks match the integrated checkout. `pack_sha256` names the extractor executable hash; full pack inventory and build provenance are recorded separately. The pack provenance records a dirty grammar Cargo.toml patch.

This is a local macOS draft run and parser handoff only. The consumer checks supplied bytes and expected results but does not authenticate arbitrary receipts. This is not Linux/release validation, installed-byte equivalence, runtime exploit evidence or shell quote-state proof.
