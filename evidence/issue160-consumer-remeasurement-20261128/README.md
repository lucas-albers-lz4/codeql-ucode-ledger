# Issue 160 / OpenWrt 68: source-staged consumer observation

This packet summarizes one independently reviewed local observational run for
[producer #160](https://github.com/lucas-albers-lz4/codeql-ucode/issues/160)
and [OpenWrt #68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68).
It changes no consumer contract or gate. The selected 12 paths are source files
projected to installed-style paths, not observed installed-image bytes. This is
not a release-binary, trusted-execution, runtime, dataflow, authorization or
security-coverage claim.

[identities.json](identities.json) records each selected LuCI source path, Git
blob, source SHA-256 and byte count, projected installed path, observed
producer route, fresh consumer classification and inventory lookup identity.
[phases.json](phases.json) records the 17 child command vectors, environments,
exit codes, elapsed times and output hashes; entries are sorted by name, not
execution order. Private absolute path prefixes are
replaced by `$RUN`, `$RUNTIME`, `$PLAN`, `$CLI`, `$CLI_DIR` and `$PYTHON`; raw
logs and databases remain local. [artifact-hashes.json](artifact-hashes.json)
records raw artifact hashes and lengths. These hashes bind the retained bytes;
they do not authenticate execution. The runner did not retain a wall-clock
start timestamp or peak RSS, so neither is asserted here.

The 12 inputs are the historical `luci-ssl-25.12` selection: 11 `.ut` files
and `uhttpd.uc` from LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`. Each
regular 100644 source Git blob and SHA-256 was checked before staging; the
historical source-to-installed manifest SHA-256 is
`8f84bf665718d36972c8b4f3d8648e1bd0c660b016cca80fa430453bb1b47a8f`.
Source, private stage and source archive identities were checked. The CLI
explicitly indexed that stage with `--include=**/*`; this does not test every
default discovery entrypoint.

Producer source was `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, the revision
named by the owner request, rather than later producer main. The private macOS
extractor pack was copied from the previously audited [33-file run](../issue160-20261124-markup-33-reconciliation/README.md).
Its extractor binary SHA-256 is
`d24a86982905079aa50a500ecd8721719beef6a39ccce7501b2e312f6a0f72a3`.
That build materialized a tree-sitter dev-dependency change from `0.27.1` to
`=0.26.8`; it is not an unmodified release build. Physical CodeQL CLI 2.27.4
launcher SHA-256 was
`bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
The full CLI distribution was not independently authenticated. The copied QL
workspace, pack and ordered dependency inputs were verified before and after;
per-query resolver, library-path and private compilation-cache checks preceded
database initialization.

All 12 producer routing rows matched their staged identities: 11 had reason
`ut_markup_extension`; `uhttpd.uc` had `markup_tag_content`. Every producer
row was `markup`, `inconclusive` / `markup_not_modeled`. The decoded
`SuccessfullyExtractedFiles` query returned one exact row per selected path;
`ExtractionErrors` returned zero rows. These queries cover their stated
source-relative extraction and parse diagnostics, not all possible failures or
full AST fidelity. No markup AST identity or substitution query was run.

Consumer source was OpenWrt
`44d19d7179b623a66ffdeb66f310d1119c1787c6`; its classifier and recorded
inventory blobs matched the historical reference. The profile inventory analysis
revision was `inventory:luci-ssl-files-v1`; its corpus revision is the SHA-256
of `corpus/lock.json`,
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
The runner called the actual
`build_records`, `find_routing_record` and `classify_installed` functions and
joined each fresh staged path to its producer route and consumer inventory
identity. The 11 `.ut` inputs returned `markup` / `.ut` / rule 2; `uhttpd.uc`
returned `markup` / `tagged markup content` / rule 4. Their recorded consumer
evidence status remained `inconclusive`. The separate existing profile
validator was applied to the fresh source, stage, route and diagnostics as a
comparison; the historical-admission validator was not used to admit a new
observation.

As a classifier-only negative, the runner removed the leading `{%` from the
`uhttpd.uc` content in memory and required `plain` / `.uc/.ucode` / rule 5.
The run passed that check; its separate JSON retains the expected tuple, not a
separately captured actual return value. It changed no staged file or producer
database. The check isolates the content discriminator for this selected input;
it establishes no parser or security behavior.

All 17 recorded child commands exited 0 and the input postguard passed. Both
check-only compiles warned that the requested 2048 MB was increased to 2638 MB;
both diagnostic evaluations warned that stage caching was disabled with a
1256 MB maximum heap. The independently reviewed observation retains these
warnings; it is not combined with the earlier 33-file run. Historical
`629a708` and the reported 641/641 remain unverified, claims 052 and 056 remain
blocked, and the deferred markup-dataflow and dispatcher gates remain intact.
