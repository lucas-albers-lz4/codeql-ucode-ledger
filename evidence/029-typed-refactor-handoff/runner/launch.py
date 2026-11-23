#!/usr/bin/env python3
"""Serial package 20 launch after independent review; does not override HOME."""
import json,os,pathlib,subprocess,sys,time
p=pathlib.Path(__file__).resolve().parent; ledger=p.parents[1]
if len(sys.argv)!=2: raise SystemExit('argument: new run path under work/')
r=pathlib.Path(sys.argv[1]).resolve(); env=dict(os.environ,CODEQL=str(ledger.parent/'.tools/codeql-2.27.4/codeql/codeql'),PYTHONDONTWRITEBYTECODE='1'); env.pop('CODEQL_UCODE_STAGED_ROOT',None)
def call(label,argv):
 start=time.monotonic(); proc=subprocess.run(list(map(str,argv)),cwd=ledger,env=env,capture_output=True); elapsed=time.monotonic()-start
 if r.exists():
  (r/(label+'.stdout')).write_bytes(proc.stdout); (r/(label+'.stderr')).write_bytes(proc.stderr); (r/(label+'.json')).write_text(json.dumps({'argv':list(map(str,argv)),'cwd':str(ledger),'exit':proc.returncode,'elapsed_seconds':elapsed},indent=2)+'\n')
 if proc.returncode: raise RuntimeError(label+' failed: '+proc.stderr.decode('utf-8','replace')[-1000:])
try:
 call('prepare',[sys.executable,'-B',p/'prepare.py',r]); call('producer',[sys.executable,'-B',p/'run-producer.py',r/'producer',r/'consumer',r/'producer-run']); call('consumer',[sys.executable,'-B',p/'run-consumer.py',r/'consumer',r/'producer-run/typed.json',r/'producer-run/main/src',r/'producer-run/main/effects.csv',r/'consumer-run'])
 (r/'result.json').write_text('{"status":"complete"}\n')
except BaseException as e:
 if r.exists(): (r/'result.json').write_text(json.dumps({'status':'failed','error':repr(e)})+'\n')
 raise
