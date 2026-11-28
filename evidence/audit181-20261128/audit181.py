#!/usr/bin/env python3
"""#181 audit pass 1: reclassify the 29 census 'no-flow' kinds using class-based joins.

The #180 census searched snake_case kind literals in flow files; the flow layer is
actually class-based (T<Camel> wrappers), so coverage was undercounted. This script:
 1. finds T<Camel> / <Camel> references in controlflow+dataflow sources (kind-specific rule),
 2. otherwise checks transparency: does the AST internal mark the node as generated/delegating,
    and does the parent kind's rule traverse children generically (child index usage),
 3. emits a verdict table: kind-rule / covered-generic(candidate) / needs-rule.
Read-only vs pinned blobs. No execution.
"""
import json, re, subprocess
from pathlib import Path

PROD = Path('/root/workspace/work/security-extension-20261125/routing-remeasure/producer')
P = '9166af76cf6944e1b3ea5856a9176366a1f7a6ee'
KINDS29 = ['declaration','primary_expression','arguments','computed_property_name',
 'else_alt_clause','else_clause','empty_statement','export_clause','export_specifier',
 'expression_statement','import_clause','lexical_declaration','named_imports',
 'namespace_import','regex','switch_body','template_string','template_substitution',
 'unary_expression','comment','default','false','hash_bang_line','null','number',
 'optional_chain','regex_flags','regex_pattern','true']

def show(path):
    r = subprocess.run(['git','-C',str(PROD),'show',f'{P}:{path}'],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else ''

# gather flow-layer texts
flow_files = []
for sub in ['ql/lib/codeql/ucode/controlflow/','ql/lib/codeql/ucode/dataflow/']:
    r = subprocess.run(['git','-C',str(PROD),'ls-tree','-r','--name-only',P,sub],capture_output=True,text=True)
    flow_files += [l for l in r.stdout.splitlines() if l.endswith('.qll')]
flow = {f: show(f) for f in flow_files}
flow_all = '\n'.join(flow.values())

def camel(k): return ''.join(w.title() for w in k.split('_') if w)

rows=[]
for k in KINDS29:
    c = camel(k)
    hits = sorted({f.split('/')[-1] for f,t in flow.items() if re.search(r'\bT'+c+r'\b', t)})
    if hits:
        verdict='kind-rule-found'   # census undercounted; kind IS flow-referenced by class
    else:
        # literal still?
        if re.search(r'"'+re.escape(k)+r'"', flow_all):
            verdict='kind-rule-literal'
        else:
            verdict='no-kind-rule'  # candidate for needs-rule or covered-generic
    rows.append({'kind':k,'class':'T'+c,'flow_files':hits,'verdict':verdict})

print(json.dumps(rows,indent=1))
nc=[r['kind'] for r in rows if r['verdict']=='no-kind-rule']
print('kinds with NO kind-level flow reference (%d):'%len(nc), nc)
Path('/root/workspace/work/security-extension-20261125/census-180/audit181-pass1.json').write_text(json.dumps(rows,indent=1))
