# Darwin run of the v2 archive receipt boundary

The consumer CLI ran five times on 2026-11-22 at clean detached
`fe5952073eeef913fef4b3324d9541ff66426492`. The [source-first oracle](ORACLE.md)
predates execution. The [harness](run.py), [preflight](preflight.json),
[expected successful response](expected-success.json) and [result](result.json)
record the selected operation and expected and observed contract. The CLI
received the actual original claim 029 receipts from its previous run. The
new run executed the consumer only.

## Inputs and original bytes

The [input manifest](input-manifest.json) identifies all 30 staged files by
original SHA-256 and size. Selection and envelope are exact copies. Consumer
Git paths refer to the [pinned consumer tree](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/fe5952073eeef913fef4b3324d9541ff66426492).
The standalone archived source is the sole regular member of the checked-in
ZIP. The claim 029 paths refer to its [portable evidence and receipt
index](../029-typed-refactor-handoff/README.md).

Claim 029's retained portable routing and extraction copies have normalized
source paths. The CLI instead received the original bytes whose raw digests
are recorded in both claims. For each of those two files, replacing the
archive's one concrete source path with the concrete path from claim 029's
digest-verified routing decision reproduced the original claim 029 bytes
exactly. The independent extraction row matched that routing identity and
its installed suffix. The harness compared the files in memory, leaving
both inputs unchanged. The other overlapping files, including the typed
record, matched the archived bytes exactly. The raw path-bearing claim 029
files remain private local artifacts. The portable copies and original
digests do not establish execution.

## Commands and observed outputs

| Case | Wall time | Exit | Observation |
| --- | ---: | ---: | --- |
| [Archive](outputs/archival/receipt.json) | 84.3 ms | 0 | Archived observation. Gate unknown and policy unassessed. |
| [Typed-only substitution](outputs/typed-substitution/receipt.json) | 66.3 ms | 0 | Exact archive output. |
| [Extraction-only substitution](outputs/extracted-substitution/receipt.json) | 69.8 ms | 2 | Evidence byte identity mismatch. |
| [Routing-only substitution](outputs/routing-substitution/receipt.json) | 70.9 ms | 2 | Evidence byte identity mismatch. |
| [Combined substitution](outputs/receipts-substitution/receipt.json) | 58.2 ms | 2 | Evidence byte identity mismatch. |

Each output directory retains exact stdout and stderr, including empty
streams. Command receipts retain unrounded wall time and substitute
`<RUN>` and `<CONSUMER>` for the two original directory prefixes. Each
normalized receipt carries the original receipt hash. Peak memory was
unmeasured. There was no extraction, query or producer timing in this run.

For each invocation the before and after inventories were byte-identical.
The worktree and staged inventories also matched the initial inventory.
Each receipt retains the snapshot hashes and entry counts. The inventories
cover 865 worktree entries outside `.git`, 30 staged files and the empty run
temporary and cache directories. They include modes, names and file
digests. Full inventories remain local. The adapter subprocesses ran with
Darwin's `sandbox-exec` profile denying file writes. Setup, Git and receipt
writing ran outside that profile. HOME was inherited. Inventory comparison
is limited to the specified paths and observation points.

The local positive recorded the Darwin guard's unknown gate and unassessed
policy, with the retained typed assumptions and unknowns and the platform
limit. The [exact-head Ubuntu M2 job](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45080021190/job/137385832351)
is separate upstream baseline evidence. The five substitutions above were
observed on Darwin. The run establishes no live device result or authority
outside the selected policy fixture.
