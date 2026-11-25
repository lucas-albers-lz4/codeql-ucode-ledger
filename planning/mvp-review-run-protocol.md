# MVP review and run protocol

Status: active process update, 2026-11-25. Use with [AGENTS.md](../AGENTS.md)
and the gates in [MVP-1.md](../MVP-1.md). This is a small working packet for
changes that cross producer, consumer, release, package-byte or queue trust
boundaries. A routine documentation or inventory edit does not need every
step.

## Route the smallest capable task

| Work | First route | Review route |
|---|---|---|
| Pinned inventories, PR/CI status, receipt arithmetic, exact path and hash comparison | `gpt-6-luna` | Verify mechanically against source/raw receipts; escalate a semantic discrepancy |
| Workflow coordination, package preflight, test wiring and non-security implementation | `gpt-6.1-terra` when its exact route works | `gpt-6.2-sol` for a difficult boundary or final decision |
| Defensive security semantics, model/flow identity, shell or queue trust design | `gpt-6-sol` | Independent `gpt-6.2-sol` review when a boundary decision matters |
| Final promotion, release or evidence-scope decision | Primary owner with `gpt-6.2-sol` review when needed | Check the current exact head and raw gate evidence |

These are options, not mandatory stages. Smoke-test an exact route before
relying on it. During this review, `gpt-6.1-terra` returned a Daybreak 403;
a second trivial read-only route smoke also returned the same 403. A
`gpt-6.2-sol` final document-review attempt returned the same Daybreak 403.
None produced a review and none may be relabeled as one. Continue
with the primary owner or explicitly choose another available route and
record the change. A requested model name is an assignment, not independent
server-side model attestation. Do not run heavy scans concurrently against
shared writable paths.

## Before implementation or a costly CI run

Write a compact review packet in the PR, claim or run notes:

1. **Decision and owner:** the exact analysis or integration decision, owning
   issue, proposed gate and what remains outside it.
2. **Revisions:** full clean/dirty producer, consumer and source SHAs; PR base,
   head and tree; relevant tool, lock and package pins. List only the changed
   contracts that can invalidate prior evidence (routing/grammar, model,
   query/suite, consumer schema, source/install recipe or workflow).
3. **Oracle and controls:** source-derived expected identities and
   multiplicity before output, route precedence including shebangs, one
   positive and one eligible near miss. For a model, include a real
   source-shaped missed form and preserve existing public QL API. For a
   package, distinguish source, stage, IPK and root installation.
4. **Gate map:** name the exact local check, the hosted check that executes it,
   expected artifacts, release/live dependencies and skipped jobs. An
   unwired local script is not a hosted regression; a skipped live job is not
   a pass. Budget expected wall time, disk and memory before a heavy build.

For an issuer, queue or artifact-custody change, add a trust-boundary map:
which bytes are untrusted, who can write them, when writers stop, which
paths are opened first, where credentials live, and what binds the event,
control, release lock, run/attempt and queue reservation. Review that map
before implementing the writer or signer. Test alias and special-file
rejection **before the first read or write**, exclusive output creation,
hardlinks, exact directory contents, tracked symlink exceptions, stale
reservations and forged-but-valid-format receipts.

## Review on the exact candidate

Give a reviewer the packet, the full diff, affected caller/API definitions,
source fixtures, pre-output oracle, raw or retained receipts, command/status
log and the known evidence limit. Ask for concrete counterexamples and file
locations. A review of a previous head or a synthetic fixture does not
authenticate a changed head or live execution. Record each defect as:
assumption → counterexample → added control → exact check that closed it.

Run small local controls first; wire a meaningful focused check into hosted
CI before paying for the full gate. Once a review is clean, run the required
exact-head hosted gate. Before merging or promoting, re-fetch PR state and
compare base/head/tree, check every required conclusion, inspect the actual
artifact and distinguish local, hosted offline, released live and consumer
handoff evidence. Do not promote a model merely because its testing query
returns rows.

## Revalidation and expensive runs

When a base or dependency changes, compare its touched contract files to
the packet. Keep unaffected historical evidence scoped to its original
revision. Re-run the smallest affected source/control check first, then the
required hosted gate on the new exact head. A shared `Models.qll` change
invalidates a query result that imports it; a tool or package-install delta
invalidates the corresponding byte comparison. Avoid rebasing draft stacks
merely to make their checkmarks fresh while their release lock is null.

For builds, use one run-owned database/output/cache set per attempt and poll
the live handle before considering a retry. Capture GNU time and resource
receipts per phase. The first independent `wifi-scripts` y/n build spent
roughly 18 minutes per host-tools phase and 32/31 minutes per toolchain,
versus about one minute per package. Its output is the baseline for future
optimization. Copying verified downloads into a separate run-owned download
directory may be measured; do not copy compiled toolchains or staging roots
without a relocation/configuration audit and a byte comparison against that
baseline. Keep large logs, IPKs and databases in ignored `work/`; commit only
small reviewed receipts with raw-artifact provenance and limits.

## What changed this protocol

- The first Wi-Fi route oracle missed shebang precedence in three `.uc`
  files; a corrected source-first oracle and fresh run resolved it.
- Producer model tests passed for direct named imports while real Wi-Fi
  calls used namespace imports. Source-shaped near misses exposed the gap.
- An initial namespace model broke the existing `NamedCall` API and missed
  bracket/delete writes; independent review added compatibility and mutation
  controls before treating it as a candidate.
- Consumer freeze PR #170 passed initial unit tests, but independent review
  found tracked symlink, pre-read alias, exclusive-output, graph-binding and
  stage-inventory gaps. Reviewing the trust map and actual first I/O earlier
  would have avoided several correction cycles.
- A queue MAC over a fabricated digest still passed the offline queue
  prototype; only a trusted same-job issuer can authenticate scan evidence.
- The paired Wi-Fi build proved conditional IPK member bytes but took about
  104 minutes end to end and did not scan them with CodeQL. Do not convert
  that result into full Gate 6 or Gate 7 coverage.
