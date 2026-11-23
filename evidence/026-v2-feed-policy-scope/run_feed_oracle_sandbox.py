#!/usr/bin/env python3
"""Run the four predeclared synthetic cases against a fresh consumer copy."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


PIN = "48c6a65b7578234644c6b06780fc82ccf6d61a8b"
REFERENCE = {"authority": "ledger-fixture", "id": "status"}
VERDICT = "intended_access"
ASSESSED = {"gate": "allow", "policy": {"status": "assessed",
                                      "verdict": VERDICT, "reference": REFERENCE}}
UNASSESSED = {"gate": "allow", "policy": {"status": "unassessed"}}
ERROR = "inapplicable reference"
CASES = (
    ("original-positive", "feed-a", "feed-a", True, ASSESSED),
    ("migrated-positive", "feed-b", "feed-b", True, ASSESSED),
    ("stale-unasserted", "feed-b", "feed-a", False, UNASSESSED),
    ("stale-asserted", "feed-b", "feed-a", True, None),
)
INPUTS = {
    "selection": "selection.json", "envelope": "envelope.json", "policy": "policy.json",
    "corpus": "corpus.bin", "profile": "profile.bin", "fixture": "fixture.json",
    "caller-package": "caller-package.json", "provider-package": "provider-package.json",
    "caller-content": "caller-content.bin", "provider-content": "provider-content.bin",
    "permission": "permission.json", "resource": "resource.json",
}
API_SCRIPT = """
import json
from pathlib import Path
import sys

from policy.v2_adapter import assess_status
from policy.v2_resolver import ResolutionError

case = Path(sys.argv[1])
names = json.loads(sys.argv[2])
selection = json.loads((case / names.pop("selection")).read_bytes())
arguments = {
    name.replace("-", "_") + "_raw": (case / filename).read_bytes()
    for name, filename in names.items()
}
try:
    result = assess_status(selection=selection, **arguments)
except ResolutionError as error:
    print(json.dumps({"exception": type(error).__name__, "message": str(error)}))
    raise SystemExit(2)
print(json.dumps(result, sort_keys=True))
"""


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_bytes(encode(value) + b"\n")


def inventory(root):
    entries = {}
    for directory, dirs, files in os.walk(root):
        base = Path(directory)
        if base == root:
            dirs[:] = [name for name in dirs if name != ".git"]
        for name in sorted(dirs + files):
            path = base / name
            relative = str(path.relative_to(root))
            mode = oct(path.lstat().st_mode)
            if path.is_symlink():
                entries[relative] = {"mode": mode, "link": os.readlink(path)}
            elif path.is_file():
                contents = path.read_bytes()
                entries[relative] = {"mode": mode, "size": len(contents), "digest": digest(contents)}
            elif path.is_dir():
                entries[relative] = {"mode": mode}
            else:
                raise RuntimeError(f"Unexpected filesystem object at {path}")
    return entries


def build_case(provider_feed, policy_feed, asserted):
    corpus = b"ledger synthetic status corpus"
    profile = b"ledger synthetic status profile"
    caller_content = b"ledger synthetic status client package"
    provider_content = b"ledger synthetic status provider package"
    caller_package = encode({"role": "caller", "feed": "feed-client", "name": "ledger-client",
                             "version": "1", "content_sha256": digest(caller_content)})
    caller = "feed-client/ledger-client/1@" + digest(caller_package)
    pairs = [{"target": "status", "operation": "read"}]

    def provider(feed):
        package = encode({"role": "provider", "feed": feed, "name": "ledger-provider",
                          "version": "1", "content_sha256": digest(provider_content)})
        identity = f"{feed}/ledger-provider/1@" + digest(package)
        scope = {"caller": "status-client", "profile": digest(profile),
                 "ingress": "fixture-transport", "entrypoint": "status.read",
                 "packages": {"caller": caller, "provider": identity}}
        return package, scope

    provider_package, scope = provider(provider_feed)
    _, policy_scope = provider(policy_feed)
    fixture = encode({"scope": scope, "pairs": pairs})
    shared = {"target": "status", "operation": "read", "pairs": pairs,
              "profile": digest(profile), "corpus": digest(corpus)}
    permission = encode(dict(shared, caller=scope["caller"], package=caller,
                             ingress=scope["ingress"], entrypoint=scope["entrypoint"],
                             provider=scope["packages"]["provider"], allowed=True))
    resource = encode(dict(shared, package=scope["packages"]["provider"], available=True))
    policy = encode({"ledger-fixture": [{"id": "status", "scope": policy_scope, "pairs": pairs}]})
    context = {"corpus": digest(corpus), "profile": digest(profile), "policy": digest(policy),
               "inputs": {"status-fixture": digest(fixture), "caller-package": digest(caller_package),
                          "provider-package": digest(provider_package),
                          "permission": digest(permission), "resource": digest(resource)}}
    selection = encode({"context": context, "scope": scope, "pairs": pairs})
    envelope = encode({"kind": "readonly-assessment", "version": 2, "context": context,
                       "reference": REFERENCE if asserted else None,
                       "verdict": VERDICT if asserted else None})
    return dict(zip(INPUTS, (selection, envelope, policy, corpus, profile, fixture, caller_package,
                             provider_package, caller_content, provider_content, permission, resource),
                    strict=True))


def independent_identity_check(material):
    a = material["original-positive"]
    b = material["migrated-positive"]
    stale = material["stale-unasserted"]
    asserted = material["stale-asserted"]
    manifests = [json.loads(case["provider-package"]) for case in (a, b)]
    if [manifest.pop("feed") for manifest in manifests] != ["feed-a", "feed-b"]:
        raise RuntimeError("Provider feeds do not represent the predeclared change")
    if manifests[0] != manifests[1]:
        raise RuntimeError("Provider manifest fields beyond feed changed")
    invariant = ("corpus", "profile", "caller-package", "caller-content", "provider-content")
    if any(len({case[key] for case in material.values()}) != 1 for key in invariant):
        raise RuntimeError("An invariant input changed")
    if stale["policy"] != a["policy"]:
        raise RuntimeError("Stale policy does not retain the exact A policy bytes")
    if any(stale[key] != b[key] for key in INPUTS if key not in {"selection", "envelope", "policy"}):
        raise RuntimeError("Stale-policy test changed a B prerequisite")
    if any(stale[key] != asserted[key] for key in INPUTS if key != "envelope"):
        raise RuntimeError("Assertion test changed a non-envelope input")
    envelopes = [json.loads(case["envelope"]) for case in (stale, asserted)]
    if [(env.pop("reference"), env.pop("verdict")) for env in envelopes] != [
        (None, None), (REFERENCE, VERDICT),
    ] or envelopes[0] != envelopes[1]:
        raise RuntimeError("Assertion test changed an unexpected envelope field")
    for case in material.values():
        selection = json.loads(case["selection"])
        context = selection["context"]
        if json.loads(case["envelope"])["context"] != context:
            raise RuntimeError("Envelope and independently supplied context differ")
        for key, filename in (("status-fixture", "fixture"), ("caller-package", "caller-package"),
                              ("provider-package", "provider-package"), ("permission", "permission"),
                              ("resource", "resource")):
            if context["inputs"][key] != digest(case[filename]):
                raise RuntimeError(f"Incorrect input digest for {key}")
        for key in ("corpus", "profile", "policy"):
            if context[key] != digest(case[key]):
                raise RuntimeError(f"Incorrect context digest for {key}")


def invoke(argv, cwd, env, output):
    start = time.monotonic()
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, check=False)
    elapsed = time.monotonic() - start
    output.with_suffix(".stdout").write_bytes(result.stdout)
    output.with_suffix(".stderr").write_bytes(result.stderr)
    write_json(output.with_suffix(".json"), {
        "argv": argv, "cwd": str(cwd), "exit": result.returncode,
        "elapsed_seconds": elapsed,
        "stdout_digest": digest(result.stdout), "stderr_digest": digest(result.stderr),
    })
    return result


def compare(result, boundary, expected):
    if expected is not None:
        if result.returncode != 0 or result.stderr or len(result.stdout.splitlines()) != 1:
            return "unexpected success-case exit or streams"
        try:
            return None if json.loads(result.stdout) == expected else "unexpected result object"
        except ValueError:
            return "invalid JSON result"
    if boundary == "cli":
        return None if (result.returncode, result.stdout, result.stderr) == (
            2, b"", ERROR.encode() + b"\n") else "unexpected CLI error exit or streams"
    try:
        matches = json.loads(result.stdout) == {"exception": "ResolutionError", "message": ERROR}
    except ValueError:
        matches = False
    return None if result.returncode == 2 and not result.stderr and matches else "unexpected API exception"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer-source", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    source = args.consumer_source.resolve(strict=True)
    run = args.run_dir.resolve()
    ledger_work = Path(__file__).resolve().parent.parent
    if not run.is_relative_to(ledger_work) or not source.is_relative_to(ledger_work):
        parser.error("consumer-source and run-dir must be beneath ledger work/")
    if run.is_relative_to(source):
        parser.error("run-dir must be outside consumer-source")
    run.mkdir()
    temporary = run / "tmp"
    cache = run / "cache"
    temporary.mkdir()
    cache.mkdir()
    env = dict(os.environ, TMPDIR=str(temporary), XDG_CACHE_HOME=str(cache),
               PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1")
    env.pop("PYTHONPATH", None)
    clone = run / "consumer"
    for label, argv in (
        ("source-pin", ["git", "-C", str(source), "rev-parse", "HEAD"]),
        ("source-clean", ["git", "-C", str(source), "status", "--porcelain=v1"]),
        ("clone", ["git", "clone", "--no-hardlinks", "--no-checkout", str(source), str(clone)]),
        ("checkout", ["git", "-C", str(clone), "checkout", "--detach", PIN]),
        ("pin", ["git", "-C", str(clone), "rev-parse", "HEAD"]),
        ("clean", ["git", "-C", str(clone), "status", "--porcelain=v1"]),
        ("git-version", ["git", "--version"]),
        ("python-version", [sys.executable, "--version"]),
    ):
        result = invoke(argv, run, env, run / label)
        if (result.returncode or (label in {"source-pin", "pin"} and result.stdout.strip() != PIN.encode())
                or (label in {"source-clean", "clean"} and result.stdout)):
            raise RuntimeError(f"Preflight failed: {label}")
    write_json(run / "preflight.json", {
        "consumer_pin": PIN, "source_repository": str(source), "consumer_clean": True,
        "platform": platform.platform(), "python_executable": sys.executable,
        "python_executable_digest": digest(Path(sys.executable).read_bytes()),
        "harness_digest": digest(Path(__file__).read_bytes()),
        "disk_free_bytes": shutil.disk_usage(run).free, "cpu_count": os.cpu_count(),
        "owned_temp": str(temporary), "owned_cache": str(cache),
        "evidence_kind": "standalone synthetic v2 status boundary",
    })

    materials = {name: build_case(feed, policy, asserted)
                 for name, feed, policy, asserted, _ in CASES}
    independent_identity_check(materials)
    inputs = run / "inputs"
    inputs.mkdir()
    for name, material in materials.items():
        case = inputs / name
        case.mkdir()
        for key, contents in material.items():
            (case / INPUTS[key]).write_bytes(contents)
        for key, contents in material.items():
            if (case / INPUTS[key]).read_bytes() != contents:
                raise RuntimeError(f"Staged bytes differ for {name}/{key}")
    baseline = {"consumer": inventory(clone), "inputs": inventory(inputs)}
    write_json(run / "before.json", baseline)
    failures = []
    for name, _, _, _, expected in CASES:
        case = inputs / name
        cli = [sys.executable, "-B", "-m", "policy.v2_adapter", "--family", "status"]
        for key, filename in INPUTS.items():
            cli.extend([f"--{key}", str(case / filename)])
        api = [sys.executable, "-B", "-c", API_SCRIPT, str(case), json.dumps(INPUTS)]
        for boundary, argv in (("api", api), ("cli", cli)):
            label = f"{name}-{boundary}"
            try:
                result = invoke(["/usr/bin/sandbox-exec", "-p", "(version 1) (allow default) (deny file-write*)", *argv], clone, env, run / label)
                issue = compare(result, boundary, expected)
                if issue:
                    failures.append(f"{label}: {issue}")
            finally:
                after = {"consumer": inventory(clone), "inputs": inventory(inputs)}
                write_json(run / f"{label}.after.json", after)
                if after != baseline:
                    failures.append(f"{label}: retained artifact or input inventory changed")
                    write_json(run / "verification.json", {"passed": False, "failures": failures})
                    raise RuntimeError(failures[-1])
    write_json(run / "verification.json", {"passed": not failures, "failures": failures,
                                          "cases": len(CASES), "boundaries": ["api", "cli"]})
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
