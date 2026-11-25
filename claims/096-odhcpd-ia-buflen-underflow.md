# Claim 096: odhcpd IA buflen underflow is capped before serialization

- Status: Demonstrated
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-53922 / GHSA-7hcw-g2jh-pqv5 — pre-auth remote DoS via size_t underflow in `dhcpv6_ia_handle_IAs`.
- Fix commits: `d08dbcc527cb8f296cd132c1e5bca696e77095b8` (cap subtraction), `d168c27fb6a55a07ac4c888e09ff2f41e263d7b7` (build_ia bounds).

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

At the pinned odhcpd source, is the IA option-length subtraction capped so `buflen` cannot underflow to `~SIZE_MAX` before `build_ia` serializes into the caller buffer?

## Source anchor

- `src/dhcpv6-ia.c`: `dhcpv6_ia_handle_IAs` (L967+), IA option loop and minimum-length comment (L1033+), `build_ia` buffer writes.
- `src/dhcpv6.c`: caller `pdbuf` and `dhcpv6_ia_handle_IAs` invocation (L823).

## Expected observable

A source oracle can enumerate the subtraction/bound checks and show the fixed order: validate option length, cap remaining buffer, reject insufficient space before memcpy/serialization.

## Oracle

Pinned-blob census + deterministic arithmetic emulation of `size_t` subtraction and signed/unsigned assignment. No CodeQL extraction assumed.

## Controls

- Positive: synthetic uncapped `buflen -= olen` with `olen > buflen`.
- Near miss: capped subtraction but missing post-check before write.
- Negative: fixed pin census; fail-no-eligible-instance if no uncapped site remains.

## Out of scope

No packet replay, runtime DoS verdict, exploitability, or analyzer `path_found`. No gate lifted.

## Result

Demonstrated (fixed-in-pin source shape). Orchestrator re-ran `run_pipeline.sh` (exit 0): oracle 10/10 checks, controls 3/3, `vulnerable_sites=0` over 9 eligible sites. Census: exactly two `buflen -=` sites (`src/dhcpv6-ia.c:1287,1410`), both guarded/capped; `ia_response_len` capped to `buflen` before subtraction (`:1406-1410`); handshake subtraction dominated by pre-write guard (`:1266-1287`); seven `build_ia` memcpy sites space-checked (`:603,607,696,715,807,821,829`); caller passes `pdbuf[512]` (`src/dhcpv6.c:669,823`). Fixes `d08dbcc527cb8f296cd132c1e5bca696e77095b8` and `d168c27fb6a55a07ac4c888e09ff2f41e263d7b7` verified ancestors of pin. Source oracle only; no CodeQL extraction, runtime/exploit verdict, `path_found`, or gate lift.
