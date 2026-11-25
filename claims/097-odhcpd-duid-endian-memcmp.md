# Claim 097: odhcpd self-loop DUID memcmp uses host-order length

- Status: Demonstrated
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-55606 / GHSA-x8x4-7gvf-gp45 — stack buffer overread via DUID length endianness mismatch in `memcmp()`.
- Fix commit: `6907f28f9ddeef9f69f5ee10bbc9ba8adc0ef57f`.

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

Does the pinned self-loop guard compare the configured server DUID against the received client DUID using a host-order length (`ntohs(dest.serverid_length)`) rather than the raw network-order field?

## Source anchor

- `src/dhcpv6.c`: `handle_client_request` self-loop guard, `memcmp(clientid.buf, dest.serverid_buf, ntohs(dest.serverid_length))` (L769).
- `src/dhcpv6.c`: serverid length assignment via `htons` (L414/L419).

## Expected observable

A source oracle can show the memcmp length argument is decoded to host order and bounded by the destination buffer size.

## Oracle

Pinned-blob census + endianness emulation for little/big-endian length values. No CodeQL extraction assumed.

## Controls

- Positive: synthetic `memcmp(..., dest.serverid_length)` with htons-encoded length.
- Near miss: `ntohs` used but no buffer-size bound.
- Negative: fixed pin census; fail-no-eligible-instance if no raw-length memcmp remains.

## Out of scope

No runtime overread measurement, exploitability, or analyzer `path_found`. No gate lifted.

## Result

Demonstrated (fixed-in-pin source shape). Orchestrator re-ran `run_pipeline.sh` (exit 0): oracle 8/8 checks, controls 3/3, `vulnerable_sites=0` over 2 eligible memcmp sites. The self-loop guard compares with host-order length `ntohs(dest.serverid_length)` (`src/dhcpv6.c:769`), and serverid length is stored via `htons` (`:414,:419`); both census memcmp sites are bounded by the destination buffer. Fix `6907f28f9ddeef9f69f5ee10bbc9ba8adc0ef57f` verified ancestor of pin. Source oracle only; no CodeQL extraction, runtime/exploit verdict, `path_found`, or gate lift.
