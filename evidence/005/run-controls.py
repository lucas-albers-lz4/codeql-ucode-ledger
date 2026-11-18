#!/usr/bin/env python3
"""Control non-fs named import versus fs for ImportedCalleeTaint."""
import json, os, subprocess, sys
from pathlib import Path
repo,run=(Path(x).resolve() for x in sys.argv[1:]); run.mkdir(parents=True,exist_ok=False)
src=run/'src'; db=run/'db'; pack=repo/'extractor-pack'; log=[]
for label,module in [('positive','luci.sys'),('negative-fs','fs')]:
 f=src/f'modules/{label}/root/usr/share/rpcd/ucode/luci'; f.parent.mkdir(parents=True)
 f.write_text("import { init_action } from '"+module+"';\nlet methods = {\n  setInitAction: { call: function(request) {\n    init_action(request.args.name);\n  } }\n};\n")
def call(args,output=None):
 p=subprocess.run(list(map(str,args)),cwd=repo,capture_output=True,text=True,env={k:v for k,v in os.environ.items() if k!='CODEQL_UCODE_STAGED_ROOT'}); log.append({'argv':list(map(str,args)),'exit':p.returncode,'stderr':p.stderr}); (run/'commands.json').write_text(json.dumps(log,indent=2)+'\n'); assert p.returncode==0,p.stderr
 if output: output.write_text(p.stdout)
call(['codeql','database','init',db,'--language=ucode',f'--search-path={pack}',f'--source-root={src}'])
call(['codeql','database','index-files',db,'--language=ucode','--include=**/rpcd/ucode/luci',f'--working-dir={src}'])
(run/'routing.json').write_bytes((db/'trap/ucode/routing.json').read_bytes())
call(['codeql','database','finalize',db])
for name,query in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('observations','m4/ImportedCalleeTaint.ql')]:
 b=run/(name+'.bqrs'); call(['codeql','query','run',repo/'ql/src'/query,f'--database={db}',f'--search-path={pack}:{repo}/ql/lib:{repo}/ql/src',f'--output={b}','--threads=1','--ram=2048']); call(['codeql','bqrs','decode','--format=json','--entities=url,string',b],run/(name+'.json'))
e=json.loads((run/'extracted.json').read_text())['#select']['tuples']; errors=json.loads((run/'errors.json').read_text())['#select']['tuples']; rows=json.loads((run/'observations.json').read_text())['#select']['tuples']
assert len(e)==2 and {r[0]['url']['uri'] for r in e}=={p.as_uri() for p in src.rglob('luci')} and not errors
assert len(rows)==1 and '/modules/positive/' in rows[0][0]['url']['uri'] and rows[0][0]['url']['startLine']==4 and rows[0][2]['url']['startLine']==4 and rows[0][3]=='init_action',rows
print('positive imported call observed; fs import excluded; both extracted')
