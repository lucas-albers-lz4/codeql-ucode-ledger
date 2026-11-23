"""Check the CLI against the separately prepared archive/claim 029 oracle."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import zipfile


HEAD = "fe5952073eeef913fef4b3324d9541ff66426492"
LUCI = "b2e0be4b46ec0fd43394c081fa7c50657af14011"
ARCHIVED_PATH = (
    "/root/workspace/workflow-design/evidence/issue89-typed-ae946190-7f532ac-a3/"
    "sealed/ql/test/extractor-smoke/usr/share/rpcd/ucode/luci"
)
INSTALLED = "usr/share/rpcd/ucode/luci"
RAW_PINS = {
    "extracted": "7bc14c07e3c7bea4be6c7a738c4288f2f08a2c39a083ed3f28acc338ffdc04fa",
    "routing": "281a835263b5ad6838c278fdd768d8f43e6f246ba5abeafa4555fd0a3f27d220",
}
REFERENCE = {"authority": "openwrt-consumer:luci-ssl-25.12", "id": "luci-mod-system-mounts"}
LIMITS = [
    "allow describes the pinned source model, not a built or installed package",
    "selected policy is a bounded consumer expectation, not authenticated provenance",
    "model assumes the ubus default script ran with no prior prefix and the plugin is present",
    "modeled object lookup assumes luci exists; live registration is not established",
    "archived evidence does not establish live execution",
    "ucode string-form system uses a shell; the fixed command includes redirection",
]


def check(condition, message):
    if not condition:
        raise SystemExit(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def inventory(root):
    result = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] == ".git":
            continue
        mode = path.lstat().st_mode
        if path.is_symlink():
            result[str(relative)] = [mode, os.readlink(path)]
        elif path.is_file():
            result[str(relative)] = [mode, sha(path.read_bytes())]
        else:
            result[str(relative)] = [mode]
    return result


def receipts(inputs, expected_path):
    extracted = list(csv.reader(io.StringIO(inputs["extracted"].decode())))
    check(extracted == [["f", "col1"], [expected_path, ""]], "wrong extraction identity")
    routing = json.loads(inputs["routing"])
    expected_counts = dict.fromkeys(
        ("markup_count", "markup_inconclusive_count", "uncertain_count", "excluded_count",
         "duplicate_input_count"), 0
    )
    expected_counts.update(input_count=1, plain_count=1)
    decision = {"path": expected_path, "installed_path": INSTALLED, "classification": "plain",
                "reason": "rpcd_raw_mode_full_path", "status": "plain_route_selected"}
    check(routing == dict(expected_counts, decisions=[decision]), "wrong routing identity")


def main():
    check(len(sys.argv) == 4, "usage: run.py CONSUMER_CHECKOUT CLAIM029_RAW_PRODUCER_RUN NEW_RUN")
    repo, claim, output = (Path(a).resolve() for a in sys.argv[1:])
    new_is_separate = all(not output.is_relative_to(p) and not p.is_relative_to(output)
                          for p in (repo, claim))
    check(new_is_separate, "separate the new run from sources")
    work_root = Path(__file__).resolve().parents[1]
    check(work_root.name == "work" and repo.is_relative_to(work_root) and (repo / ".git").is_dir(),
          "consumer must be a disposable Git clone under work/")
    output.mkdir()
    worktree_status = ["git", "-C", str(repo), "status", "--porcelain=v1", "--untracked-files=all"]
    check(subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"]).decode().strip()
          == HEAD and subprocess.check_output(worktree_status) == b"", "consumer checkout pin or state")
    pins = json.loads(Path(__file__).with_name("pins.json").read_bytes())
    pin = pins["_REAL_INPUTS"]
    artifacts = repo / "evidence/issue89-typed-ae946190-7f532ac/attempt/artifacts"
    archive_files = {"typed": "typed.json", "source-archive": "source-archive.zip", "errors": "errors.csv",
                     "extracted": "extracted.csv", "effects": "effects.csv", "routing": "routing.json"}
    inputs = {k: (artifacts / f).read_bytes() for k, f in archive_files.items()}
    with zipfile.ZipFile(io.BytesIO(inputs["source-archive"])) as archive:
        check(archive.namelist() == [ARCHIVED_PATH[1:]], "wrong source ZIP member")
        inputs["source"] = archive.read(ARCHIVED_PATH[1:])
    inputs["login"] = (repo / "policy/fixtures/rpcd.config").read_bytes()
    inputs["acl"] = (repo / "policy/fixtures/luci-mod-system.json").read_bytes()
    source_pins = {"recipe-system": "luci-mod-system.Makefile", "recipe-base": "luci-base.Makefile",
                   "recipe-ssl": "luci-ssl.Makefile", "recipe-light": "luci-light.Makefile",
                   "recipe-admin": "luci-mod-admin-full.Makefile", "uhttpd-recipe": "uhttpd.Makefile",
                   "uhttpd-default": "ubus.default", "uhttpd-config": "uhttpd.config",
                   "uhttpd-init": "uhttpd.init", "feed-config": "feeds.conf.default"}
    for key, name in source_pins.items():
        inputs[key] = (repo / "policy/fixtures/v2-source-pins" / name).read_bytes()
    check({k: "sha256:" + sha(v) for k, v in inputs.items()} == pin, "archival input digest mismatch")
    receipts(inputs, ARCHIVED_PATH)
    recorded = {"typed": (claim / "typed.json").read_bytes()}
    for key, file in {"source": f"src/{INSTALLED}", "effects": "effects.csv", "errors": "errors.csv",
                      "extracted": "extracted.csv", "routing": "routing.json"}.items():
        recorded[key] = (claim / "main" / file).read_bytes()
    check(all(recorded[k] == inputs[k] for k in ("typed", "source", "effects", "errors")),
          "typed/source/effects/errors should be archive-equivalent")
    check(all(sha(recorded[k]) == v and recorded[k] != inputs[k] for k, v in RAW_PINS.items()),
          "raw, nonidentical claim 029 receipts required")
    recorded_decisions = json.loads(recorded["routing"])["decisions"]
    check(len(recorded_decisions) == 1, "wrong recorded routing multiplicity")
    recorded_path = recorded_decisions[0]["path"]
    check(recorded_path.startswith("/") and recorded_path.endswith(f"/main/src/{INSTALLED}")
          and recorded_path != ARCHIVED_PATH, "wrong recorded source path")
    receipts(recorded, recorded_path)
    for key in RAW_PINS:
        check(inputs[key].count(ARCHIVED_PATH.encode()) == 1
              and inputs[key].replace(ARCHIVED_PATH.encode(), recorded_path.encode()) == recorded[key],
              f"{key}: expected only the concrete source path to change")
    errors = list(csv.reader(io.StringIO(inputs["errors"].decode())))
    effects = list(csv.reader(io.StringIO(inputs["effects"].decode())))
    expected_effects = [
        ["observation_kind", "method", "sink_kind", "command", "source_path", "start_line",
         "start_column", "end_line", "end_column"],
        ["callback_body_call", "setBlockDetect", "system", "/sbin/block detect > /etc/config/fstab",
         INSTALLED, "532", "21", "532", "68"],
    ]
    check(errors == [["error", "col1", "col2"]] and effects == expected_effects,
          "expected zero errors and one exact projected effect")

    profile = repo / "corpus/profiles/luci-ssl-25.12"
    common = {"corpus": (repo / "corpus/lock.json").read_bytes(),
              "profile": (profile / "profile.json").read_bytes(),
              "policy": (profile / "expected-capabilities.json").read_bytes()}
    context = {k: pins["_REAL_" + k.upper()] for k in common}
    check(context == {k: "sha256:" + sha(v) for k, v in common.items()}, "selected bytes mismatch")
    context["inputs"] = pin
    scope = {"caller": REFERENCE["id"], "profile": context["profile"], "ingress": "ubus_http",
             "entrypoint": "ubus_http:luci.setBlockDetect",
             "packages": {"caller": f"luci/luci-mod-system/{LUCI}@{pin['acl']}",
                          "provider": f"luci/luci-base/{LUCI}@{pin['source']}"}}
    pairs = [{"target": "ubus:luci.setBlockDetect", "operation": "invoke"}]
    selection = {"context": context, "scope": scope, "pairs": pairs}
    envelope = {"kind": "readonly-assessment", "version": 2, "context": context,
                "reference": REFERENCE, "verdict": "intended_access"}
    staged = output / "staged"
    staged.mkdir()
    for key, data in common.items():
        (staged / key).write_bytes(data)
    dump(staged / "selection", selection)
    dump(staged / "envelope", envelope)
    for label, values in (("archive", inputs), ("recorded", recorded)):
        for key, data in values.items():
            (staged / f"{label}-{key}").write_bytes(data)

    linux = sys.platform == "linux"
    check(linux or sys.platform == "darwin", "oracle covers Linux and Darwin only")
    gate = "allow" if linux else "unknown"
    policy = ({"status": "assessed", "reference": REFERENCE, "verdict": "intended_access"}
              if linux else {"status": "unassessed"})
    typed = json.loads(inputs["typed"])
    check(len(typed) == 1, "wrong typed record multiplicity")
    limit = [] if linux else ["Linux libc evaluator unavailable on this platform"]
    expected = {"gate": gate, "modeled_gate": gate, "policy": policy, "limits": LIMITS + limit,
                "observation": "archived-neutral-observation", "typed_unknowns": typed[0]["unknowns"],
                "typed_assumptions": typed[0]["assumptions"]}
    dump(output / "expected-success.json", expected)
    sandbox = []
    if sys.platform == "darwin":
        sandbox = ["/usr/bin/sandbox-exec", "-p", "(version 1) (allow default) (deny file-write*)"]
        check(Path(sandbox[0]).is_file(), "Darwin write-denying sandbox unavailable")
    dump(output / "preflight.json", {"head": HEAD, "git": subprocess.check_output(
        ["git", "--version"], text=True).strip(), "platform": platform.platform(),
        "libc": platform.libc_ver(), "python": sys.version, "python_executable": sys.executable,
        "home": "inherited", "adapter_sandbox": sandbox, "free_bytes": os.statvfs(output).f_bavail * os.statvfs(output).f_frsize})

    cases = {"archival": (), "typed-substitution": ("typed",), "extracted-substitution": ("extracted",),
             "routing-substitution": ("routing",), "receipts-substitution": ("typed", "extracted", "routing")}
    original = {"worktree": inventory(repo), "staged": inventory(staged)}
    dump(output / "inventory-initial.json", original)
    for case, swaps in cases.items():
        result = output / case
        result.mkdir()
        roots = {name: result / name for name in ("TMPDIR", "XDG_CACHE_HOME")}
        for path in roots.values():
            path.mkdir()
        env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
        env.update({name: str(path) for name, path in roots.items()})
        env.update(PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1")
        args = [*sandbox, sys.executable, "-B", "-s", "-m", "policy.v2_adapter", "--family", "setblock"]
        for name in ("selection", "envelope", "policy", "corpus", "profile"):
            args += ["--" + name, str(staged / name)]
        for key in sorted(inputs):
            label = "recorded" if key in swaps else "archive"
            args += ["--evidence", f"{key}={staged / f'{label}-{key}'}"]
        before = {"worktree": inventory(repo), "staged": inventory(staged),
                  **{name: inventory(path) for name, path in roots.items()}}
        start = time.monotonic()
        proc = subprocess.run(args, cwd=repo, env=env, capture_output=True, check=False, timeout=60)
        elapsed = time.monotonic() - start
        after = {"worktree": inventory(repo), "staged": inventory(staged),
                 **{name: inventory(path) for name, path in roots.items()}}
        (result / "stdout").write_bytes(proc.stdout)
        (result / "stderr").write_bytes(proc.stderr)
        dump(result / "receipt.json", {"argv": args, "cwd": str(repo), "elapsed_seconds": elapsed,
                                       "exit": proc.returncode, "inventories_equal": before == after,
                                       "environment_paths": {k: str(v) for k, v in roots.items()}})
        dump(result / "inventory-before.json", before)
        dump(result / "inventory-after.json", after)
        check(before == after and original["worktree"] == after["worktree"]
              and original["staged"] == after["staged"], f"{case}: artifacts changed")
        if case in ("archival", "typed-substitution"):
            stdout = (json.dumps(expected, sort_keys=True) + "\n").encode()
            check((proc.returncode, proc.stdout, proc.stderr) == (0, stdout, b""), f"{case}: result mismatch")
        else:
            check((proc.returncode, proc.stdout, proc.stderr) ==
                  (2, b"", b"evidence byte identity mismatch\n"), f"{case}: wrong rejection")
    check(subprocess.check_output(worktree_status) == b"", "consumer checkout changed")
    dump(output / "result.json", {"cases": list(cases), "status": "pass", "platform": sys.platform})


if __name__ == "__main__":
    main()
