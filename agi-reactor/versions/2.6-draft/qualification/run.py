"""Run the local contract suite, mutation controls and admission-only timing."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parent

def run_suite(path, names):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,'-m','unittest','-v',*names],cwd=path,env=env,capture_output=True,text=True,timeout=90)
    return {'exit':p.returncode,'output':p.stdout+p.stderr}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('qualification-result.json'));args=parser.parse_args()
    baseline=run_suite(ROOT,['test_kernel'])
    controls=[]
    mutations=[('disabled-fence','ok,code,_=fence_verdict(row,token[\'fence\'],time.time())',"ok,code,_=(True,'bypassed','')",'test_kernel.KernelContract.test_stale_attempt_has_no_effect'),('unsafe-replay',"raise Refused('OUTCOME_UNKNOWN' if old['state']=='UNKNOWN' else 'ALREADY_SETTLED')","a.execute('DELETE FROM operations WHERE id=?',(operation,))",'test_kernel.KernelContract.test_crash_after_acceptance_does_not_replay')]
    for name,old,new,test in mutations:
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            for f in ROOT.glob('*.py'):shutil.copyfile(f,d/f.name)
            p=d/'kernel.py';text=p.read_text();assert text.count(old)==1;p.write_text(text.replace(old,new))
            result=run_suite(d,[test]);controls.append({'mutation':name,'detected':result['exit']!=0 and 'Refused not raised' in result['output'],**result})
    # Local control-path timing, not full gateway or external delivery latency.
    from kernel import Kernel
    from test_kernel import ARGS
    samples=[]
    with tempfile.TemporaryDirectory() as d:
        k=Kernel.initialize(Path(d)/'kernel',cap=120)
        for i in range(120):
            tid=f'bench-{i}';k.create_ticket(tid,'agent-a');token=k.claim(tid,'agent-a')
            start=time.perf_counter_ns();k.admit(token,f'op-{i}','report',ARGS);elapsed=(time.perf_counter_ns()-start)/1e6
            if i>=20:samples.append(elapsed)
    sorted_samples=sorted(samples)
    report={'specimen':'Reactor local contract demonstrator 0.1','observed_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'python':platform.python_version(),'platform':platform.platform(),'evidence_class':'local source-derived composition; not deployed Qthonic qualification','baseline':baseline,'mutation_controls':controls,'admission_timing':{'samples':len(samples),'warmup':20,'median_ms':statistics.median(samples),'p95_ms':sorted_samples[94],'max_ms':max(samples),'scope':'single-host fcntl + SQLite + Python allowlist + custody check + committed effect reservation/evidence; excludes Cedar, NATS, network, model, human review and external effect'},'observed_limitations':['Permitted misleading report content is accepted. No semantic safety claim.','Classification is a declared fixture label, not verified content classification.','Effects admitted before stop may be accepted after stop.','UNKNOWN stays reserved; no automated reconciliation or recovery-release gate is implemented.','Authority journal and revocations must survive the work-only restore. Complete authority-store rollback is unqualified.','Caller identity and OS isolation are fixture assumptions.','No model calls, deployed gateway, cross-host consensus, power-loss or production capacity testing.'],'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('*.py'))}}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'baseline_exit':baseline['exit'],'mutation_controls':[{'mutation':c['mutation'],'detected':c['detected']} for c in controls],'timing':report['admission_timing'],'report':str(args.output)},indent=2))
    return 0 if baseline['exit']==0 and all(c['detected'] for c in controls) else 1

if __name__=='__main__':sys.exit(main())
