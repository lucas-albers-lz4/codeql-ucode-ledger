# Claim 069: mdnsd PTR/reverse-lookup stack buffers

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin mdnsd `defe7ccfd20281b9ef4dfa45437813386a64f8ba` (shared-clone HEAD; mdnsd has left the OpenWrt feed; no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-mpgh-v658-jqv5 / CVE-2026-30872
- GHSA-7c3j-f7w2-p8f6 / CVE-2026-30871 (both critical stack overflows)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned mdnsd source, what stack buffers receive DNS PTR/reverse-lookup name construction, and what bounds checks are observed in-source?

## Method

Source oracle / P1-gated CodeQL C on mdnsd (resolve package pin at execution): transcribe name-building loops and buffer declarations.

## Required evidence

- Buffer→write-chain multiset
- Pin resolution receipt

## Controls

- Positive: unbounded name copy into fixed stack buffer (if present)
- Near miss: bounded snprintf
- Negative: heap-allocated name path

## Out of scope

- No overflow execution
- No DNS protocol completeness

## Notes

None.

## Result

Demonstrated (source oracle): FIXED-IN-PIN / fail-no-eligible-instance WITH census; controls 3/3; gate run_pipeline.sh exit 0 (32 chains, 169 citations verified, 59/59 census). No runtime/exploit/vulnerability verdict; no gate lifted.

FIXED-IN-PIN / fail-no-eligible-instance. Source-shape statement only; no
runtime/exploit/vulnerability verdict; no gate lifted.

The peer-question PTR/reverse-lookup path writes into these stack buffers, all
guarded at the pin:
- name_buf[256] (dns.c:634): strcpy@635 dominated by strlen range guard 20..28
  (dns.c:629-631, MIN/MAX_PTR_NAME_LEN, dns.h:45/47).
- name_buf6[256] (dns.c:646): strcpy@647 dominated by strlen == 72 equality guard
  (dns.c:642-643, MAX_PTR6_NAME_LEN, dns.h:49).
- temp_ip[INET6_ADDRSTRLEN=46] (dns.c:457): nibble/colon rebuild loop 461-477 with
  in-loop dot/nibble alternation reject (462-463); worst case 32 nibbles + 7 colons
  = 39 writes <= 45; zero-init; inet_pton revalidation (479).
- intf_ip[46]/[16] (dns.c:511/549): inet_ntop with matching size args (525/563).
- buffer[256] x2 (dns.c:512/550): dn_comp sizeof(buffer) + len<1 (529/531, 567/569).
- ip1[4]/ip2[4] int (dns.c:488): sscanf "%d.%d.%d.%d%c" + res==4 (491-492).
Upstream source name_buffer[8097] static, dn_expand cap 8096 (dns.c:53/405) > 255:
local guards are load-bearing.

Fix ancestry verified: a3dcb4a, b798c24, a52cdb3 (2026-02-06) and 4d3628f
(2026-09-30 TXT bound) are all ancestors of the pin; path introduced by 2b28094
(2024-02-20). Eligible unguarded peer-question instance set at pin: EMPTY.
