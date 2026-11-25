# Claim 068: px5g certificate-signing buffer bounds

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin luci `b2e0be4b46ec0fd43394c081fa7c50657af14011` (px5g in luci-lib-px5g; no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jgc3-4q3p-g6xh (2040-bit cert signing heap overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned luci-lib-px5g source, what buffer sizes govern key/signature handling during certificate signing, and is the 2040-bit overflow shape observable?

## Method

Source oracle / P1-gated CodeQL C on px5g at pinned luci SHA: transcribe allocation sizes vs key-size inputs in the signing path.

## Required evidence

- Size-input table with source lines
- Historical-shape presence statement

## Controls

- Positive: fixed buffer smaller than max key-derived write (if present)
- Near miss: size-derived allocation
- Negative: unrelated fixed buffer

## Out of scope

- No overflow execution
- No crypto correctness claim

## Notes

None.

## Result

Demonstrated (source-shape observability): the GHSA-jgc3-4q3p-g6xh 2040-bit signing-overflow shape is observable in pinned luci-lib-px5g source (present_in_pin_unfixed). Source oracle, two-pass census; controls 3/3; gate run_pipeline.sh exit 0. No runtime/exploit/vulnerability verdict; no gate lifted.

### Answer — buffer-bounds observation
Key-size → buffer-size chain (signing path):
- nbits enters via Lua px5g genkey (entry context, outside census).
- rsa_gen_key guards nbits >= 128 (rsa.c:80); primes are (nbits+1)>>1
  (rsa.c:93/96); retries until msb(N) == nbits (rsa.c:105-106).
- ctx->len = (msb(N)+7)>>3 = ceil(nbits/8) (rsa.c:127; rsa.h:91).
- make_sign: sign_len = mpi_size(N) = ceil(nbits/8) (x509write.c:972);
  sign buffer malloc(sign_len) (x509write.c:978).
- sha1(tbs) -> hash[20] (x509write.c:971/975; sha1.c output[20]).
- rsa_pkcs1_sign writes EXACTLY olen = ctx->len bytes into sign:
  0x00,0x01 + 0xFF*nb_pad + 0x00 + DigestInfo(15) + hash(20),
  nb_pad = olen-3-35 (rsa.c:427), guard nb_pad >= 8 (rsa.c:434).
  This buffer is correctly sized (exact fit). rsa_private -> mpi_write_binary
  is guarded by buflen < mpi_size (bignum.c:497).
- The signature is then wrapped: asn1_add_obj(sign, sign_len,
  ASN1_BIT_STRING, &chain->sign) (x509write.c:986).

THE OVERFLOW IS NOT IN THE RSA SIGNATURE BUFFER. It is in the ASN.1 BIT
STRING node that wraps it:
- alloc (long branch, x509write.c:113) = size + tl + eval_octet(size),
  tl = 3 for BIT STRING -> size + 3 + eval_octet(size).
- the length field encodes size+1 (the unused-bits octet is counted in the
  length, x509write.c:127) and consumes 1 + eval_octet(size+1) bytes.
- write (x509write.c:137 memcpy) = 1(tag) + [1+eval_octet(size+1)](length)
  + 1(unused) + size = size + 3 + eval_octet(size+1).
- alloc reserves eval_octet(size) length-value bytes but the length field
  needs eval_octet(size+1). They differ exactly when size+1 crosses a
  power-of-256 boundary -> 1-byte heap overflow at size in {127, 255, 65535,...}.
- For a 2040-bit key: sign_len = ceil(2040/8) = 255 -> alloc 259, write 260
  -> one-byte heap overflow (byte index 259 into a 259-byte buffer [0..258]).
  The post-write check (p += size-1) != node->end (x509write.c:138) returns
  POLARSSL_ERR_X509_POINT_ERROR AFTER the memcpy already executed.
  This reproduces the advisory's 259/260 figures exactly from source.
- For a 2048-bit key: sign_len = 256 -> alloc 261, write 261 -> exact fit (safe).
- The INTEGER encoding (asn1_add_mpi, x509write.c:214) uses length value = size
  (not size+1), so alloc == write always -> safe. The defect is BIT-STRING-specific.

Overflow-shape sites (cls=overflow_iff_boundary):
- library/x509write.c:113 [node_realloc]
- library/x509write.c:116 [node_realloc]
- library/x509write.c:137 [memcpy]
- library/x509write.c:263 [node_realloc]
- library/x509write.c:266 [node_realloc]

### Present vs fixed (source observation only)
Determination: present_in_pin_unfixed.
- All 10 census-file blobs in the pin are IDENTICAL to the advisory PoC commit
  8b5f528eb3ad (blob identity; histories divergent but px5g tree byte-identical).
- The px5g-drop commit cbf6d42c3370 is NOT an ancestor of the pin (package present).
- x509write.c history has no encoder fix (comment-typo + build-system commits only).
- The overflow formula is transcribable from the pinned bytes (R2 PASS).
=> The 2040-bit overflow shape is PRESENT and unfixed in the pin, observable
   in-source. This is a source-shape observation, NOT a runtime/exploit/vuln verdict.

### Census / two-pass agreement
- PASS A mechanical census: 172 size sites (scripts/census.py).
- PASS B independent transcription: 172 sites (scripts/expected.py).
- R1 multiset bijection: PASS (exact cover). R0 citation anchors: PASS.
- Scope: {'governing': 31, 'keygen': 6, 'out': 78, 'signing': 57}.
- R2 boundary arithmetic: PASS (advisory 259/260 reproduced; 127/255 overflow,
  128/254/256 safe; INTEGER always exact; PKCS#1 block exact fit).

### Controls (predeclared site-based R3, 3/3)
- POS asn1_append_tag [BITSTRING_LEN_MISMATCH] PASS — x509write.c:263 alloc / :279 length(node->len+1) / :287 memcpy
- NEAR asn1_append_nodes [CONSISTENT] PASS — x509write.c:325 alloc / :338 length(size) / :349 memcpy
- NEG mpi_write_binary [GUARDED] PASS — bignum.c:497 if( buflen < n ) return POLARSSL_ERR_MPI_BUFFER_TOO_SMALL
  POS delta(255)=1, delta(127)=1; NEAR max|delta|=0 over 603 sizes; NEG guard 'buflen < n' at bignum.c:[497].

### Evidence
- size_input_table.json (172 rows + boundary arithmetic + key-size chain)
- oracle.json / oracle.md (predeclared rules + results)
- controls.json (3/3 gate)
- provenance.json (pin + sha256 + blob identity)
- evidence/nl_*.txt (sha256-verified citations), evidence/sha256_sources.txt,
  evidence/provenance_raw.txt
- scripts/{census,expected,shape_model,eval_table,controls,shape_eval,assemble}.py
- run_pipeline.sh (exit 0 only if oracle + controls pass)

### Gaps / honest absence
- No runtime/exploit demonstration (out of scope; source oracle only).
- No compiled C probe; limb-width (ciL) is host-dependent (unsigned long:
  4 on 32-bit MIPS, 8 on x86_64) but all byte-level formulas are ciL-invariant.
- bn_mul.h contributes no size sites (assembly multiply macros only).
- px5g.c Lua entry point is context only (outside the declared census scope).
- The advisory's exact heap layout/allocator behavior is NOT reproduced; only
  the source-level alloc-vs-write byte arithmetic is transcribed.
