#!/usr/bin/env python3
"""Run direct getFeatures query over positive and near-miss source controls."""
import json, os, subprocess, sys
from pathlib import Path
repo,run=(Path(x).resolve() for x in sys.argv[1:]);run.mkdir(parents=True,exist_ok=False)
src=run/'src';db=run/'db';pack=repo/'extractor-pack';commands=[]
programs={'positive':"import { popen } from 'fs';\nlet methods = {\n  getFeatures: { call: function() { popen('x'); system('x'); } },\n  other: { call: function() { popen('x'); system('x'); } }\n};\n", 'wrong-import':"import { popen } from 'other';\nlet methods = {\n  getFeatures: { call: function() { popen('x'); } }\n};\n"}
for name,program in programs.items():
 p=src/f'modules/{name}/root/usr/share/rpcd/ucode/luci';p.parent.mkdir(parents=True);p.write_text(program)
def call(args,out=None):
 p=subprocess.run(list(map(str,args)),cwd=repo,capture_output=True,text=True,env={k:v for k,v in os.environ.items() if k!='CODEQL_UCODE_STAGED_ROOT'}); commands.append({'argv':list(map(str,args)),'exit':p.returncode,'stderr':p.stderr}); (run/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert p.returncode==0,p.stderr
 if out:out.write_text(p.stdout)
call(['codeql','database','init',db,'--language=ucode',f'--search-path={pack}',f'--source-root={src}'])
call(['codeql','database','index-files',db,'--language=ucode','--include=**/rpcd/ucode/luci',f'--working-dir={src}'])
(run/'routing.json').write_bytes((db/'trap/ucode/routing.json').read_bytes());call(['codeql','database','finalize',db])
for name,query in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('results','m4/GetFeaturesDirectExec.ql')]:
 b=run/(name+'.bqrs');call(['codeql','query','run',repo/'ql/src'/query,f'--database={db}',f'--search-path={pack}:{repo}/ql/lib:{repo}/ql/src',f'--output={b}','--threads=1','--ram=2048']);call(['codeql','bqrs','decode','--format=json','--entities=url,string',b],run/(name+'.json'))
e=json.loads((run/'extracted.json').read_text())['#select']['tuples']; errors=json.loads((run/'errors.json').read_text())['#select']['tuples']; results=json.loads((run/'results.json').read_text())['#select']['tuples']
assert len(e)==2 and {r[0]['url']['uri'] for r in e}=={p.as_uri() for p in src.rglob('luci')} and not errors
assert len(results)==2 and {r[3] for r in results}=={'popen','system'} and all('/modules/positive/' in r[0]['url']['uri'] and r[0]['url']['startLine']==3 for r in results),results
print('two eligible positives; wrong method and wrong import excluded')
