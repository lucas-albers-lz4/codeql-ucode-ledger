# Claim 026: synthetic v2 provider feed and policy scope

**Status:** Demonstrated, for the four synthetic cases and pinned consumer below.

**Scope:** A selected provider identity changes from feed A to feed B while package name, version and content remain the same. Current synthetic B permission and resource records satisfy the status gate; an existing assertion scoped to A is inapplicable to B. This informs whether an expectation must be reconsidered after a provider identity change.

**Out of scope:** Real grants or authority, package provenance or installation, runtime access, a producer query or live handoff, and any claim of security or completeness.

## Revisions and context

The consumer was `codeql-openwrt` [48c6a65b7578234644c6b06780fc82ccf6d61a8b](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/48c6a65b7578234644c6b06780fc82ccf6d61a8b), clean in the source and disposable checkout. No ucode producer or real corpus was used. The [source-first oracle](../evidence/026-v2-feed-policy-scope/ORACLE.md) specifies the exact synthetic fixture and independent policy selection. The [adapter](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/v2_adapter.py) binds selected bytes and computes the synthetic gate; the [resolver](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/48c6a65b7578234644c6b06780fc82ccf6d61a8b/policy/v2_resolver.py) requires exact scope applicability. The [pilot issue](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/138) retains the real-scope boundary.

## Evidence and controls

The two providers share package content and differ in feed and hence manifest digest and identity. The fixture, selection, permission and resource bind the appropriate provider. A and B policies are independently prescribed synthetic expectations under the same authority and ID; B with stale A policy retains that existing reference but changes the selected scope. The last two cases have identical inputs and selection except for the submitted reference and verdict. Exact bytes, results and inventory receipts are preserved in the [run evidence](../evidence/026-v2-feed-policy-scope/README.md).

| Case | API wrapper and CLI observation |
|---|---|
| A provider, A policy, reference | Gate allow; assessed `intended_access` |
| B provider, B policy, reference | Gate allow; assessed `intended_access` |
| B provider, A policy, no reference | Gate allow; unassessed |
| B provider, A policy, reference | `ResolutionError: inapplicable reference`; CLI exit 2 |

Both positive cases and the stale unasserted case exited 0 at both boundaries. The error is resolved before gate computation; the otherwise identical unasserted case demonstrates the gate can pass. The API wrapper catches and serializes the error; its exit and stdout are not a direct API protocol. All expected input bytes, output streams and statuses matched the independent oracle, and recorded pre/post inventories matched after all eight invocations.

## Run limits

Run B on 2026-11-22 used Python 3.15.2, Git 2.56.1 and macOS sandboxed adapter subprocesses. HOME was inherited, not owned by the run; setup Git ran outside the sandbox. The retained record describes the sandbox probes and their limits. The prior unsandboxed run A is not a separate source of independent-model corroboration. No extraction, CodeQL query or fresh producer ran. Hashes bind selected synthetic bytes but do not authenticate the execution or their origin. At this run's consumer pin, the real policy scope and authority had not yet been independently reviewed.

At a later consumer revision, the owner reviewed a narrowly scoped mounts
expectation and closed issue #138. That later decision does not change this
synthetic run; [claim 030](030-v2-archive-receipt-boundary.md) examines a
different boundary at the newer consumer.
