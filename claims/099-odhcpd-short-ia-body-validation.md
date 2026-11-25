# Claim 099: odhcpd validates IA_NA/IA_PD option size before reading the header

- Status: Demonstrated
- Program: [Security-extension Wave N](../planning/security-extension-waveN-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Corpus pin: odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273`
- Consumer: none
- Environment: local source oracle; no CI

## Historical anchor

- CVE-2026-53920 / GHSA-p769-5v73-pc4f — DHCPv6 short IA_NA/IA_PD body stack disclosure.
- Fix commit: `719fc3abc0d7e7059871f9f572fb05ada86b8ff2`.

Anchor role: motivation and source-shape specification only; no runtime/exploit verdict.

## Bounded question

Does `dhcpv6_ia_handle_IAs` reject IA_NA/IA_PD options shorter than the RFC8415 header before casting to `dhcpv6_ia_hdr` and reading `iaid`/`t1`/`t2`?

## Source anchor

- `src/dhcpv6-ia.c`: IA option loop minimum-length validation (L1033–1047).
- `src/dhcpv6-ia.h`: `dhcpv6_ia_hdr` layout.

## Expected observable

A source oracle can show the length guard precedes every header field read and uses the correct minimum size.

## Oracle

Pinned-blob census + short-option emulation. No CodeQL extraction assumed.

## Controls

- Positive: synthetic cast/read with `olen < sizeof(header)`.
- Near miss: guard present after first field read.
- Negative: fixed pin census; fail-no-eligible-instance if guarded.

## Out of scope

No runtime disclosure verdict, exploitability, or analyzer `path_found`. No gate lifted.

## Result

Demonstrated (fixed-in-pin source shape). Orchestrator re-ran `run_pipeline.sh` (exit 0): oracle verdict PASS (15/15 checks), controls 3/3. The IA option loop validates minimum option length before casting to `dhcpv6_ia_hdr` and reading `iaid`/`t1`/`t2` (`src/dhcpv6-ia.c:1033-1047`); header layout is packed type/len/iaid/t1/t2 with `sizeof=16` (`src/dhcpv6.h:131`) and `DHCPV6_OPT_HDR_SIZE=4` (`src/odhcpd.h:197`). Short-option emulation shows no eligible under-length header read remains. Fix `719fc3abc0d7e7059871f9f572fb05ada86b8ff2` verified ancestor of pin. Source oracle only; no CodeQL extraction, runtime/exploit verdict, `path_found`, or gate lift.
