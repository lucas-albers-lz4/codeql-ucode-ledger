# Lightweight ledger checks

Run from the repository root:

```sh
python3 -B scripts/verify-ledger.py
python3 -B scripts/compare-csv-oracle.py evidence/020-markup-call/expectations.json evidence/020-markup-call/calls.csv tree,path,kind,name,sl,sc,el,ec
python3 -B scripts/verify-mvp-corpus-source.py \
  --manifest planning/mvp-bounded-corpus-v0.4.json \
  --luci work/stage6-luci --openwrt work/stage6-openwrt \
  --packages work/stage6-packages
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

The third command checks v0.1 through v0.6 of the bounded MVP source
manifest against clean, exact-pinned isolated checkouts, including each
selected file's SHA-256 and Git blob and the recorded excluded identities.
For v0.5 and v0.6 it also checks the 12 and five added OpenWrt full-tree
source identities respectively, plus manifest counts. It does not check installed package bytes, routing,
extraction, query results or execution freshness. Its `work/` paths are local
examples; use the actual isolated checkout paths on another machine.
