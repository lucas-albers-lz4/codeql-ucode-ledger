# Claim 025: Plain and markup AST roots in one pinned LuCI stage

**Status:** Demonstrated for the selected 21 upstream source files and three
controls.

**Decision:** Can one database preserve the selected profile's file identities
and produce exactly one root of the expected AST kind for every staged file?
The result establishes root kind and multiplicity for the selected source
bytes. Rendering, AST fidelity below the root, flow, and consumer integration
remain outside the claim.

## Revisions and source selection

The disposable producer tracked tree was
`0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`, with local untracked ledger
queries. CodeQL was 2.27.4 on macOS arm64. The reused extractor pack
matched the recorded files from the build at
`8375887ed14825dd59addbfd0df43616d9e684fb`.
[Pack and lock provenance](../evidence/025-mixed-profile/provenance.json)

The source was clean LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
The selection used the OpenWrt `luci-ssl-25.12` inventory and lock from
`fa745e1c62f1f558bd8f6659a1d1040bb569cb96`. Those files were unchanged
through inspected consumer main `5f8bd2658483c0c06c0ebfced98fd09b1f57aeff`.
The [oracle](../evidence/025-mixed-profile/source-first-oracle.json) records
each mode, Git blob, digest, and source-to-stage mapping.

Nine plain files include the extensionless rpcd plugin and shebang CGI.
Twelve markup files include `uhttpd.uc` and eleven `.ut` templates. The
stage omits generated `version.uc`, two bootstrap symlinks, and three shell
helper entries. The copies preserve upstream bytes at expected install paths.
LuCI's installation substitutes version and resource tokens in two selected
headers. No configured installation was performed.

## Evidence and controls

The three controls comprise a mixed template, a template with a tag-like
string, and a plain program with a tag-like string. Both template controls
produced a markup root. The plain string control produced a plain root. Their
root counts test parse-mode separation for these inputs.

The [routing and diagnostic outputs](../evidence/025-mixed-profile/outputs/)
match all 24 predeclared paths. Every successful-file identity appears once.
The extraction-error and all-diagnostic tables were empty. Routing selected
10 plain and 14 markup paths, including the controls. All 14 markup rows
retain `inconclusive` / `markup_not_modeled`.

The [root query](../evidence/025-mixed-profile/queries/MixedProfileRootCounts.ql)
counts typed root entities by file. All 24 exact path and count tuples matched.
Ten files have one `Program` and zero `Markup` roots. Fourteen files have
zero `Program` and one `Markup` root. The
[archive check](../evidence/025-mixed-profile/archive-check.json) verified
the 24 path and byte-hash pairs in the finalized database's source archive.

## Run record

The November 22, 2026 run indexed the stage in 0.720 seconds and finalized
the database in 1.403 seconds. The first root query exited 2 after 1.109
seconds with unresolved imports from its initial pack context. The identical
query ran inside the disposable producer query pack and exited 0 in 1.624
seconds with peak RSS 353,796,096 bytes. Decode exited 0 in 0.217 seconds.
The [command receipt](../evidence/025-mixed-profile/commands.json) records
each phase's arguments, statuses, and measurements. It verifies run-local
temporary and extractor/cache paths and explicit package search paths.
The scripts inherited `HOME` and the receipt does not establish a run-owned
override.

The result extends separate plain and markup extraction observations to one
database. The consumer was not invoked, and its integration remains with
[OpenWrt #68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68).
