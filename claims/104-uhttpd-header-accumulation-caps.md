# 104 — uhttpd header count and byte accumulation caps

- Status: Demonstrated
- Question: At the pinned uhttpd corpus, are header count and cumulative bytes capped before `blobmsg_add_string` accumulation on both ordinary-header and chunked-trailer paths, closing GHSA-vhx4-3p5q-m59q?
- Corpus pin: `uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; pinned-C source oracle, no assumed CodeQL extraction.
- Source anchor: `client.c:550-556,658,717-728`; `uhttpd.h:49-50` caps; fix commit `214783449202e3d526e668b2c05a8d399c028400`.
- Expected observable: census of header accumulation sites reports count/byte checks before insertion on ordinary and trailer paths; no eligible unbounded accumulation remains in the pin.
- Oracle: pinned-source cap/insertion census plus deterministic boundary emulator; advisory anchors motivation/source-shape only; no runtime DoS proof or exploit verdict.
- Controls: positive vulnerable fixture (unbounded blobmsg_add_string), near-miss exact cap boundary, negative fixed pin; fail-no-eligible-instance with full header census if fixed.
- Result: Demonstrated (fixed-at-pin source shape). Lane L decision packet re-ran `run_pipeline.sh` (exit 0). Oracle O3: 15 header sites, 0 vulnerable; ordinary cap `client.c:550-556` before insertion `:658`; trailer cap `:717-728` with connection-close on overflow. Caps `UH_LIMIT_HEADER_COUNT=100`, `UH_LIMIT_HEADER_BYTES=16384`. Controls P3/NM3/N3 all true. Fix `214783449202e3d526e668b2c05a8d399c028400` verified in packet. Source-shape only; no runtime DoS proof, analyzer `path_found`, or gate lift.