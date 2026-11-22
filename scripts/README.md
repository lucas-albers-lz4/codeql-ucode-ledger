# Lightweight ledger checks

Run from the repository root:

```sh
python3 -B scripts/verify-ledger.py
python3 -B scripts/compare-csv-oracle.py evidence/020-markup-call/expectations.json evidence/020-markup-call/calls.csv tree,path,kind,name,sl,sc,el,ec
```

The first checks simple inline Markdown links to local files in tracked and
non-ignored untracked files, and JSON/CSV syntax. It skips fenced examples,
external URLs, images, reference-style links and link fragments. It is a simple
pattern check: link titles and inline-code examples may need manual review.
It does not verify anchors, claims, provenance, secrets or the content of
linked documents. Run `git diff --check` and review changes and
portable artifacts separately.

The second accepts a JSON object containing `expected_rows`, a decoded CSV,
and an explicit ordered comma-separated list of columns. It reports missing
and unexpected tuple multiplicities and returns nonzero on differences or
invalid input. The expected rows must already have been independently derived
from the source and contract before examining actual output. Matching projected
rows does not prove unique AST entities, successful extraction, routing,
absence of diagnostics, or execution freshness; check these separately. The
example rechecks a completed receipt; it does not rerun CodeQL.
