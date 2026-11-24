# Filling the R3 release lock from an immutable producer release

Status: procedure prepared before publication, 2026-11-24. The consumer
[draft PR #154](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/154)
keeps every release-dependent field null until an actual immutable release
exists. Producer [PR #159](https://github.com/lucas-albers-lz4/codeql-ucode/pull/159)
merged as `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, but the grammar
compatibility [PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161)
passed Linux R2, Cargo and M3/M4 smoke at `b25bdd3` and merged as
`104a398468f214961168d2edc9a10be45b80062f`. Release-setting and
published-asset verification still precede a consumer lock.
A passing PR Actions artifact has
`artifact_kind: ci-candidate` and cannot supply the final asset digest or
producer commit for this lock.

After the reviewed producer release candidate passes all hosted gates and merges,
verify that the repository's
active `v*` tag ruleset still blocks update and deletion and that **Enable
release immutability** is on before creating a version tag. Record the full
merged `main` commit, the exact tag and its peeled remote object ID. Use a
new `vMAJOR.MINOR.PATCH` tag (the initial pack metadata is 0.1.0; verify
the final release version and unused tag namespace at publication time).
Set the workflow policy variable only after the setting is confirmed.

The 2026-11-24 prepublication check found producer `main` at
`104a398468f214961168d2edc9a10be45b80062f`, no returned tags or
releases, and active tag ruleset `28002678` matching `refs/tags/v*` with
both `deletion` and `update` rules. The repository REST metadata does not
expose the release-immutability toggle. A fresh Playwright Chrome context
reached the settings URL unauthenticated and received GitHub's sign-in-only
404, so the toggle remains unverified. Do not create a tag or set the policy
variable from the tag rule alone.

Once the tag workflow publishes, fetch the release metadata independently:
the tag must match, the release must be published and `isImmutable` true,
and exactly one expected Linux bundle asset URL must exist. Download that
asset to a new run-owned path and hash its bytes; compare with the release
`SHA256SUMS` asset, but retain the independently calculated outer SHA-256 as
the consumer pin. Fetch the producer verifier from the **tagged full commit**,
hash it, then use it to safely unpack the pinned asset in a new directory.
The unpacked `bundle-manifest.json` must declare `versioned-release`, the
same tag and commit. Hash the manifest and each required file independently;
the manifest is a consistency record, not its own authenticity proof.

Map the reviewed observations into `docs/r3-release-lock.json`:

| Lock field | Independent source or byte check |
|---|---|
| `release.tag`, `release.commit` | GitHub release tag plus peeled remote Git tag and full `main` commit. |
| `release.asset_url`, `release.asset_sha256` | Exact immutable-release asset URL and downloaded archive SHA-256; compare published `SHA256SUMS`. |
| `release.manifest_sha256` | SHA-256 of unpacked `bundle-manifest.json`, after outer archive and producer verifier pass. |
| `release.verifier_sha256` | SHA-256 of `scripts/verify-linux-release-bundle.py` fetched at the tagged producer commit. |
| `release.extractor_sha256` | SHA-256 of unpacked `extractor-pack/tools/linux64/extractor`, checked against manifest `build.built_extractor_sha256`. |
| `release.library_lock_sha256`, `release.query_lock_sha256` | SHA-256 of unpacked `ql/lib/codeql-pack.lock.yml` and `ql/src/codeql-pack.lock.yml`. |
| `release.suite_sha256` | SHA-256 of unpacked `ql/src/codeql-suites/code-scanning.qls`, checked against manifest pack metadata. |
| `release.packs.*.version` | Unpacked QL pack metadata and manifest pack identities; do not assume current 0.1.0 without checking release bytes. |
| `release.codeql_binary_sha256` | SHA-256 of `codeql/codeql` inside the separately downloaded, digest-pinned official CodeQL 2.27.4 Linux archive. |

Leave the pinned `source_oracle_sha256`, exact expected rule IDs and official
CodeQL archive URL/SHA under separate review. Do not change them merely to
make a job pass. Commit the filled lock in the consumer draft and run its
fresh Linux historical handoff; review the retained raw SARIF and command
receipt. The stacked [current-corpus PR #155](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/155)
and [v0.6 upgrade PR #157](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/157)
then exercise the same released tool on the frozen 128-path corpus. Neither
a downloaded release nor a lock with matching strings proves installed
package bytes or incoming-change coverage.

The lock also contains fields that are fixed consumer policy rather than
values to derive from the new release: `schema`, `release.repository`,
`release.artifact_kind`, `release.expected_rules`, `codeql.version`,
`codeql.url`, `codeql.sha256` and `source_oracle_sha256`. The latter hashes
`docs/r3-openvpn-source-oracle.json` in the consumer. Check those bytes and
the rule IDs against the reviewed consumer commit; do not populate them from
the producer asset. The independent `SHA256SUMS` comparison above is an
additional publication check: the current R3 runner does **not** read that
file. Its acceptance depends on the separately pinned outer asset digest.

After filling the lock, the R3 runner also verifies the peeled tag commit,
published non-prerelease immutable GitHub release, one exact expected asset,
tagged verifier bytes, unpacked manifest/pack metadata, unchanged QL locks
after install, and suite resolution to exact reviewed query paths/IDs and
multiplicity. Preserve these runtime observations in the Linux receipt; a
syntactically complete lock alone is not acceptance.
