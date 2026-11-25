# Claim 098: odhcpd IA reply serialization checks buffer space at both overflow sites

- Status: Proposed
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-53921 / GHSA-7fwx-hhrg-3496 — stack buffer overflow in DHCPv6 IA reply serialization (two independent sites).
- Fix commits: `d168c27fb6a55a07ac4c888e09ff2f41e263d7b7`, `6634b7a3c79c41a27687925c98c35c8aea2f2b5a`, `89d18771810bdf73f05db042d0baa4fd1af71eae`.

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

At the pinned source, do `build_ia` error-status serialization and the Reconfigure-Accept auth write both check remaining buffer space before writing, and does the IA_ADDR branch signal buffer-full consistently with IA_PREFIX?

## Source anchor

- `src/dhcpv6-ia.c`: `build_ia` status/IA header writes (L603–607, L696–715, L807–829).
- `src/dhcpv6-ia.c`: Reconfigure-Accept auth write in `dhcpv6_ia_handle_IAs` (L1282–1283).

## Expected observable

A source oracle can enumerate each write site, its preceding space check, and the buffer-full return path.

## Oracle

Pinned-blob census + deterministic buffer-offset emulation. No CodeQL extraction assumed.

## Controls

- Positive: synthetic write without remaining-space check.
- Near miss: IA_PREFIX returns 0 but IA_ADDR continues.
- Negative: fixed pin census; fail-no-eligible-instance if all sites guarded.

## Out of scope

No runtime overflow verdict, exploitability, or analyzer `path_found`. No gate lifted.
