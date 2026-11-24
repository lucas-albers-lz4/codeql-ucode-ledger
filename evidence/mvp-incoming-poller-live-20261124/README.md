# Manual incoming discovery snapshot, 2026-11-24

An isolated, clean `codeql-openwrt` checkout at poller commit
`05312d6c6fa31c821e5f13abbe61f3188febf4c3` ran the read-only
`incoming-poll-v3` prototype against public
`openwrt/openwrt` and `openwrt/luci` GitHub REST API endpoints, using the
existing `gh` authentication token without printing or storing it. Python
3.15.2, a fresh ignored output directory under `work/`, explicit `--genesis`
and capacity 2 were used. The command exited 0. It did not run CodeQL,
dispatch CI or authenticate a scan completion.

The exact invocation from the disposable checkout was:

```sh
python3 -c 'import os,runpy,subprocess,sys; os.environ["GITHUB_TOKEN"]=subprocess.check_output(["gh","auth","token"],text=True).strip(); sys.argv=["tools/incoming_poll.py","--genesis","--capacity","2","--output-dir","/Users/lalbers/gitroot/ucode/codeql-ucode-ledger/work/incoming-live-20261124-2335"]; runpy.run_path("tools/incoming_poll.py",run_name="__main__")'
```

The token value was passed in process memory and is absent from the output
and this evidence. The path above identifies the local raw artifact only;
another machine cannot retrieve it from the repository.

The [portable summary](summary.json) records the checkpoint SHA-256 and
counts. The raw 45.7 MB `decisions.json` remains under ignored
`work/incoming-live-20261124-2335/` and is not portable. It retains 81 exact
successful response bodies with per-body digests. The v3 checkpoint parser
rechecked those body digests and validated all 1,851 pending decisions; the
checkpoint digest matched the independently calculated file digest. No HTTP
retry was needed in this run. GitHub pagination is not an atomic snapshot;
the counts describe returned rows during this run, not every upstream
transition or a stable census.

The prototype selected the lexically first two pending identities: the LuCI
default tip and LuCI PR #5041. This exposes a fairness gap: with no
authenticated completion transition, repeated polls can keep selecting
these records while later backlog waits. The PR event records full head/base
commits with unresolved trees by design. Any scan must revalidate PR state,
bind commit trees and run the released CodeQL path in the same job. The
default-tip event has no compatible downstream event resolver yet. This
snapshot therefore does not establish Gate 8 or justify scheduling.
