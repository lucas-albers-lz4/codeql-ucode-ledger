# 095 — jsonpath token string lifetime in jp_get_token

- Status: Proposed
- Question: At the pinned jsonpath upstream commit used by OpenWrt jsonfilter, does `jp_get_token()` release the temporary token string after `jp_alloc_op()` copies it, closing the string/label/regexp token leak in GHSA-rcc6-v4r6-gj4m / CVE-2026-30873?
- Corpus pin: `jsonpath b9034210bd331749673416c6bf389cccd4e23610`, selected by `openwrt 4e9642517b48bae612ff10fb72fb9199e559500e:package/utils/jsonfilter/Makefile:9`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; source oracle on pinned upstream C, no assumed CodeQL extraction.
- Source anchor: `lexer.c:506-526` (`jp_get_token`, `jp_alloc_op`, temporary `op.str` free); `ast.c:27-58` (`jp_alloc_op` copies string into pooled allocation); fix commit `e086664e6a570630e8feba889482f174a9a8715e`.
- Expected observable: every temporary string allocated by token matching is freed after ownership transfer/copy, while pooled opcode strings remain owned by the parser pool; no eligible leaked temporary token string remains in the pin.
- Oracle: pinned-source allocation/ownership census plus deterministic token-lifetime emulator for string, label, and regexp paths; advisory anchors motivation/source-shape only; no runtime leak measurement or exploit verdict.
- Controls: positive vulnerable fixture (temporary string copied but not freed), near-miss non-string token with null string, negative fixed pin; fail-no-eligible-instance with full token-path census if fixed.
- Result: pending lane evidence.
