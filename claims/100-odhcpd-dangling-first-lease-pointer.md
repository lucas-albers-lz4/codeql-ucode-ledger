# Claim 100: odhcpd avoids a dangling first-lease pointer across IA options

- Status: Proposed
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-53918 / GHSA-44ff-jcwh-wgc2 — DHCPv6 IA dangling first pointer use-after-free.
- Fix commit: `5b283832c0a77aed20f1cc384ffc40bc768b06e9`.

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

At the pinned source, can the per-message `first` lease pointer remain dangling after a later same-IAID IA frees that lease, before a subsequent IA copies `first->key`?

## Source anchor

- `src/dhcpv6-ia.c`: `first` assignment/key reuse and lease free paths in `dhcpv6_ia_handle_IAs` (L1203–1290, L1375).
- `src/dhcpv6-ia.c`: lease free helper (L75–76).

## Expected observable

A source oracle can enumerate `first` writes, lease frees, and key copies, and show the fixed invalidation/revalidation order.

## Oracle

Pinned-blob census + deterministic pointer-lifetime emulation. No CodeQL extraction assumed.

## Controls

- Positive: synthetic free of `first` without clearing/revalidating before key copy.
- Near miss: pointer cleared but key copied from stale local.
- Negative: fixed pin census; fail-no-eligible-instance if no dangling path remains.

## Out of scope

No runtime UAF verdict, exploitability, or analyzer `path_found`. No gate lifted.
