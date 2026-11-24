# Claim 075: historical OpenVPN candidate-query baseline

**Status: Demonstrated for the selected source files, controls, producer pin and local run.**

## Claim and boundary

At clean producer `6010ff2c0f101f7629c6fe117a421f671c311a2b`, the
testing-tagged `ShellInjection.ql` returns no candidate for the upstream LuCI
OpenVPN `generateKey` source in either its vulnerable parent or actual fixed
revision. Each file extracts exactly once with zero extraction errors. An
independent AST witness locates `cl_meta` and the line-77 `popen` call in both.
The same query returns the predeclared exact positive-control tuple and no row
for an eligible request-argument/constant-sink near miss. This is a bounded
current-model gap, **not** a detection of the historical vulnerability or
recognition of its fix.

The maintainer [advisory](https://github.com/openwrt/luci/security/advisories/GHSA-pm9w-522m-8rrh)
attributes the historical issue and its preconditions; this run tests static
source/query behavior only. The [fix commit](https://github.com/openwrt/luci/commit/e4ff45ecbc6ad212951815c8c99b2749fbd7de6b)
wraps `req.args?.cl_meta` in `shellquote(...)` at line 71. The query model
requires a receiver literally named `request`, while this source uses `req`.
This source inspection explains the observed absence as a model prerequisite;
it does not establish that broadening the receiver alone would find the path
or distinguish the fix.

## Pins and source-first expectations

| Input | Git revision and path | SHA-256 | Predeclared target |
|---|---|---|---|
| Vulnerable parent | LuCI `b45584b4e6068b9b096872dd02494a048d869c36`, `protocols/luci-proto-openvpn/root/usr/share/rpcd/ucode/luci.openvpn.uc` | `051c8162f826683333e11264615806df5ab08415676c0bd098921cb1b05af991` | `cl_meta` line 71, columns 115–131; `popen` line 77, columns 16–25; no current candidate expected. |
| Fixed | LuCI `e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`, same path | `6593792678951fd500c2b090d17d9e500a05a642cfb996ee02c1649473152410` | `cl_meta` line 71, columns 126–142; same `popen`; no current candidate expected. |
| Controls | Producer `6010ff2c0f101f7629c6fe117a421f671c311a2b`, byte-exact `taint_pos` and `taint_neg` fixtures staged with `.uc` names | See [source-first oracle](../evidence/075-20261124-openvpn-baseline/source-first.json) | One exact `taint_pos.uc` tuple; no `taint_neg.uc` row. |

The source-first oracle was prepared before running CodeQL and copied byte for
byte into portable evidence. The advisory's earlier affected revision has the
same file bytes as the selected fix parent. The staged paths represent pinned
upstream source at an installed-style path; no package build or actual
installed-byte comparison was performed. The full source/fixture Git blobs,
hashes, control tuple and expected route are in the oracle.

## Local run, 2026-11-24 UTC

The local CLI was CodeQL 2.27.4 at
`/Users/lalbers/gitroot/ucode/.tools/codeql-2.27.4/codeql/codeql`; the host was
macOS arm64 with 16 GiB RAM and 127 GiB free disk at preflight. The selected
producer checkout was clean. A compatible extractor pack built at
`8375887ed14825dd59addbfd0df43616d9e684fb` was copied into the fresh
run; the selected producer and pack-build revision had no diff in `Cargo.lock`,
extractor metadata or the inspected build/grammar scripts. The copied
extractor SHA-256 was
`c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
Build provenance and all raw output remain under ignored
`work/mvp-openvpn-baseline-20261123-b/`; that local directory is **not** a
portable reference. [The reviewed receipt](../evidence/075-20261124-openvpn-baseline/receipt.json)
normalizes it to `$RUN`, and [the command log](../evidence/075-20261124-openvpn-baseline/commands-normalized.json)
records every command, exit and phase duration. Each of parent, fixed and
controls had its own database, stage, writable cache and temporary directory.
`HOME` remained inherited under the environment rule; no shared writable
database or cache was used.

For each stage the actual sequence was `codeql database init`, `index-files`
with `--include=**/*.uc`, `finalize`, the successful-file and extraction-error
diagnostic queries and decodes, then `ShellInjection.ql` and CSV decode.
Parent and fixed additionally ran an AST witness query narrowed to the
predeclared line-77 sink. All commands in the completed run exited 0. A
broader first witness also enumerated three same-file `popen` calls; its
[query text](../evidence/075-20261124-openvpn-baseline/OpenvpnAstWitnessBroad.ql)
and the [narrowed target query](../evidence/075-20261124-openvpn-baseline/OpenvpnAstWitnessTarget.ql)
are preserved separately because the run-owned query file changed between
these two commands. The receipt records their hashes. A
separate initial preparation attempt failed its first `database init` with
exit 2 because the database parent directory did not exist; it made no query
result and was not counted as a pass. The run script was corrected and a fresh
run path was used.

CodeQL also warned on each `ShellInjection.ql` query run that a problem query
must select an even number of columns; this testing query selects seven. The
BQRS/CSV commands exited 0 and produced the rows below, but the warning is a
separate blocker for treating this query as a SARIF alert. The raw stderr also
has a low-heap query-loading cache warning. Both are retained in the receipt.

| Stage | Successful files | Extraction errors | Target AST source/sink witness | Candidate rows |
|---|---:|---:|---|---:|
| Parent | exactly `luci.openvpn.uc` once | 0 | `MemberExpression` 71:115–131 and `CallExpression` 77:16–25, exactly one target pair | 0 |
| Fixed | exactly `luci.openvpn.uc` once | 0 | `MemberExpression` 71:126–142 and same line-77 sink, exactly one target pair | 0 |
| Controls | exactly `taint_pos.uc` and `taint_neg.uc` once each | 0 | Source controls in oracle; no target claim | 1 |

The sole control tuple was exactly
`(MemberExpression, "shell-injection candidate via popen in taint_pos.uc", CallExpression, popen, probe, 8, 8)`;
`taint_neg.uc` contributed no row. Post-run hashes of all four staged files
still matched the source-first oracle. The run's phase wall times and macOS
`time -l` peak resident bytes are in the receipt. For example, parent index,
finalize and candidate query took 0.732 s, 1.208 s and 2.621 s respectively;
the candidate query peak RSS was 762,085,376 bytes. These are tiny selected
sources, not an estimate for a full LuCI or OpenWrt scan.

## What remains

The baseline supports an actual selected-query miss with a working positive
control and target AST identities. It does not show a default-suite alert,
trusted quote-helper semantics, complete flow, Linux CI, SARIF, consumer
acceptance, runtime reachability or exploitability. The two historical cases
and the longer release path are in [MVP-1.md](../MVP-1.md). Before promoting a
check, establish receiver binding, the source-to-command path and a
discriminating quote barrier, then rerun vulnerable/fixed and eligible controls
through the default suite and fresh downstream CI.
