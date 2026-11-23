import collections,csv,datetime,json,os,pathlib,shutil,subprocess,time
from expected import expected
P=pathlib.Path(__file__).resolve().parent; R=P.parent/'run-20261122-d'; out=R/'output'; ql=R/'producer-ql/ql'; cache=R/'cache'; common=R/'common-cache'; db=R/'database/db'; codeql=P.parents[2].parent/'.tools/codeql-2.27.4/codeql/codeql'; env=dict(os.environ,TMPDIR=str(R/'tmp'),TMP=str(R/'tmp'),TEMP=str(R/'tmp'),XDG_CACHE_HOME=str(cache),CODEQL_UCODE_CACHE=str(cache),PYTHONDONTWRITEBYTECODE='1'); env.pop('CODEQL_UCODE_STAGED_ROOT',None)
ps=subprocess.run(['ps','-ax','-o','pid=,etime=,command='],capture_output=True,text=True,check=True); heavy=[x for x in ps.stdout.splitlines() if ('/codeql/codeql ' in x or 'com.semmle.cli2.CodeQL' in x) and 'ps -ax' not in x]; (R/'logs/continuation-process.json').write_text(json.dumps({'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':heavy},indent=2)+'\n')
if heavy: raise RuntimeError('CodeQL process active; no continuation')
cmds=[]
def cmd(label,argv):
 t=time.monotonic(); p=subprocess.run(['/usr/bin/time','-l',*map(str,argv)],cwd=R,env=env,capture_output=True); (out/('continuation-'+label+'.stdout')).write_bytes(p.stdout); (out/('continuation-'+label+'.stderr-time.txt')).write_bytes(p.stderr); cmds.append({'label':label,'argv':list(map(str,argv)),'exit':p.returncode,'elapsed_seconds':time.monotonic()-t}); (R/'logs/continuation-commands.json').write_text(json.dumps(cmds,indent=2)+'\n');
 if p.returncode: raise RuntimeError(label+' failed')
try:
 for n in ('roots','scopes','ast','nodes','edges'):
  shutil.copy2(P/'queries'/(n+'.ql'), ql/'src'/('pkg6-fixed-'+n+'.ql'))
  b=out/('continuation-'+n+'.bqrs'); csvp=out/('continuation-'+n+'.csv'); search=':'.join(map(str,[R/'pack/ucode-extractor-pack',ql/'lib',ql/'src']))
  cmd(n,[codeql,'query','run',ql/'src'/('pkg6-fixed-'+n+'.ql'),f'--database={db}',f'--search-path={search}',f'--common-caches={common}',f'--compilation-cache={cache}/compilation','--no-default-compilation-cache','--threads=1','--ram=2048',f'--output={b}']); cmd(n+'-decode',[codeql,'bqrs','decode','--format=csv',f'--output={csvp}',b])
 oracle=expected()
 def rows(n):
  with (out/('continuation-'+n+'.csv')).open(newline='') as f: return list(csv.reader(f))[1:]
 def check(n,a,e):
  passed=collections.Counter(map(tuple,a))==collections.Counter(map(tuple,e)); (out/('continuation-assert-'+n+'.json')).write_text(json.dumps({'passed':passed,'actual':a,'expected':e},indent=2)+'\n');
  if not passed: raise AssertionError(n)
 for n in ('roots','scopes','nodes','edges'): check(n,rows(n),oracle[n])
 wanted={tuple(x[:-1]) for x in oracle['ast_selected']}; check('ast-selected',[x for x in rows('ast') if tuple(x[:-1]) in wanted],oracle['ast_selected'])
 (R/'logs/continuation-result.json').write_text(json.dumps({'status':'complete','commands':len(cmds)})+'\n')
except BaseException as e:
 (R/'logs/continuation-result.json').write_text(json.dumps({'status':'failed','error':repr(e),'commands':len(cmds)})+'\n'); raise
