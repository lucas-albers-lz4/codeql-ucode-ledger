# Claim 072: procd PATH/environment filter in service exec

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin procd `58eb263d5abe03f8c1280bdfa65a3b052614215d` (no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jw28-hxcm-j934 / CVE-2026-30874 (PATH filter bypass)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned procd service exec source, how is PATH/environment filtered before exec, and is the advisory bypass shape observable in-source?

## Method

Source oracle / P1-gated CodeQL C on procd (resolve pin at execution): transcribe env construction and exec paths.

## Required evidence

- Env-filter transcription with source lines
- Pin receipt

## Controls

- Positive: filter bypassable by observed construction (if present)
- Near miss: fully sanitized env
- Negative: non-service exec path

## Out of scope

- No command execution demonstration
- Low-severity advisory — claim value is the interface observation

## Notes

None.

## Result

Demonstrated (source oracle): fail-no-eligible-instance — FIXED-IN-SOURCE at pin WITH census; controls 3/3; gate run_pipeline.sh exit 0. No runtime/exploit/vulnerability verdict; no gate lifted.

### Finding (pinned bytes)
The advisory site is hotplug-dispatch.c:hotplug_call (ubus
hotplug.<subsys>.call), not service/instance.c. Caller env strings are
filtered before merging with procd's inherited environ:
- hotplug-dispatch.c:232 strncmp(enve,"LD_",3) — LD_ prefix blocked.
- hotplug-dispatch.c:235 strncmp(enve,"PATH=",5) — PATH prefix blocked;
  the literal includes '=', so every well-formed PATH=VALUE is skipped.
- hotplug-dispatch.c:245 validate_envvarname — name charset validation.
- Merge is no-override (base environ inserted first, :217; caller insert
  :262; duplicate frees :264-265): caller may add new vars, not override.
- execve("/bin/sh", ..., pc->envp) at :126 uses the explicit filtered envp
  built at :279-289, not environ. Teardown balanced (H03).

Historical shape (e08cdc85^ = afa4391d, POS control): the PATH filter was
`if (!strcmp(enve, "PATH"))` — full-string compare against a literal without
'=', which no well-formed PATH=VALUE string can equal; the filter skipped
nothing and caller PATH reached the merge (conditional on the inherited
environ lacking PATH, since the no-override merge would otherwise skip it).
The fix changes exactly that one statement (diff numstat 1/1, verified).
At the pin the shape is FIXED; no eligible instance exists in pinned bytes.

### Context paths (not the advisory family)
- service/instance.c instance_run: setenv :486/:489/:492 (root-supplied
  service config, no filter by design) -> execvp :559. NEG control.
- plug/hotplug.c handle_exec: kernel-event setenv :189 -> execvp :211.
- jail/jail.c: build_envp :967 imports -e/OCI env unfiltered; execvpe :1329
  honors imported PATH intentionally (:1328 comment); free_opts(false) keeps
  env live in child (:260-261). Local root CLI trust boundary.
- jail OCI hooks: execve with hook->envp :487, stat/exec-bit guards.

### Census and agreement
93 sites (hotplug-dispatch.c 37, plug/hotplug.c 7, service/instance.c 19,
jail/jail.c 30); 71 covered by 7 pinned chains + 22 local_only with reasons;
1 historical control chain (H08). Two independent passes (line-regex census
vs state-machine/function-token transcription) agree exactly on site set,
classes, and multiset.

### Controls
POS real pre-fix bytes -> FILTER_INEFFECTIVE; NEAR real pinned hotplug_call
-> FILTER_EFFECTIVE (one-statement difference); NEG real pinned instance_run
-> NO_FILTER (different family). 3/3. Supplemental synthetic statement swap
(disposable, never compiled/executed) -> FILTER_INEFFECTIVE, outside gate.

### Evidence
072/oracle.md, oracle.json, chains.json, controls.json, provenance.json,
run_pipeline.sh, summary.md, work/revisions.md, pinned/ (14 blobs),
work/historical/prefix_hotplug-dispatch.c, scripts/ (6 stages).
Reproduce: cd 072 && ./run_pipeline.sh (exit 0).
