#!/usr/bin/env python3
"""Exercise actual getblock adapter in isolated copies; BASE PRODUCER_RUN RUN."""
import csv, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
base, prod, run=(Path(x).resolve() for x in sys.argv[1:]); run.mkdir(parents=True,exist_ok=False)
table=prod/'main/effects.csv'; source=prod/'main/src'; target='m4:effect:luci-getBlockDevices-popen'
artifacts=['reports/m4-block-device-exec.json','reports/handler_effects.json']
log=[]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def call(argv,cwd):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 log.append({'cwd':str(cwd),'argv':list(map(str,argv)),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); (run/'commands.json').write_text(json.dumps(log,indent=2)+'\n'); return p

def clone(name):
 dest=run/name; p=call(['git','clone','--quiet','--no-hardlinks','--local',base,dest],run); assert p.returncode==0,p.stderr
 p=call(['git','-C',dest,'checkout','--detach','a8bdef3c22c8d5ba9999baa978052b59bd22907e'],run); assert p.returncode==0,p.stderr
 return dest

def snapshots(repo): return {x:(repo/x).read_bytes() for x in artifacts}
def import_table(repo,csvfile,root): return call([sys.executable,'-B','-m','policy.getblock_table','--csv',csvfile,'--source-root',root],repo)
def records(b): return json.loads(b)
def others(rows): return [r for r in rows if r.get('record_id')!=target]
def verify(before,after):
 for path in artifacts:
  a,b=records(before[path]),records(after[path]); old=[r for r in a if r.get('record_id')==target]; new=[r for r in b if r.get('record_id')==target]
  assert len(old)==len(new)==1 and others(a)==others(b)
  row=new[0]; assert row['analysis_revision']=='step3:getblock-table-v1' and row['assessment']=='intended_access' and row['expectation_id']=='luci-mod-system-mounts'
  assert row['source_location']=={'path':'usr/share/rpcd/ucode/luci','start_line':481,'start_column':18,'end_line':481,'end_column':54}
  assert {'policy:grant:luci-mod-system-mounts:ubus_http:luci.getBlockDevices','policy:grant:root:ubus_http:luci.getBlockDevices'} <= set(row['evidence_refs'])
summary={'producer_table_sha256':digest(table),'source_sha256':digest(source/'usr/share/rpcd/ucode/luci'),'cases':{}}
repo=clone('valid'); before=snapshots(repo); grants=digest(repo/'policy/grants.json')
p=import_table(repo,table,source); assert p.returncode==0,p.stderr; after=snapshots(repo); verify(before,after); assert digest(repo/'policy/grants.json')==grants
p=import_table(repo,table,source); assert p.returncode==0,p.stderr; again=snapshots(repo); assert after==again
summary['cases']['current_and_reimport']={'before':{k:hashlib.sha256(v).hexdigest() for k,v in before.items()},'after':{k:hashlib.sha256(v).hexdigest() for k,v in after.items()},'reimport_identical':True}
repo=clone('seeded');
for path in artifacts:
 f=repo/path; rows=json.loads(f.read_text()); matches=[r for r in rows if r.get('record_id')==target]; assert len(matches)==1; matches[0]['analysis_revision']='ledger-seeded-prior'; f.write_text(json.dumps(rows,indent=2)+'\n')
before=snapshots(repo); p=import_table(repo,table,source); assert p.returncode==0,p.stderr; after=snapshots(repo); verify(before,after)
assert all(before[k]!=after[k] for k in artifacts)
summary['cases']['seeded_replacement']={'before':{k:hashlib.sha256(v).hexdigest() for k,v in before.items()},'after':{k:hashlib.sha256(v).hexdigest() for k,v in after.items()},'seed':'target analysis_revision set to ledger-seeded-prior'}
wrongroot=run/'bad-source'; shutil.copytree(source,wrongroot); f=wrongroot/'usr/share/rpcd/ucode/luci'; f.write_bytes(f.read_bytes()+b'\n')
wrongtable=run/'bad-row.csv'
with table.open(newline='') as f: rows=list(csv.reader(f))
rows[1][5]='482'
with wrongtable.open('w',newline='') as f: csv.writer(f,lineterminator='\n').writerows(rows)
for name,csvfile,root in [('bad-source',table,wrongroot),('bad-row',wrongtable,source)]:
 repo=clone(name+'-consumer'); before=snapshots(repo); p=import_table(repo,csvfile,root); after=snapshots(repo); assert p.returncode!=0 and before==after,(name,p.stderr)
 summary['cases'][name]={'exit':p.returncode,'unchanged':True,'artifact_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in after.items()},'error_last_line':p.stderr.strip().splitlines()[-1]}
(run/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print('valid, seeded replacement, reimport and both rejected controls verified')
