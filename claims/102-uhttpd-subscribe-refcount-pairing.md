# 102 — uhttpd subscribe client refcount pairing

- Status: Demonstrated
- Question: At the pinned uhttpd corpus, does every `/ubus/subscribe` client-reference acquisition pair with release on success and all failure exits, closing GHSA-wvgh-cm54-q6f6?
- Corpus pin: `uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; pinned-C source oracle, no assumed CodeQL extraction.
- Source anchor: `ubus.c:445,465,467,470-473`; fix commit `06aa5c4749a570503f5b51a8b865d2632e26fbed`.
- Expected observable: census of subscribe acquire/release sites reports every `uh_client_ref` paired with `uh_client_unref` and disconnect cleanup installed; no eligible unpaired acquire remains in the pin.
- Oracle: pinned-source refcount census plus deterministic ownership emulator; advisory anchors motivation/source-shape only; no runtime DoS or exploit verdict.
- Controls: positive vulnerable fixture (acquire without release), near-miss error path with unregister+unref, negative fixed pin; fail-no-eligible-instance with full subscribe census if fixed.
- Result: Demonstrated (fixed-at-pin source shape). Lane L decision packet re-ran `run_pipeline.sh` (exit 0). Oracle O1: 10 subscribe sites, 0 vulnerable; `uh_client_ref` `ubus.c:445`, cleanup installed `:465`, release `:467`, failure paths `:470-473`. Controls P1/NM1/N1 all true. Fix `06aa5c4749a570503f5b51a8b865d2632e26fbed` verified in packet. Source-shape only; no runtime DoS proof, analyzer `path_found`, or gate lift.