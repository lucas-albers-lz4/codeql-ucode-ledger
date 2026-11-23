# Source-first oracle for v2 synthetic provider-feed scope

Consumer source pin `48c6a65b7578234644c6b06780fc82ccf6d61a8b`, clean disposable checkout at inspection. This specification precedes execution and contains expected results only.

Decide whether a synthetic provider migration to another feed preserves a valid gate while invalidating an expectation scoped to the original feed. Both providers have the same package name, version and content bytes. The existing feed test moves the provider policy and resource before checking a stale permission. This comparison instead holds both permission and resource current and varies only selected expectation applicability and the submitted reference. [Existing feed test](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/tests/test_v2_adapter.py#L407-L429)

## Deterministic inputs

Use ASCII literals for raw content, with zero trailing bytes after the quoted string: corpus `"ledger synthetic status corpus"`, profile `"ledger synthetic status profile"`, caller content `"ledger synthetic status client package"`, provider content `"ledger synthetic status provider package"`. Serialize all JSON documents as UTF-8 using lexicographically sorted object keys, comma and colon without surrounding spaces, and no trailing LF. Array order is preserved. Let `J(x)` be those JSON bytes and `D(b)` be `sha256:` followed by the lowercase hex SHA-256 of exact bytes `b`. Corpus and profile identities are the digests of their raw content.

1. Caller manifest fields are `role=caller`, `feed=feed-client`, `name=ledger-client`, `version=1` (string), and `content_sha256=D(caller content)`. Caller identity is `feed-client/ledger-client/1@` followed by the digest of the manifest JSON bytes.
2. Provider manifest fields are `role=provider`, `name=ledger-provider`, `version=1` (string), and `content_sha256=D(provider content)`. The only differing manifest field is `feed`, respectively `feed-a` or `feed-b`. Provider identity is `<feed>/ledger-provider/1@` followed by the digest of the corresponding manifest JSON bytes. The full provider identities and manifest digests differ, while both cases use the identical supplied provider content bytes and content digest.
3. For each provider, build scope object `S` with exactly `caller="status-client"`, `profile=D(profile bytes)`, `ingress="fixture-transport"`, `entrypoint="status.read"` and `packages={"caller":<caller identity>,"provider":<provider identity>}`. The single shared ordered pair list `P` is `[{"target":"status","operation":"read"}]`. Build fixture object `{"scope":S,"pairs":P}`.
4. Build permission object with exactly `caller=S.caller`, `package=S.packages.caller`, `ingress=S.ingress`, `entrypoint=S.entrypoint`, `corpus=D(corpus bytes)`, `profile=S.profile`, `provider=S.packages.provider`, `target="status"`, `operation="read"`, `pairs=P`, and `allowed=true`. Build resource object with exactly `package=S.packages.provider`, `target="status"`, `operation="read"`, `pairs=P`, `corpus=D(corpus bytes)`, `profile=S.profile`, and `available=true`. Submit both current records in every case.
5. Independently prescribe selected policy A and B as separate synthetic expectations. Policy A bytes are `J({"ledger-fixture":[{"id":"status","scope":S_A,"pairs":P}]})`. Policy B bytes use `S_B` in the same definition. The authority and ID are intentionally identical so the old reference exists while scope differs. Neither policy is derived from the modeled permission/resource records.
6. For each case select `{"context":C,"scope":S,"pairs":P}` separately from the envelope. Context `C` has exactly `corpus=D(corpus bytes)`, `profile=D(profile bytes)`, `policy=D(selected policy bytes)`, and `inputs` mapping the five names `status-fixture`, `caller-package`, `provider-package`, `permission`, and `resource` to the digests of their exact selected raw JSON bytes. Build envelope `{"kind":"readonly-assessment","version":2,"context":C,"reference":R,"verdict":V}` where `R` and `V` are assigned below. Submission of envelope context merely echoes the externally supplied selection.

[Public byte-binding and scope contract](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/v2_adapter.py#L22-L114)

## Predeclared results

`R` when present is `{"authority":"ledger-fixture","id":"status"}`. The non-null verdict is exactly `"intended_access"`. Each old-policy case uses the exact A policy bytes, rebuilt B fixture/permission/resource bytes and B provider manifest, a selection independently binding those bytes, and a matching envelope context. No other authorities are selected.

| Case | Provider and gate inputs | Selected policy | Envelope reference and verdict | Expected public outcome |
|---|---|---|---|---|
| A, original-feed positive | A | A | Present | allow, assessed |
| B, migrated-feed positive | B | B | Present | allow, assessed |
| B, stale policy without assertion | B | A | Both null | allow, unassessed |
| B, stale policy with assertion | B | A | Present | `ResolutionError("inapplicable reference")` |

The full assessed result is `{"gate":"allow","policy":{"status":"assessed","verdict":"intended_access","reference":{"authority":"ledger-fixture","id":"status"}}}`. The full unassessed result is `{"gate":"allow","policy":{"status":"unassessed"}}`. API errors raise; CLI success exits 0, emits one JSON line to stdout and has empty stderr. CLI failure exits 2, emits no stdout and has stderr exactly `inapplicable reference\n`. The last two cases use identical inputs and selection with only the reference and verdict fields changed in the envelope. B with migrated policy is the positive that independently demonstrates gate prerequisites can pass with B records. The stale case asserts a scope-mismatched existing definition, so missing reference, context mismatch, digest error and authority conflict are different outcomes. [Applicability and reference ordering](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/v2_resolver.py#L86-L109)

## Public invocation and verification

Call `policy.v2_adapter.assess_status` with the selection dict and exact byte arguments `envelope_raw`, `policy_raw`, `fixture_raw`, `corpus_raw`, `profile_raw`, `caller_package_raw`, `provider_package_raw`, `caller_content_raw`, `provider_content_raw`, `permission_raw` and `resource_raw`. For CLI use the disposable consumer checkout and exact file paths as follows.

```sh
python3 -B -m policy.v2_adapter --family status \
  --selection <selection.json> --envelope <envelope.json> --policy <policy.json> \
  --corpus <corpus.bin> --profile <profile.bin> --fixture <fixture.json> \
  --caller-package <caller-package.json> --provider-package <provider-package.json> \
  --caller-content <caller-content.bin> --provider-content <provider-content.bin> \
  --permission <permission.json> --resource <resource.json>
```

Angle-bracketed arguments are placeholders. The status family takes no evidence flags. If run, record input hashes, actual argv, complete result objects or error streams, exit status and timing, and compare pre/post inventories of retained artifacts and selected input bytes on success and failure. Keep generated evidence outside the consumer checkout. [CLI contract](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/v2_adapter.py#L117-L166)

The authority is fictional and chosen out of band for this oracle. This does not use real grants, ACLs, archived typed observations, the Linux libc mounts evaluator, historical v1 import/export, or a live producer. Exact byte identity establishes consistency with selected synthetic inputs. This check cannot establish provenance authentication, real policy scope, package installation, registration, or runtime behavior. Real mounts assessment still requires separate review of scope and policy authority. [Pilot scope and limits](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/138)

No adapter, resolver, test, extraction, or producer was executed in preparing this oracle.
