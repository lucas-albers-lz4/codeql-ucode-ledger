# R3 clean Linux producer-to-consumer handoff

Status: implementation contract refreshed 2026-11-24. Consumer
[PR #152](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/152)
merged the strict offline SARIF parser and source-first OpenVPN oracle.
[Draft PR #154](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/154)
adds the released-producer Linux job; its contract checks pass and its live
job is skipped while the release lock is null. Producer
[PR #157](https://github.com/lucas-albers-lz4/codeql-ucode/pull/157)
merged the candidate bundle and Linux R2 gate. Publication
[PR #159](https://github.com/lucas-albers-lz4/codeql-ucode/pull/159)
merged as `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; grammar
[PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161)
then passed final-head Linux R2, Cargo and M3/M4 smoke and merged as
`104a398468f214961168d2edc9a10be45b80062f`. No versioned release exists yet, so
the live R3 job cannot pass.

## Lock and source-first inputs

Commit a consumer-owned lock before running R3. It must pin an immutable
producer release tag and full commit, the release asset URL and outer SHA-256,
the bundle-manifest digest and expected extractor/QL pack/suite identities,
the official CodeQL 2.27.4 Linux archive URL and SHA-256, and the historical
source pair. Do not substitute a run-scoped Actions artifact or moving branch.
The existing R2 Actions bundle says `artifact_kind: ci-candidate`; it is not
the release lock input. After publication, derive the candidate lock from
the actual release tag, commit, GitHub release metadata, independently
downloaded asset bytes and the unpacked `versioned-release` manifest. Hash
the producer verifier from that exact commit and the Linux CodeQL executable
from the separately pinned official archive. Review the filled lock against
the downloaded bytes and source-first oracle before committing it. A
release-tag and asset digest must be verified independently of the internal
manifest; a manifest is not self-authenticating.

The frozen OpenVPN pair is LuCI parent
`b45584b4e6068b9b096872dd02494a048d869c36`, fixed
`e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`, source path
`protocols/luci-proto-openvpn/root/usr/share/rpcd/ucode/luci.openvpn.uc`.
Parent SHA-256 is
`051c8162f826683333e11264615806df5ab08415676c0bd098921cb1b05af991`,
fixed SHA-256 is
`6593792678951fd500c2b090d17d9e500a05a642cfb996ee02c1649473152410`.
Both stage at `usr/share/rpcd/ucode/luci.openvpn.uc` in separate source roots
and databases. The default-rule expectation is one parent warning with rule
`ucode/m4/direct-rpc-shell-word` at line 71, UTF-16 columns 115–132, and
zero fixed results. Declare the second Tailscale historical matrix as a
separate release regression, since its testing query is not in the default
suite.

## Job sequence and receipt

Use `ubuntu-24.04`, read-only repository permission and unique run-owned
download, `HOME`, `TMPDIR`, caches, source, database and output directories.
Measure each phase with GNU `time -v`. Verify both archive digests before
unpacking. Obtain the producer verifier from the exact pinned producer commit
(it is not inside the current bundle), hash it, and safely verify/extract the
bundle. Bootstrap locked `ql/lib` and `ql/src` dependencies in writable
run-owned copies; compare lock digests after install and record network use.
Resolve the default suite from the extracted bundle and compare exact query
IDs and suite digest with the lock.

For each OpenVPN case, fetch the full LuCI commit into an isolated checkout;
check clean HEAD, Git blob and source SHA before inspecting output. Copy
verbatim source bytes into a separate proposed installed-path stage and check
stage equality. Record that **actual package-installed bytes are unverified**
unless a package build separately proves them. Create/finalize a fresh CodeQL
database from that stage using the extracted Linux extractor, query exact
successful-file and extraction-error diagnostics, then run the released
default suite to fresh SARIF. Require the exact resolved rule set, one
selected/extracted file and zero errors. Pass the same SARIF bytes, a
source-first case manifest, a receipt generated from actual commands and the
stage root directly to `tools/sarif_accept.py`; retain its accepted record.
The fixed case must run its own database and produce a zero-result SARIF.

The receipt must bind the CI run ID, consumer full SHA and clean state,
release tag/asset digest, producer commit, tool and pack digests, source
commit/blob/stage hashes, exact selected and extracted identities,
diagnostics, resolved suite and rule IDs, SARIF digest, each command/exit,
wall time and peak RSS. Keep raw SARIF and small normalized receipts as CI
artifacts. Existing local `work/direct-rpc-local-handoff/run_b.py` is a
macOS draft implementation example only: it copies a built pack and cache,
uses `/usr/bin/time -l`, and does not pin a release.

The parser validates supplied bytes, but it cannot authenticate that a
database was indexed from those bytes or that a receipt is genuine. The
trusted job must bind source staging, database creation, diagnostics, SARIF
and consumer invocation in one process chain. An offline parser pass, a
matching count or a replayed artifact does not close R3.
