#!/usr/bin/env python3
"""Fresh selected-source markup/plain extraction and syntax inventory. REPO RUN_ROOT."""
import csv,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
repo,root=(Path(x).resolve() for x in sys.argv[1:]); src=root/'src'; out=root/'output-final'; out.mkdir(exist_ok=False); db=out/'db'; pack=repo/'extractor-pack'
codeql=os.environ.get('CODEQL', 'codeql')
env={**os.environ,'HOME':str(root/'home'),'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(root/'tmp')}; env.pop('CODEQL_UCODE_STAGED_ROOT',None)
log=[]
def call(label,cmd,*,environment=env,output=None):
 cmd=list(map(str,cmd)); t=time.monotonic(); p=subprocess.run(['/usr/bin/time','-l',*cmd],cwd=repo,env=environment,capture_output=True)
 (out/(label+'.stdout')).write_bytes(p.stdout); (out/(label+'.stderr')).write_bytes(p.stderr)
 if output is not None: output.write_bytes(p.stdout)
 log.append({'label':label,'argv':cmd,'cwd':str(repo),'exit':p.returncode,'wall_seconds':round(time.monotonic()-t,3),'stderr_and_time':label+'.stderr'})
 (out/'commands.json').write_text(json.dumps(log,indent=2)+'\n')
 if p.returncode: raise RuntimeError(f'{label} exited {p.returncode}; see log')
call('init',[codeql,'database','init',db,'--language=ucode',f'--search-path={pack}',f'--source-root={src}'])
staged={**env,'CODEQL_UCODE_STAGED_ROOT':str(src)}
call('index',[codeql,'database','index-files',db,'--language=ucode','--include=**/uhttpd.uc','--include=**/plain.uc','--include=**/member.ut',f'--working-dir={src}'],environment=staged)
shutil.copyfile(db/'trap/ucode/routing.json',out/'routing.json')
call('finalize',[codeql,'database','finalize',db])
qlpath=f'{pack}:{repo}/ql/lib:{repo}/ql/src'
for name, query in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('calls','MarkupCalls.ql')]:
 bqrs=out/(name+'.bqrs'); call(name+'-query',[codeql,'query','run',repo/'ql/src'/query,f'--database={db}',f'--search-path={qlpath}',f'--output={bqrs}','--threads=1','--ram=2048'])
 call(name+'-decode',[codeql,'bqrs','decode','--format=csv',bqrs],output=out/(name+'.csv'))
print('database and query commands completed; inspect output against pre-run oracle')
