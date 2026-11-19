# Claim 017: rpcd login ACL negation whitespace parity

**Status: Demonstrated for the pinned C reference, consumer oracle, and stated controls.**

## Claim and boundary

At the pinned consumer revision, `policy.oracle.login_test_permission` agrees
with rpcd's `rpc_login_test_permission` on the tested ASCII C-whitespace,
UTF-8 NBSP/EM SPACE, ordinary read/write, default-session, NUL and synthetic
session-gate cases. In particular, C-locale whitespace after `!` is stripped,
while NBSP and EM SPACE bytes are not. This is a bounded policy-oracle
comparison; it does not establish live rpcd/uhttpd behavior or an authorization
bypass.

## Revisions and expected behavior

- Consumer: `1d025213c102dfa68a0f1a5cb46de65f5b0c4e33`.
- rpcd source: `d99f703e4035d03fbcfbada3cb697db346c2b984`, selected by the
  consumer's corpus lock.
- Issue: [OpenWrt #116](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/116).
- `session.c` SHA-256:
  `225e9a1fa8badc8fa431db11403f833ed745a99502f46ca84e004b36499ada6f`.

Before running the consumer tests, independently read
`rpcd/session.c:934–990` and derived the expected matrix from its
`isspace((unsigned char)...)` loop under the test's C locale. The six ASCII
whitespace characters are stripped; UTF-8 NBSP/EM SPACE are not. Thus with
patterns `['*', '!<whitespace>example']`, an ASCII-prefixed negation denies
`example`, while a Unicode-prefixed negation leaves `example` allowed and
matches the correspondingly Unicode-prefixed group. The source-first
[expectations](../evidence/018-20261118-login-whitespace/source-first.json)
record this matrix and function identity.

The function body embedded in
`policy/tests/rpcd_login_permission_ref.c` was compared byte-for-byte with
that exact upstream function: both SHA-256 values are
`260a54df33b57e8a0e96cd046e45d8cf02db729f9981a6b6d6d9c665cf781e1b`.
The reference harness uses minimal UCI stand-ins and a thread-local C locale;
it is not a build or execution of native rpcd.

## Fresh consumer test run: 2026-11-18 UTC

The isolated consumer checkout was clean at the pinned revision. Ran:

```sh
env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest \
  policy.tests.test_login_negation_whitespace -v
```

Exit 0: all three focused tests passed. They compare the actual Python oracle
to the compiled C reference over the whitespace controls, then check existing
read/write/default/NUL cases and that synthetic `session_acls` plus
`evaluate_call` follow the same allow/deny outcomes. Python 3.15.2, GCC
13.3.0; GNU time reported 0.11 s wall and 24,788 KiB peak RSS. Exact hashes,
commands and output are in the
[run receipt](../evidence/018-20261118-login-whitespace/commands-and-timings.json).

## Limits

This check does not exercise libuci, a live rpcd session, uhttpd transport,
firmware, or a real ACL configuration. The integrated gate cases use synthetic
sessions and ACL entries. It demonstrates parity only for the named cases and
reference function; it does not establish policy correctness beyond that
comparison, runtime reachability, authorization bypass, or a vulnerability.
The owning change and broader test suite remain with OpenWrt #116; this claim
adds bounded evidence and does not create a separate finding.
