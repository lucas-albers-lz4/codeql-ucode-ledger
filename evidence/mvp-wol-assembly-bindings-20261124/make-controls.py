from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
stage = root / 'stage/usr/share/rpcd/ucode'
base = """import { popen } from 'fs';
function transform(s) { return s; }
const methods = {
  exec: {
    call: function(request) {
      let parts = map(request.args.args, transform);
      const fd = popen('/bin/echo' + ' ' + join(' ', parts));
      return fd;
    }
  }
};
return { 'testing.wol': methods };
"""

fixtures = {
    "identity": (base, ("identity", "no-matching-comparison")),
    "fixed_args": (base.replace("request.args.args", "['fixed']"), None),
    "other_callback": (base.replace("transform);", "length);"), None),
    "no_join": (base.replace("join(' ', parts)", "parts"), None),
    "callback_shadow": (base.replace("      let parts", "      function transform(s) { return 'fixed'; }\n      let parts"), None),
    "callback_write": (base.replace("const methods", "transform = function(s) { return 'fixed'; };\nconst methods"), None),
    "parts_shadow": (base.replace("      const fd", "      if (true) {\n      let parts = ['fixed'];\n      const fd").replace("      return fd;", "      }"), None),
    "parts_write": (base.replace("      const fd", "      parts = ['fixed'];\n      const fd"), None),
    "mixed_parts": (base.replace("      const fd", "      push(parts, 'fixed');\n      const fd"), None),
    "wrong_import": (base.replace("from 'fs'", "from 'other'"), None),
    "popen_shadow": (base.replace("      let parts", "      function popen(s) { return s; }\n      let parts"), None),
    "map_shadow": (base.replace("      let parts", "      function map(a, f) { return ['fixed']; }\n      let parts"), None),
    "join_shadow": (base.replace("      let parts", "      function join(s, a) { return 'fixed'; }\n      let parts"), None),
    "overridden_method": (base.replace("  exec: {", "  exec: {},\n  exec: {"), None),
    "escaped_join": (base.replace("join(' ', parts)", r"join(' \t', parts)"), None),
    "nonreturned": (base.replace("return { 'testing.wol': methods };", "return {};"), None),
    "request_write": (base.replace("      let parts", "      request = { args: { args: ['fixed'] } };\n      let parts"), None),
    "partial_quote": (base.replace("return s;", "return \"'\" + s + \"'\";"), ("unknown", "no-matching-comparison")),
}
real = (stage / 'luci.wol').read_text()
fixtures["altered_guard"] = (real.replace("request.args.name == wakeonlan", "request.args.name != wakeonlan"), ("single-quote-body", "no-matching-comparison"))

fixtures["mixed_quoted_parts"] = (real.replace("const fd = popen", "push(parts, 'fixed');\n\t\t\t\tconst fd = popen"), None)

expected = {"usr/share/rpcd/ucode/luci.wol": [41, 42, "single-quote-body", "fixed-path-comparison"]}
for name, (source, classification) in fixtures.items():
    path = stage / (name + '.uc')
    path.write_text(source)
    if classification:
        lines = source.splitlines()
        expected[f"usr/share/rpcd/ucode/{name}.uc"] = [
            next(i for i, ln in enumerate(lines, 1) if "map(request.args.args" in ln),
            next(i for i, ln in enumerate(lines, 1) if "+ join(" in ln),
            *classification,
        ]
files = {p.relative_to(root / 'stage').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(stage.iterdir())}
(root / 'source-first/oracle.json').write_text(json.dumps({
    "luci_commit": "b2e0be4b46ec0fd43394c081fa7c50657af14011",
    "luci_blob": "fd9e9f0485ab6baec96ae089caf1089a6d471c99",
    "stage_files": files,
    "expected_successful_multiset": dict.fromkeys(files, 1),
    "expected_witnesses": expected,
    "expected_zero_witnesses": sorted(set(files) - set(expected)),
    "expected_extraction_errors": [],
}, indent=2) + "\n")
