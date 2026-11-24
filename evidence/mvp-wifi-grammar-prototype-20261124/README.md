# Disposable grammar prototype for newer wifi Ucode syntax

The prototype is under ignored `work/grammar-new-wifi-20261124/tree-sitter-ucode`,
based on grammar commit `4a243af329fae2f4ff01e0fc80133cbab8314600`.
It adds a dedicated dynamic `import()` expression node and permits an
exported function without a trailing semicolon. Focused corpus cases retain
static imports, a semicolon-terminated export, malformed dynamic imports,
and the newer no-semicolon form followed by another declaration. Generated
parser and node-type files changed for both plain Ucode and markup grammars.
The checkout remains local and uncommitted.

After inspecting package scripts and lockfile, `npm ci` installed 28 locked
packages into this disposable checkout using a run-owned home, temp and npm
cache. `npm run build` generated both parsers and exited zero. The first
`npm test` exposed two stale corpus expectations for the deliberately expanded
syntax; those expectations were updated. The final `npm test` exited zero:
244/244 plain Ucode, 89/89 markup and 151/151 documentation corpus cases,
plus query, highlight and tag checks. Tree-sitter CLI 0.27.1 parsed the two
exact OpenWrt files that failed in [claim 089](../../claims/089-newer-openwrt-wifi-parse-boundary.md)
and two controls with no error nodes. The [summary](summary.json) records
source paths, hashes of changed grammar/generated files, raw test-log and
parse-summary hashes, commands' exit statuses and limits. Raw logs, generated
parser output and full parse summary remain under ignored `work/`.

This is grammar-level evidence only. The generated CodeQL AST bindings and
producer extractor have not yet been rebuilt or run with it. The dedicated
dynamic import node needs an explicit model decision; parsing the source
alone does not establish query coverage or a safe release.
