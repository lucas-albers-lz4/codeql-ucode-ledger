# Current-corpus first-slice inventory

Status: source-tree inventory, 2026-11-24. No extraction, installed-image,
package-selection or CodeQL result is claimed here. This follows the two
historical security baselines in claims 075 and 036 and prepares Stage 6 of
[MVP-1.md](../MVP-1.md).

## Source pins and scope

The consumer's `corpus/lock.json` has SHA-256
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
Clean detached source checkouts from that lock were inspected at:

| Repository | Full revision |
|---|---|
| LuCI | `b2e0be4b46ec0fd43394c081fa7c50657af14011` |
| OpenWrt core | `4e9642517b48bae612ff10fb72fb9199e559500e` |
| Packages feed | `07e0d16305d2b5903b37ad7913e33e18795f81a4` |

The inspected tracked trees contain 93 `.uc` files across the three
repositories, including five test or mock files, and 23 additional
extensionless, shebang or raw-mode Ucode candidates. LuCI contributes 21
`.uc` files and 12 additional candidates; OpenWrt core 39 and seven;
packages feed 33 and four. LuCI also has 33 `.ut` files, which need separate
markup routing. These are repository candidates, not an installed-file count
or a claim that every file is supported by the extractor.

The source-first selection inventory is retained under ignored
`work/stage6-first-slice-selection.json`, SHA-256
`ccf7ffad1b5701d366c98fc297d7590dc172d3144a824d9750063d0b66a23b45`.
It records 21 unique tracked source/destination pairs (18 `.uc`, three
extensionless) with Git blobs and source hashes, and one separate generator
input for `version.uc`. This path is local run preparation, not portable
evidence or a generated installed-byte assertion.

## First bounded slice

Start with LuCI `modules/luci-base` and OpenWrt `package/utils/cli`: two
source owners with 18 tracked `.uc` files and three additional candidate
entry points: LuCI's raw rpcd `luci` module and CGI launcher, and the OpenWrt
`cli` launcher. Freeze each exact source path, blob/digest, expected route and
expected extracted identity before running CodeQL. Distinguish a plain `.uc`
from `luci-base/ucode/uhttpd.uc`, which is markup sensitive; also account for
generated `version.uc` separately from tracked source.

The LuCI lock's existing `luci-ssl` profile inventory covers only 27 routes
and is not a complete LuCI corpus selection. `luci.mk` copies `ucode/` to
`/usr/share/ucode/luci` and `root/` into the install root, and substitutes
the version file. The `cli` Makefile installs `files/*` directly. Those
recipes guide a source-to-stage map, but the run must verify actual stage
bytes and qualify any generated or transformed output. A selected build
configuration and installed rootfs/IPKs are still missing, so do not claim
package installation or coverage in a deployed image.

## Source-first run gate

1. Snapshot the two clean repository revisions, lock digest, tool version,
   selected source hashes, package recipes, and route expectations. Identify
   the markup and generated cases explicitly.
2. Stage only the selected source-derived files in a disposable run directory.
   Use a fresh database, cache, temporary directory and outputs. Inspect
   extractor/build scripts before running them.
3. Compare every selected path with exact successful extraction identities,
   error diagnostics and AST entities. Report each unsupported or transformed
   path instead of dropping it from the denominator.
4. Run the resolved suite and both experimental security checks as distinct
   observations. Record exact rows and source locations, including all
   unexpected alerts, elapsed time and peak memory. An alert on this current
   slice is a triage candidate, not automatically a vulnerability.
5. Expand package owners only after this slice's route/byte mapping is
   auditable. Candidate next owners are LuCI `luci-app-ddns` and current
   `luci-app-tailscale-community`, one `.uc` each, outside the `luci-ssl`
   profile inventory. This was a first-slice suggestion only: both files were
   subsequently included in the 17-file rpcd slice of
   [claim 081](../claims/081-current-luci-rpcd-direct-shell-slice.md). They
   are no longer disjoint candidates for another coverage slice.

## First local extraction observation

The frozen oracle SHA-256 is
`3943f4cec7739867178ceb94f2ba1026d24f5379d4137bf90aff7215c51e92da`.
The initial `run/` extraction completed, but its diagnostic query failed
because locked CodeQL dependencies were absent from that run's cache; it is
retained as a failed attempt. In a new owned `run-b/`, the 21 staged source
bytes matched the oracle, extraction commands and diagnostic queries exited
zero, and the exact successful-file multiset contained all 21 paths once,
with zero extraction-error rows. A separate direct extractor route probe
recorded 20 `plain_route_selected` paths, one markup `inconclusive` path
(`usr/share/ucode/luci/uhttpd.uc`), and no excluded or uncertain paths.
The route probe is a distinct direct invocation on the same source bytes;
its receipt does not authenticate the database run. The markup file's
successful-file diagnostic does not mean its full content was modeled.

On this selected database, the resolved current default suite contained
only `ExtractionErrors.ql` and `SuccessfullyExtractedFiles.ql`; SARIF had zero
rule descriptors and zero results. The explicit OpenVPN rule returned zero
rows in 3.080 seconds. The explicit Tailscale rule was interrupted after
187.742 seconds (exit 130, 1,354,055,680 bytes peak RSS) while evaluating
its `before/2` predicate over the larger AST. That is a performance failure,
not a zero-result observation. The rule requires a query-plan fix and fresh
historical and current-slice verification before promotion or expansion.
An isolated query-plan revision at producer commit
`2dde7010e9bcf7cb445743fc48221bbfadfcaa34` later finished a
copied-database 21-file probe in 3.196 seconds with zero candidate rows and
450,052,096 bytes peak RSS. A fresh separate 13-file historical run retained
the parent/fix/control matrix. The copied-database probe is a performance
measurement, not a fresh extraction or installed-byte handoff. Independent
read-only review found that the new sink/function/file anchoring narrows
the previous matches; it also excludes same-line constructions.

OpenWrt core's `wifi-scripts` includes Ucode in a `.sh` path and has a
`CONFIG_WIFI_SCRIPTS_UCODE` selection condition. Other core packages and
feeds also acquire external source commits not established by the three
repository pins. Those cases need separate routing and acquisition records
before a broader coverage denominator can be claimed.
