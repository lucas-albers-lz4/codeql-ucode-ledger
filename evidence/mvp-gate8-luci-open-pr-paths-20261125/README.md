# Current open LuCI PR Ucode path screen (2026-11-25)

## Decision and boundary

This is a bounded lead inventory for the Gate 8 known-alert drill. It does
not establish a CodeQL alert, a vulnerability, a clean negative, a full head
tree inventory, or a released scan. PRs can change after this snapshot.
The portable [candidate manifest](candidates.json) records the 41 open PRs
whose changed-file metadata contained one of the paths described below,
with full head/base commits and GitHub's changed-file blob SHA per path.
For a removed file such as #9058's, that SHA identifies the removed blob,
not a current-head blob. These identities have not been independently
fetched or compared with installed bytes.

## Collection

At 2026-11-25 02:53:32 UTC, `gh` 2.104.0 enumerated open `openwrt/luci`
PRs with `gh pr list --repo openwrt/luci --state open --limit 500 --json
number,headRefOid,baseRefOid,url`. A separate paginated REST listing returned
two pages and the same 200-open-PR denominator. Enumeration was not atomic;
PR state may have changed between page requests. The ignored collection
scripts under `work/gate8-luci-open-pr-paths-root-20261125/` requested each
PR's changed-file pages through `gh api` with `per_page=100`, four workers
and a 90-second per-request timeout. They selected paths ending `.uc`,
`.ucode`, `.ut`, or containing `/rpcd/ucode/`. All 200 file-list requests
exited 0: 41 PRs had 88 matching changed paths. The second pass fetched
patch metadata for those 41 PRs, re-read each PR's head/base, and matched
all 41 full SHA pairs to the initial list. It saw no missing patch body and
no request error. A case-insensitive textual screen for `request.args`,
`popen(`, `system(`, `shellquote`, `fs.exec` or `exec_direct(` found 22 PRs
with a hit in a matching changed-file patch. These are text leads only.

The raw API responses, per-request exits and error fields remain in ignored
`work/` on the collection machine. They are not portable evidence. Their
SHA-256 digests are: initial PR list
`0208249906ecf01440991f7d7d8c6c655740f55e2cb7bce1f1226c429f02eea1`,
file-list summary
`159d34b475b37c638e3b035c01760180fbbe65f07d2c0070237dbf1c5b994c2e`,
and patch-screen summary
`7f05b1bb6d9e159936fcddf3aa51b6aebe5b87e1cf366a47b4eb730030299dde`.
The committed candidate manifest is a reviewed small projection of the
file-list responses; its SHA-256 is
`342e919ddc6333638e4629244751abdd5fed3326178f280e72909f74e9da2e98`.

## Security triage of changed patches

A defensive source review of all 22 textual-hit patches found no eligible
**changed-patch** positive for the current narrow `DirectRpcShellWord.ql`
shape: a returned handler method with a direct raw `${formal.args.field}`
shell word in a template, passed to imported `fs.popen` in that handler or
through its supported one-local form. Representative distinctions:

- #9291 has an imported `popen` for a fixed-prefix `sha256sum` command on a
  helper-local temporary path; its `install` handler forwards `request.args`.
- #9193 uses `req.args.action` but the command reaches builtin `system` via
  `sprintf`, outside this rule's imported-`fs.popen` sink.
- #8713 builds commands in helpers and shell-quotes supplied values before
  `popen`; #9178 quotes `dev` in a nested query helper.
- #9253 quotes each helper `argv` element before `popen`; #8878's OpenVPN
  patch changes quoting/validation and its source is outside the current
  v0.6 selected policy.

This review does not cover unmodified code elsewhere in those head trees,
all other upstream PRs, imported lexical identity in a CodeQL database, or
runtime behavior. It does not prove that the PRs are safe. The next candidate
must be chosen from exact head/base source blobs, checked against the frozen
selection policy, with a predeclared alert location and independent clean
control before any released producer-to-consumer drill.
