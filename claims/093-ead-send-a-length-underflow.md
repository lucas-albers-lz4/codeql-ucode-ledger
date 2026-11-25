# 093 — EAD handle_send_a pre-subtraction length guard

- Status: Proposed
- Question: At the pinned OpenWrt corpus, does `handle_send_a()` reject `msg_len < sizeof(struct ead_msg_number)` before subtraction and bound the resulting copy length, closing the integer-underflow shape in GHSA-9558-77jp-g3fw / CVE-2026-55608?
- Corpus pin: `openwrt 4e9642517b48bae612ff10fb72fb9199e559500e`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; source oracle on pinned C, no assumed CodeQL extraction.
- Source anchor: `package/network/services/ead/src/ead.c:427-441,673-674`; fix commit `fda611d2751ea7e10bd16de8e55d498beca35f09`.
- Expected observable: the guard tests `msg_len` before subtraction, rejects under-length messages, bounds `msg_len - sizeof(...)` by `MAXPARAMLEN + 1`, and only then uses the nonnegative bounded length in `memcpy`; no eligible underflow path remains in the pin.
- Oracle: pinned-source guard/copy census plus deterministic unsigned-to-signed arithmetic emulator for boundary lengths; advisory anchors motivation/source-shape only; no runtime or exploit verdict.
- Controls: positive vulnerable fixture (`0u - 1u` assigned to signed length and passed to copy), near-miss `msg_len == sizeof(...)` and `MAXPARAMLEN + 2`, negative fixed pin; fail-no-eligible-instance with full `handle_send_a` census if fixed.
- Result: pending lane evidence.
