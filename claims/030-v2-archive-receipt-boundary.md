# Claim 030: v2 archive receipt boundary

**Status:** Demonstrated for the selected v2 CLI, five cases and Darwin run.

**Scope:** Determine whether the original extraction and routing receipts
from claim 029 can accompany its byte-identical neutral typed record in the
pinned v2 `setBlockDetect` archive adapter.

**Out of scope:** A new extraction or producer-to-consumer handoff, an
observed Linux result for these five cases, live execution, registration,
or runtime authorization.

## Revisions and evidence

Consumer [`fe5952073eeef913fef4b3324d9541ff66426492`](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/fe5952073eeef913fef4b3324d9541ff66426492)
was clean in a disposable checkout. [Claim 029](029-typed-refactor-handoff.md)
previously generated its neutral record and receipts at producer
`6010ff2c0f101f7629c6fe117a421f671c311a2b` and imported the record through
strict v1 at consumer `48c6a65b7578234644c6b06780fc82ccf6d61a8b`. Both
packets identify LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
[OpenWrt #138](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/138)
owns the archive pilot and is closed. Upstream already tests altered
evidence digests and a coherent synthetic path change at the private
decoder. The present run submits original claim 029 receipts via the public
CLI. [Upstream PR #144](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/144)
retains a separate strict v1 handoff from a later producer.

The [source-first oracle](../evidence/030-v2-archive-receipt-boundary/ORACLE.md)
fixed the exact archived scope, selected policy, alternate inputs and
expected results. The archive and claim 029 contain the same source bytes,
one projected effect row at `532:21–532:68`, zero extraction diagnostic
rows, and identical typed output. Both extraction and routing receipts
identify the same installed path and differ byte-for-byte only in the
concrete source path. The exact originals were used for the substitutions.

## Observed results

The complete archive exited 0 and returned the archived observation with
both gate fields `unknown` and policy `unassessed` on Darwin. Replacing only
the typed file with the actual claim 029 export produced identical stdout.
Replacing the extraction receipt or the routing receipt independently
exited 2 with empty stdout and `evidence byte identity mismatch` on stderr.
Submitting both original receipts together produced the same rejection.
Selection, policy, archive ZIP and all other evidence remained fixed. The
adapter checks those input digests before interpreting the routed source or
evaluating the modeled gate.

The [portable run record](../evidence/030-v2-archive-receipt-boundary/README.md)
retains exact streams, normalized commands, input and inventory digests,
and phase timing. The five calls took 58–84 ms each. Python 3.15.2 ran the
adapter on macOS arm64 under a write-denying subprocess sandbox. The
checked worktree, staged files, temporary directory and cache inventories
matched before and after every call. HOME was inherited and setup ran
outside the subprocess sandbox. The
[exact-head Ubuntu M2 run](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45080021190)
covers the upstream Linux baseline. The original claim 029 receipt
substitutions were observed on Darwin. The result establishes the pinned
archive identity boundary for these inputs while leaving runtime behavior
outside the claim.
