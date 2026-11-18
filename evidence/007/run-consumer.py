#!/usr/bin/env python3
"""Exercise the setBlockDetect table adapter with an actual producer CSV."""
import csv, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
base, table, source, run = (Path(x).resolve() for x in sys.argv[1:])
run.mkdir(parents=True, exist_ok=False)
target='m4:effect:luci-setBlockDetect-system'
paths=['reports/m4-block-device-exec.json','reports/handler_effects.json']
protected=['policy/grants.json','policy/policy_decisions.json']
commands=[]
def sha(data): return hashlib.sha256(data).hexdigest()
def call(argv,cwd):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 commands.append({'argv':list(map(str,argv)),'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); (run/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); return p
def clone(name):
 dest=run/name
 for cmd in (['git','clone','--quiet','--no-hardlinks','--local',base,dest],['git','-C',dest,'checkout','--detach','a8bdef3c22c8d5ba9999baa978052b59bd22907e']):
  p=call(cmd,run); assert p.returncode==0,p.stderr
 return dest
def snap(root): return {p:(root/p).read_bytes() for p in paths+protected}
def hashes(s): return {k:sha(v) for k,v in s.items()}
def invoke(root,csvfile,source_root): return call([sys.executable,'-B','-m','policy.setblock_table','--csv',csvfile,'--source-root',source_root],root)
def verify(before,after):
 for key in protected: assert before[key]==after[key],key
 for key in paths:
  prior=json.loads(before[key]); result=json.loads(after[key]); a=[r for r in prior if r.get('record_id')!=target]; b=[r for r in result if r.get('record_id')!=target]
  assert a==b
  rows=[r for r in result if r.get('record_id')==target]; assert len(rows)==1
  row=rows[0]; assert row['analysis_revision']=='step3:setblock-table-v1' and row['assessment']=='intended_access' and row['expectation_id']=='luci-mod-system-mounts'
  assert row['source_location']=={'path':'usr/share/rpcd/ucode/luci','start_line':532,'start_column':21,'end_line':532,'end_column':68}
  assert {'policy:grant:luci-mod-system-mounts:ubus_http:luci.setBlockDetect','policy:grant:root:ubus_http:luci.setBlockDetect'} <= set(row['evidence_refs'])
r=clone('positive'); before=snap(r); p=invoke(r,table,source); assert p.returncode==0,p.stderr; after=snap(r); verify(before,after); p=invoke(r,table,source); assert p.returncode==0,p.stderr; again=snap(r); assert after==again
summary={'table_sha256':sha(table.read_bytes()),'source_sha256':sha((source/'usr/share/rpcd/ucode/luci').read_bytes()),'positive':{'before':hashes(before),'after':hashes(after),'reimport_identical':True},'negatives':{}}
wrong=run/'wrong.csv'
with table.open(newline='') as f: rows=list(csv.reader(f))
rows[1][5]='533'
with wrong.open('w',newline='') as f: csv.writer(f,lineterminator='\n').writerows(rows)
wrongroot=run/'wrong-root'; shutil.copytree(source,wrongroot); f=wrongroot/'usr/share/rpcd/ucode/luci'; f.write_bytes(f.read_bytes()+b'\n')
for name,csvfile,root in [('wrong-row',wrong,source),('wrong-source',table,wrongroot)]:
 r=clone(name); before=snap(r); p=invoke(r,csvfile,root); after=snap(r); assert p.returncode!=0 and before==after,(name,p.stderr)
 summary['negatives'][name]={'exit':p.returncode,'unchanged':True,'artifacts':hashes(after),'error':p.stderr.strip().splitlines()[-1]}
(run/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print('positive and two rejected controls passed')
