# Disposable producer-owned grammar integration

The producer checkout under ignored
`work/producer-grammar-integration-20261124/producer` started clean at
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, which still matched its
GitHub `main` when fetched. Upstream grammar `main` at
`f177807675c9e6996c9368f74ee75e70cd0728a0` had only documentation
changes since the producer's locked grammar
`4a243af329fae2f4ff01e0fc80133cbab8314600`; it did not supply the
newer wifi syntax.

The disposable producer patch applies a source-only grammar/corpus change
to that locked revision, runs `npm ci`, regenerates the plain and markup
parsers with Tree-sitter 0.27.1, and runs the grammar suite. It adds a
dedicated dynamic-import expression and accepts exported functions without
a trailing semicolon. Explicitly terminated exported functions retain the
prior export-statement tree shape; an initial variant did not, so it was
revised before this candidate pack was built. The release-gate draft checks
the patch, npm lock and six generated grammar hashes, plus exact agreement
between committed and rebuilt dbscheme/TreeSitter QL bindings. Candidate
and publication bundle manifests carry the base grammar revision, patch
SHA-256 and a fingerprint of generated grammar files.

The [receipt](receipt.json) records source, tool, patch, generated and
extractor digests, exact local commands and raw log hashes. The end-to-end
bootstrap passed in the disposable checkout. Grammar tests passed 244 plain,
89 markup and 151 documentation cases. Producer `cargo test --offline
--locked` passed 12 extractor, three grammar-load and one doc test. The
offline bootstrap unit test and seven bundle tests passed. The rebuilt
macOS extractor has SHA-256
`6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b`.
Raw outputs and build/cache directories remain under ignored `work/`.

The initial receipt captures the disposable checkout before its final PR
packaging. The source patch was then rewritten with zero diff context to
avoid embedded patch-file whitespace; the regenerated parser and extractor
hashes stayed the same. The final producer commit is
`d39b1e19eb3c9cb63b493f44f2be2e95d89c17f4` in draft
[PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161).
Its Linux release gate now runs the [typed AST fixture](../mvp-grammar-syntax-smoke-20261124/README.md).
The refined pack's [corpus](../mvp-corpus-v0.6-refined-local-run/README.md)
and [historical parent/fix](../mvp-grammar-refined-historical-regressions-20261124/README.md)
reruns are tracked separately. Hosted Linux CI, installed OpenWrt bytes and
an immutable release remain open.
