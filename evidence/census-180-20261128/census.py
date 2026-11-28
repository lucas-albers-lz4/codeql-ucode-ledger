#!/usr/bin/env python3
"""Census for codeql-ucode#180: grammar node kinds vs dbscheme/AST/CFG/data-flow layers.

Reads only pinned sources:
  - grammar: 4a243af329fae2f4ff01e0fc80133cbab8314600 node-types.json (ucode, ucode_markup)
  - producer: 9166af76cf6944e1b3ea5856a9176366a1f7a6ee ql/lib (dbscheme, ast/internal, CFG, DataFlow)
Writes census.json + census.md. Deterministic; no execution, no gate changes.
"""
import json, re, subprocess, sys
from pathlib import Path

PROD = Path('/root/workspace/work/security-extension-20261125/routing-remeasure/producer')
GRAM = PROD / 'extractor/tree-sitter'
P = '9166af76cf6944e1b3ea5856a9176366a1f7a6ee'

def show(path):
    r = subprocess.run(['git', '-C', str(PROD), 'show', f'{P}:{path}'],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

def camel(kind):
    return ''.join(p.title() for p in re.split(r'[_]', kind) if p)

# ---- layer 0: grammar named kinds
def named_kinds(rel):
    data = json.loads((GRAM / rel).read_text())
    return [n['type'] for n in data if n.get('named')]

ucode_kinds = named_kinds('ucode/src/node-types.json')
markup_kinds = named_kinds('ucode_markup/src/node-types.json')

# ---- layer 1: dbscheme entity tables
ds = show('ql/lib/ucode.dbscheme') or ''
# entity declarations look like: [name="foo"] bar(...) or type Foo = ...
ds_lower = ds.lower()
ds_tables = set(re.findall(r'case (\d+) = \w+|"([a-z][a-z0-9_]+)"', ds))
ds_table_names = set(m[1] for m in re.findall(r'\[name="([^"]+)"\]', ds))
# fallback: any identifier in a decl position
ds_decl_names = set(re.findall(r'^(?:\[name="([^"]+)"\]\s*)?(\w+)\s*\(', ds, re.M))

def in_dbscheme(kind):
    k = kind.lower()
    c = camel(kind).lower()
    hay = [k, c, 'ucode_' + k, 'ucode_' + c, 'node_' + k]
    for h in hay:
        if h in ds_lower:
            return True
    return False

# ---- layer 2: AST mapping files
ast_files = {}
r = subprocess.run(['git', '-C', str(PROD), 'ls-tree', '-r', '--name-only', P,
                    'ql/lib/codeql/ucode/ast/internal/'], capture_output=True, text=True)
for line in r.stdout.splitlines():
    m = re.search(r'internal/([A-Za-z0-9]+)\.qll$', line)
    if m:
        ast_files[m.group(1).lower()] = line

def ast_class_ref(kind, camel_kind):
    # AST.qll or ast/*.qll mentioning the kind string directly
    for f in ['ql/lib/codeql/ucode/AST.qll']:
        t = show(f) or ''
        if f'"{kind}"' in t:
            return f'{f} (kind literal)'
    return None

# ---- layer 3: CFG + data-flow references (kind literals or camel class names)
flow_files = {
    'CFG.qll': 'ql/lib/codeql/ucode/CFG.qll',
    'BasicBlocks': 'ql/lib/codeql/ucode/controlflow/BasicBlocks.qll',
    'CfgNodes': 'ql/lib/codeql/ucode/controlflow/CfgNodes.qll',
    'ControlFlowGraph': 'ql/lib/codeql/ucode/controlflow/ControlFlowGraph.qll',
    'DataFlow': 'ql/lib/codeql/ucode/DataFlow.qll',
}
flow_text = {}
for key, path in flow_files.items():
    flow_text[key] = show(path) or ''
# internal subdirs
for subdir in ['ql/lib/codeql/ucode/controlflow/internal/', 'ql/lib/codeql/ucode/dataflow/']:
    rr = subprocess.run(['git', '-C', str(PROD), 'ls-tree', '-r', '--name-only', P, subdir],
                        capture_output=True, text=True)
    for line in rr.stdout.splitlines():
        if line.endswith('.qll'):
            flow_text['file:' + Path(line).stem] = show(line) or ''

def flow_refs(kind, camel_kind):
    hits = []
    kpat = re.compile(r'"' + re.escape(kind) + r'"')
    cpat = re.compile(r'\b' + re.escape(camel(kind)) + r'\b')
    for name, text in flow_text.items():
        if kpat.search(text):
            hits.append(f'{name}:kind-literal')
        elif cpat.search(text):
            hits.append(f'{name}:class-ref')
    return hits

def census(kinds):
    rows = []
    for k in kinds:
        ck = camel(k)
        d = in_dbscheme(k)
        a = k.replace('_', '').lower() in ast_files or ck.lower() in ast_files
        ast_path = ast_files.get(ck.lower()) or ast_files.get(k.replace('_', '').lower())
        fl = flow_refs(k, ck)
        if not d:
            cls = 'absent-or-transparent'
        elif a and fl:
            cls = 'extracted+ast+flow'
        elif a:
            cls = 'extracted+ast'
        else:
            cls = 'extracted-only'
        rows.append({'kind': k, 'dbscheme': d, 'ast': bool(a), 'ast_file': ast_path,
                     'flow': fl, 'class': cls})
    return rows

res = {'pin_producer': P, 'pin_grammar': '4a243af329fae2f4ff01e0fc80133cbab8314600',
       'ucode': census(ucode_kinds), 'markup': census(markup_kinds)}

out = Path('/root/workspace/work/security-extension-20261125/census-180')
out.mkdir(exist_ok=True)
(out / 'census.json').write_text(json.dumps(res, indent=1))
for gram in ('ucode', 'markup'):
    counts = {}
    for row in res[gram]:
        counts[row['class']] = counts.get(row['class'], 0) + 1
    print(gram, len(res[gram]), counts)
print('wrote', out / 'census.json')
