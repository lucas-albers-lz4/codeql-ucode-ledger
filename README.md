# codeql-ucode-ledger

A small, independent workspace for examining **specific coverage claims** across [codeql-ucode](https://github.com/lucas-albers-lz4/codeql-ucode) and [codeql-openwrt](https://github.com/lucas-albers-lz4/codeql-openwrt).

The ledger connects a claim to the source it concerns, the analyzer behavior it relies on, the tests or observations that support it, and what remains unknown. It is not an overall coverage percentage or a list of security guarantees.

## Start here

The initial claims are **proposals, not completed results**:

1. [Explicit staged-root extraction](claims/001-staged-root-extraction.md): the intended extensionless ucode file is selected and extracted cleanly.
2. [getBlockDevices query observation](claims/002-getblock-query.md): a narrow source shape yields the expected query row, with meaningful controls.
3. [getBlockDevices producer–consumer handoff](claims/003-getblock-handoff.md): a freshly generated table is validated and imported by the OpenWrt consumer without overstating its meaning.

Together these move from source selection through extraction, query, and consumer, but each claim stands on its own evidence. Start with **001**, then **002**, then **003**. See [the claim template](claims/TEMPLATE.md) before adding a result.

## Scope and status

- **Proposed:** a question or expected contract; no current run is claimed.
- **Demonstrated:** supported by an identified run, exact revisions, commands, expected identities, observed outputs and relevant controls; scoped to those inputs.
- **Partial:** some, but not all, required evidence exists. State exactly what is missing.
- **Unknown:** insufficient evidence; this is not a negative result.
- **Deferred:** intentionally out of scope or owned elsewhere, with a reference and revisit condition.

A clean extraction does not prove semantic accuracy; a query result does not prove runtime reachability; an empty result does not establish safety; a matching fixture does not prove a fresh producer execution. Separate language support, analyzed source coverage and policy interpretation. Do not infer device behavior, authorization, taint, or vulnerability from a source observation alone.

## Working on another server

Clone this repository and create **separate disposable checkouts** of the two projects. Do not use active development checkouts or share writable CodeQL databases between runs. Each run needs its own workspace, database, outputs, and enough disk, memory and CPU. Local run artifacts belong under `work/`, which is ignored by Git; selectively retain small, reviewed evidence separately when useful. Do not commit credentials, raw private data, generated databases or unexplained host paths.

This repository is a documentation and investigation starting point. **It does not yet contain an automated end-to-end runner or CI.** Follow the linked project instructions for the exact selected revisions; inspect scripts before running them. Build and test commands can modify their working directory, invoke network operations and consume substantial resources. Never run an adapter that rewrites reports against an active checkout: use a disposable consumer copy.

### Reference pair

The initial source links refer to a **historical reference pair**, not a recommendation to use stale code for every run:

| Repository | Reference commit |
|---|---|
| `codeql-ucode` | `7a1ded90962cc85a3e3a94949584c64214426aed` |
| `codeql-openwrt` | `a8bdef3c22c8d5ba9999baa978052b59bd22907e` |

When you start a new run, choose and record both commits explicitly. Fetch the branches first, then create detached checkouts at the chosen full SHAs in a private workspace. For example, after cloning each project into `work/codeql-ucode` and `work/codeql-openwrt`:

```sh
git -C work/codeql-ucode fetch origin
git -C work/codeql-openwrt fetch origin
git -C work/codeql-ucode checkout --detach <ucode-commit>
git -C work/codeql-openwrt checkout --detach <openwrt-commit>
git -C work/codeql-ucode rev-parse HEAD
git -C work/codeql-openwrt rev-parse HEAD
```

Replace the placeholders; do not paste the example unchanged. Record dirty state, tools/versions, fixture or corpus pins, commands and actual outcomes. Recheck the relevant source contracts and existing issues at those commits: the reference pair may differ from current `main`. Comparing different pairs requires an explicit delta review; an earlier pass does not automatically transfer.

## Optional model roles

For model-assisted work, keep the split simple:

- **Luna:** bounded mechanical collection, inventories, mapping paths to existing tests, and organizing run receipts. Check its output against the actual sources or commands.
- **Terra:** coordinate the paired pins and isolated runs, verify claims and reproduce candidate results, reconcile overlap with existing issues, and maintain the ledger.
- **Sol:** assess difficult semantic questions, choose discriminating controls, judge evidence boundaries, and synthesize the strongest unresolved coverage questions.

These are task roles, not separate mandatory stages or a requirement to run three models for every claim. Start with the simplest useful workflow. Resolve and smoke-test the desired model route at execution time; do not silently substitute another model. A second pass by the same model is fresh review, not independent-model corroboration.

## Relationship to the projects

This is an incubation workspace, not a submodule or a new authoritative implementation. Reuse existing project tests and issues. As the work matures, move producer-only regressions to `codeql-ucode` and consumer-only regressions to `codeql-openwrt`; decide separately where genuinely paired integration tests belong. Do not duplicate a finding already owned by an open issue.
