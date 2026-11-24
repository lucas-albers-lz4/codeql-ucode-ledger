# Disposable producer parser probe

This run used a local grammar override based on pinned grammar commit
`4a243af329fae2f4ff01e0fc80133cbab8314600`, with the exact changed
grammar and corpus [source patch](grammar-source.patch). The override is
distinguished from that base SHA by its diff digest and generated-file
hashes in the [normalized receipt](receipt.json). The disposable producer
checkout started clean at merged commit
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; its generated dbscheme,
TreeSitter QL bindings and focused diagnostic queries remain local and
uncommitted. The producer was compiled against the modified grammar; the
generated schema adds a `DynamicImportExpression` relation in both plain and
markup ASTs.

The [source-first oracle](source-first-oracle.json) was prepared before the
CodeQL database run and names two formerly failed OpenWrt wifi sources plus
changed `wireless.uc` and new `wireguard.uc` controls. All four exact source
and staged SHA-256 values and Git blobs were checked at OpenWrt
`bce40f6a15c273778061e8fceced7b9e0f58d99b`. A fresh run-owned macOS
database indexed and finalized. The successful-file query returned all four
identities once each; extraction errors were empty. The
[identity table](exact-identities.csv) records source, route and result
multiplicity. A separate direct extractor routing receipt on the same staged
bytes recorded the expected four plain routes; it is not the database
execution receipt.

Focused AST queries observed one `DynamicImportExpression` with a `String`
source child at `mac80211.uc:17:15–17:33`, and three distinct exported
function declarations in `utils.uc`, including semicolon-free `board_wlan`
at lines 74–76. The receipt retains entity IDs and ranges. This corrects an
earlier assumption: `rename_phy_by_name` is an ordinary function at line 78,
not an exported one. Failed setup attempts, including a pack assembly error
and wrong CodeQL dependency-cache placement, are recorded separately from
the final zero-exit database and query phases. Cargo build exited zero in
16.860 seconds; the macOS `/usr/bin/time -l` wrapper then exited 1 because
its memory sysctl was denied, so peak RSS is unavailable.

This is a focused prototype. No full 128-file run, default suite, SARIF,
installed-byte comparison, Linux result, runtime validation or release was
established by it. The original [v0.6 failure](../mvp-corpus-v0.6-local-run/README.md)
remains the result for merged producer bytes.

A later [local producer regression run](cargo-test-receipt.json) executed
`cargo test --offline --locked` against this modified checkout with its
isolated Cargo home and target. It exited zero: 12 extractor unit tests,
three grammar-load tests and one doc test passed. The receipt hashes raw
stdout/stderr retained under ignored `work/producer-new-wifi-20261124/run`.
This supplements the focused and [full v0.6 prototype scan](../mvp-corpus-v0.6-prototype-local-run/README.md);
it is not a Linux or release regression.
