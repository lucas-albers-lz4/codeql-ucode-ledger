# 103 — uhttpd non-POST /ubus url_path ownership

- Status: Demonstrated
- Question: At the pinned uhttpd corpus, does every non-POST `/ubus` dispatch exit release `du->url_path`, closing GHSA-83vv-qrc6-h3hx?
- Corpus pin: `uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; pinned-C source oracle, no assumed CodeQL extraction.
- Source anchor: `ubus.c:1172-1182,1184-1206`; fix commit `5343b7f50c7906a1540bc4bbdb80656325b1b91f`.
- Expected observable: census of `/ubus` dispatch/free sites reports non-POST paths free `url_path` or install a free hook before early return; no eligible leaked allocation remains in the pin.
- Oracle: pinned-source allocation/free census plus deterministic dispatch emulator; advisory anchors motivation/source-shape only; no runtime leak measurement or exploit verdict.
- Controls: positive vulnerable fixture (strdup then early return without free), near-miss POST path with free hook, negative fixed pin; fail-no-eligible-instance with full dispatch census if fixed.
- Result: Demonstrated (fixed-at-pin source shape). Lane L decision packet re-ran `run_pipeline.sh` (exit 0). Oracle O2: 9 dispatch/free sites, 0 vulnerable; allocation failure returns before ownership `ubus.c:1172-1175`, free hook installed `:1182`, GET/OPTIONS/default free `:1205-1206`, POST defers to hook `:1189-1194`. Controls P2/NM2/N2 all true. Fix `5343b7f50c7906a1540bc4bbdb80656325b1b91f` verified in packet. Source-shape only; no runtime leak measurement, analyzer `path_found`, or gate lift.