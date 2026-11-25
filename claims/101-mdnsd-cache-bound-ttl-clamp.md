# Claim 101: mdnsd cache growth is bounded and hostile TTLs are clamped

- Status: Proposed
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: mdnsd `defe7ccfd20281b9ef4dfa45437813386a64f8ba`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-55492 / GHSA-jg8f-fhfw-jg46 — pre-auth adjacent-network DoS via unbounded mDNS cache.
- Fix commits: `1b5e7bf1cec775b89f1a6068dc0b9df3593b5986` (bound cache size/clamp TTL), `bd7599d021571e785bd32a75469e7148eb1772e3` (calloc_a size argument type).

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

Does the pinned mdnsd cache enforce an entry-count limit for records and services and clamp stored TTLs so GC can reclaim hostile entries?

## Source anchor

- `cache.c`: `CACHE_TTL_MAX`, `CACHE_ENTRIES_MAX`, `cache_entries_max` (L59–62).
- `cache.c`: service limit (L202), TTL clamp (L305–306), record limit/drop (L406–407).
- `main.c`: `-c` override validation (L111–115).

## Expected observable

A source oracle can enumerate allocation sites and show each is guarded by the count limit, and TTL is clamped before storage.

## Oracle

Pinned-blob census + deterministic cache-growth emulation. No CodeQL extraction assumed.

## Controls

- Positive: synthetic unbounded calloc_a insertion with hostile TTL.
- Near miss: count limit present but TTL unclamped.
- Negative: fixed pin census; fail-no-eligible-instance if bounded.

## Out of scope

No runtime OOM/DoS verdict, exploitability, or analyzer `path_found`. No gate lifted.
