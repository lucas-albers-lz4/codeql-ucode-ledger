# Claim 070: libubox blobmsg JSON serialization bounds

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin libubox `ff13b89e82e64cdd7853419504e51ec0c7e487e0` (no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2020-7248 (tagged binary JSON serialization stack overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned libubox blobmsg_json source, what buffer management governs serialization of nested/tagged data, and is the historical stack-overflow shape present or fixed?

## Method

Source oracle / P1-gated CodeQL C on libubox (resolve pin at execution): transcribe serialization buffer growth and recursion depth handling.

## Required evidence

- Buffer-management transcription with source lines
- Historical-shape presence statement

## Controls

- Positive: fixed stack buffer with recursion (if present)
- Near miss: realloc-grown buffer
- Negative: non-recursive scalar path

## Out of scope

- No overflow execution
- No JSON parser completeness

## Notes

None.

## Result

Demonstrated (source oracle): FIXED-IN-PIN / fail-no-eligible-instance WITH census; controls pass; gate run_pipeline.sh exit 0 (all rules pass). No runtime/exploit/vulnerability verdict; no gate lifted.

FIXED-IN-PIN / fail-no-eligible-instance, WITH full census (25 sites).
Controls 3/3. Oracle R0-R5 pass. 18 chains, 108 byte-verified citations.

Buffer management (two layers):
1. Heap strbuf output: malloc floor 1024 (blobmsg_json.c:320-322),
   blobmsg_puts capacity branch + SIZE_MAX overflow reject + realloc NULL
   check before every memcpy (139-155), !s.pos post-format guard (331-334),
   final realloc(pos+1) + NUL (336-340). Input-side blobmsg_add_* writes grow
   heap blob_buf via blob_buf_grow/realloc with INT_MAX-256 rejects
   (blobmsg.c:310-318; blob.c:25-63, 125-143).
2. Fixed stack staging per recursion frame: char buf[317]
   (blobmsg_json.c:236), ALL scalar formats snprintf(buf, sizeof(buf), ...)
   (254-275, DOUBLE "%.17g" worst case 25 bytes incl NUL <= 317); escape
   buf[8] with fixed index 1 and snprintf(sizeof(buf)-4) (179-186);
   indent_chars clamped memcpy (162-170).

Recursion: mutual cycles both directions (format_element <->
format_json_list; add_object <-> add_json_element <-> add_array); NO explicit
depth cap in source; implicit bound floor(input_len/4) from packed 4-byte
blob_attr headers (blob.h:47-48, 246-248). Source observation only.

Historical shape: pre-fix parent blob 132ecb56 (=1ffa415^, sha256
f890d9a2ef625f8843da870bfb0593c8630c9eb638ebfc84e8f624dfe8df1853) has
char buf[32] + sprintf(buf, "%lf") — UNGUARDED_STACK_FORMAT (declared worst
case 318 > 32). Fix 1ffa415 + hardening afc0fa8/6f01162/3bbf83c/ad775bd all
verified ancestors of the pin; pin commit itself adds the blob_is_extended
name-read guard (243). At pin: zero unguarded scalar format sinks -> the
CVE-2020-7248 stack-overflow shape is NOT present.
