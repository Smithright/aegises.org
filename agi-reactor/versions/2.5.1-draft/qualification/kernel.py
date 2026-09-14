"""Local contract demonstrator. NOT a production security boundary.

One trusted host, fcntl-serialized admission and two SQLite stores:
work.sqlite owns tickets. authority.sqlite owns current epoch, grants, effect
journal and reservations, and is explicitly OUTSIDE the restored work snapshot.
Caller identity is supplied by the test harness, not cryptographically verified.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import time
import urllib.parse
import urllib.request
from qthonic_decisions import grant, fence_verdict


class Refused(Exception):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class Kernel:
    def __init__(self, root):
        self.root = Path(root)
        for name in ('work.sqlite', 'authority.sqlite', 'lock'):
            if not (self.root/name).is_file():
                raise Refused('MISSING_DURABLE_STATE')

    @classmethod
    def initialize(cls, root, cap=4):
        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        if any(root.iterdir()):
            raise ValueError('Use an empty disposable directory')
        (root/'lock').touch()
        with sqlite3.connect(root/'work.sqlite') as c:
            c.execute('CREATE TABLE tickets(id TEXT PRIMARY KEY, row TEXT NOT NULL)')
        with sqlite3.connect(root/'authority.sqlite') as c:
            c.executescript('''
            CREATE TABLE control(id INTEGER PRIMARY KEY CHECK(id=1), epoch INTEGER, stopped INTEGER, cap INTEGER);
            CREATE TABLE grants(principal TEXT PRIMARY KEY, recipient TEXT, classification TEXT, active INTEGER);
            CREATE TABLE operations(id TEXT PRIMARY KEY, work_key TEXT UNIQUE, digest TEXT, intent TEXT, state TEXT, reservation INTEGER);
            CREATE TABLE evidence(seq INTEGER PRIMARY KEY, kind TEXT, record TEXT);
            CREATE TABLE routes(method TEXT PRIMARY KEY, endpoint TEXT);
            ''')
            c.execute('INSERT INTO control VALUES(1,1,0,?)', (cap,))
            c.execute('INSERT INTO routes VALUES(?,?)',('report.send','http://127.0.0.1:1/reports'))
            c.executemany('INSERT INTO grants VALUES(?,?,?,1)', [('agent-a','leaders@example.invalid','public'),('agent-b','leaders@example.invalid','public')])
        return cls(root)

    @contextmanager
    def locked(self):
        # All authoritative transitions go through this one trusted local writer.
        # fsync/SQLite cover process-crash tests; power loss is NOT qualified here.
        with (self.root/'lock').open('r+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with sqlite3.connect(self.root/'authority.sqlite', timeout=10) as authority:
                authority.row_factory = sqlite3.Row
                with sqlite3.connect(self.root/'work.sqlite', timeout=10) as work:
                    work.row_factory = sqlite3.Row
                    yield work, authority

    @staticmethod
    def record(a, kind, data):
        a.execute('INSERT INTO evidence(kind,record) VALUES(?,?)', (kind,json.dumps(data,sort_keys=True)))

    @staticmethod
    def ticket(w, ticket):
        row = w.execute('SELECT row FROM tickets WHERE id=?', (ticket,)).fetchone()
        if row is None:
            raise Refused('NO_TICKET')
        return json.loads(row['row'])

    def create_ticket(self, ticket, assignee):
        # Trusted fixture setup. An operational implementation needs admission here too.
        with self.locked() as (w,a):
            if not a.execute('SELECT 1 FROM grants WHERE principal=?',(assignee,)).fetchone():
                raise Refused('UNKNOWN_ASSIGNEE')
            w.execute('INSERT INTO tickets VALUES(?,?)',(ticket,json.dumps({'id':ticket,'status':{'value':'open'},'assignee':assignee,'steps':['report']})))

    def configure_target(self, url):
        # Trusted fixture provisioning only; workers do not own the routing map.
        u=urllib.parse.urlsplit(url)
        if u.scheme!='http' or u.hostname!='127.0.0.1' or u.username or u.password:
            raise Refused('LOOPBACK_ONLY')
        with self.locked() as (_,a):
            a.execute('UPDATE routes SET endpoint=? WHERE method=?',(url,'report.send'))

    def claim(self, ticket, principal, ttl=60):
        with self.locked() as (w,a):
            control = a.execute('SELECT * FROM control').fetchone()
            if control['stopped']:
                raise Refused('STOPPED')
            if not a.execute('SELECT 1 FROM grants WHERE principal=? AND active=1',(principal,)).fetchone():
                raise Refused('REVOKED')
            row = self.ticket(w,ticket)
            if row['assignee'] != principal:
                raise Refused('NOT_ASSIGNEE')
            if row.get('epoch') != control['epoch']:
                row.update(lease_holder=None,lease_expiry=0)
            ok, code, _, patch, lease = grant(row,principal,time.time(),ttl=ttl)
            if not ok:
                raise Refused(code)
            row.update(patch,epoch=control['epoch'])
            w.execute('UPDATE tickets SET row=? WHERE id=?',(json.dumps(row),ticket))
            return {'principal':principal,'ticket':ticket,'epoch':control['epoch'],'fence':lease['fence']}

    def admit(self, token, operation, step, arguments, endpoint=None):
        token=json.loads(json.dumps(token))
        arguments=json.loads(json.dumps(arguments))
        intent={'tenant':'specimen','caller':token['principal'],'method':'report.send','target':arguments.get('recipient'),'arguments':arguments,'ticket':token['ticket'],'step':step}
        work_key=json.dumps(['specimen',token['ticket'],step])
        with self.locked() as (w,a):
            c=a.execute('SELECT * FROM control').fetchone()
            if c['stopped']: raise Refused('STOPPED')
            if token['epoch'] != c['epoch']: raise Refused('STALE_EPOCH')
            row=self.ticket(w,token['ticket'])
            if step not in row['steps']: raise Refused('UNKNOWN_WORK_STEP')
            if row.get('epoch') != c['epoch']: raise Refused('STALE_EPOCH')
            if row.get('lease_holder') != token['principal'] or row['assignee'] != token['principal']:
                raise Refused('NOT_HOLDER')
            if type(token['fence']) is not int: raise Refused('MALFORMED_FENCE')
            ok,code,_=fence_verdict(row,token['fence'],time.time())
            if not ok: raise Refused(code)
            g=a.execute('SELECT * FROM grants WHERE principal=?',(token['principal'],)).fetchone()
            if not g or not g['active']: raise Refused('REVOKED')
            if set(arguments) != {'recipient','classification','body'}: raise Refused('ARGUMENT_SCHEMA')
            if not all(isinstance(v,str) for v in arguments.values()): raise Refused('ARGUMENT_SCHEMA')
            if len(arguments['body']) > 4096: raise Refused('ARGUMENT_SCHEMA')
            if arguments['recipient'] != g['recipient']: raise Refused('RECIPIENT_SCOPE')
            if arguments['classification'] != g['classification']: raise Refused('DATA_SCOPE')
            route=a.execute('SELECT endpoint FROM routes WHERE method=?',('report.send',)).fetchone()
            if not route: raise Refused('NO_ROUTE')
            if endpoint is not None and endpoint != route['endpoint']: raise Refused('ENDPOINT_SCOPE')
            intent['endpoint']=route['endpoint']
            frozen=json.dumps(intent,sort_keys=True,separators=(',', ':')).encode()
            old=a.execute('SELECT * FROM operations WHERE id=? OR work_key=?',(operation,work_key)).fetchone()
            if old:
                if old['id'] != operation: raise Refused('STEP_ALREADY_BOUND')
                if old['digest'] != digest(intent): raise Refused('INTENT_MISMATCH')
                raise Refused('OUTCOME_UNKNOWN' if old['state']=='UNKNOWN' else 'ALREADY_SETTLED')
            reserved=a.execute('SELECT COALESCE(SUM(reservation),0) FROM operations').fetchone()[0]
            if reserved+1 > c['cap']: raise Refused('CUMULATIVE_LIMIT')
            # Commit UNKNOWN BEFORE dispatch, retaining the reservation even if the
            # worker dies before send. This deliberately sacrifices liveness.
            a.execute('INSERT INTO operations VALUES(?,?,?,?,?,1)',(operation,work_key,digest(intent),frozen.decode(),'UNKNOWN'))
            self.record(a,'admitted',{'operation':operation,'epoch':token['epoch'],'fence':token['fence'],'digest':digest(intent)})
        return frozen

    def execute(self, token, operation, step, arguments, url, crash_after_200=False, before_send=None):
        u=urllib.parse.urlsplit(url)
        if u.scheme!='http' or u.hostname!='127.0.0.1' or u.username or u.password:
            raise Refused('LOOPBACK_ONLY')
        frozen=self.admit(token,operation,step,arguments,endpoint=url)
        if before_send: before_send()  # test barrier after committed admission
        request=urllib.request.Request(url,data=frozen,headers={'Content-Type':'application/json'},method='POST')
        # No credentials, no environment proxies, no redirects to external hosts.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs): return None
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        with opener.open(request,timeout=5) as response:
            response.read()
            if response.status!=200: raise Refused('TARGET_NOT_ACCEPTED')
        if crash_after_200: os._exit(86)
        with self.locked() as (_,a):
            a.execute("UPDATE operations SET state='SUCCEEDED' WHERE id=?",(operation,))
            self.record(a,'observed-result',{'operation':operation,'status':200})
        return 'SUCCEEDED'

    def stop(self):
        with self.locked() as (_,a):
            a.execute('UPDATE control SET stopped=1')
            self.record(a,'stop',{'new_admission':'closed','in_flight':'may_complete'})

    def revoke(self,principal):
        with self.locked() as (_,a):
            a.execute('UPDATE grants SET active=0 WHERE principal=?',(principal,))
            self.record(a,'revoked',{'principal':principal})

    def snapshot_work(self,path):
        with self.locked() as (w,_):
            with sqlite3.connect(path) as target: w.backup(target)

    def restore_work(self,path):
        # Trusted maintenance operation, no public restore endpoint. Persistent
        # epoch and current revocations/journal MUST survive this work-only restore.
        with (self.root/'lock').open('r+') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            with sqlite3.connect(self.root/'authority.sqlite') as a:
                a.execute('UPDATE control SET epoch=epoch+1, stopped=1')
            # The hold is committed first; process death during copy cannot reopen.
            shutil.copyfile(path,self.root/'work.sqlite')

    def reopen_fixture(self):
        # Trusted test-only operator action, NOT a qualified recovery-release gate.
        # The journal and revocations continue to refuse affected work after this.
        with self.locked() as (_,a):
            a.execute('UPDATE control SET stopped=0')

    def status(self):
        with self.locked() as (_,a):
            return {'control':dict(a.execute('SELECT * FROM control').fetchone()),'operations':[dict(r) for r in a.execute('SELECT id,state,reservation FROM operations')], 'evidence_count':a.execute('SELECT COUNT(*) FROM evidence').fetchone()[0]}
