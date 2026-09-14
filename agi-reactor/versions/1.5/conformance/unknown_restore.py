"""RFC-001 reference fault harness: real HTTP, process death and SQLite backup.
No NATS, PostgreSQL, production credentials or external network destinations.
Neither this reference guard nor its storage substitutes for the real reactor.
"""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import urllib.request

INTENT = {'tenant': 'specimen', 'caller': 'agent-a', 'method': 'append',
          'target': 'local-receipt-ledger', 'arguments': {'receipt': 'R-001'}}
OP = 'operation-001'

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                          separators=(',', ':')).encode()).hexdigest()

def db(path):
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    return c

class Refused(Exception):
    pass

class ReferenceGuard:
    """Single-process admission reference, not a concurrent/cryptographic PEP."""
    def __init__(self, root):
        self.path = root/'control.sqlite'
        self.epoch_path = root/'recovery.json'

    def boundary(self):
        return json.loads(self.epoch_path.read_text())

    def execute(self, url, epoch, operation=OP, intent=INTENT, die_after_200=False):
        with db(self.path) as c:
            op = c.execute('SELECT * FROM operations WHERE step=?', ('ticket-001/step-1',)).fetchone()
            # Inspect the immutable binding before sending anything.
            if op and op['digest'] != digest(intent):
                raise Refused('INTENT_MISMATCH')
            boundary = self.boundary()
            if epoch != boundary['epoch']:
                raise Refused('STALE_EPOCH')
            if boundary['hold']:
                raise Refused('RECOVERY_HOLD')
            if op['id'] != operation:
                raise Refused('STEP_ALREADY_HAS_OPERATION')
            if op['state'] == 'UNKNOWN':
                raise Refused('OUTCOME_UNKNOWN')
            if op['state'] != 'ADMITTED':
                raise Refused('NOT_DISPATCHABLE')
            # Conservative send-intent: UNKNOWN must commit before the send.
            c.execute('UPDATE operations SET state=? WHERE id=?', ('UNKNOWN', operation))
            c.commit()
        req = urllib.request.Request(url, data=json.dumps(intent['arguments']).encode(),
                                     headers={'Content-Type':'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            response.read()
            if response.status != 200:
                raise RuntimeError('target did not acknowledge acceptance')
        if die_after_200:
            os._exit(86)  # Actual worker termination; no result commit or cleanup.
        with db(self.path) as c:
            c.execute('UPDATE operations SET state=? WHERE id=?', ('SUCCEEDED', operation))
        return 'SUCCEEDED'

    def restore(self, backup, unsafe=False):
        # Deliberately outside the restored DB: recovery epoch/admission authority.
        old = self.boundary()
        self.epoch_path.write_text(json.dumps({'epoch':old['epoch']+1, 'hold':True}))
        shutil.copyfile(backup, self.path)
        with db(self.path) as c:
            c.execute('UPDATE tickets SET state=?', ('NEEDS_RECONCILIATION',))
        if unsafe:
            # Negative control: common destructive recovery shortcut.
            with db(self.path) as c:
                c.execute("UPDATE operations SET state='ADMITTED' WHERE state='UNKNOWN'")
            self.epoch_path.write_text(json.dumps({'epoch':old['epoch']+1, 'hold':False}))

def initialize(root):
    root.mkdir(parents=True, exist_ok=True)
    # Refuse to overwrite any prior run's custody or evidence.
    if any(root.iterdir()):
        raise RuntimeError('root must be an empty, disposable directory')
    with db(root/'control.sqlite') as c:
        c.execute('CREATE TABLE tickets(id TEXT PRIMARY KEY, assignee TEXT, state TEXT)')
        c.execute('INSERT INTO tickets VALUES(?,?,?)', ('ticket-001','agent-a','RUNNING'))
        c.execute('CREATE TABLE operations(id TEXT PRIMARY KEY, step TEXT UNIQUE, digest TEXT, state TEXT)')
        c.execute('INSERT INTO operations VALUES(?,?,?,?)', (OP,'ticket-001/step-1',digest(INTENT),'ADMITTED'))
    (root/'recovery.json').write_text(json.dumps({'epoch':1,'hold':False}))
    with db(root/'target.sqlite') as c:
        c.execute('CREATE TABLE effects(sequence INTEGER PRIMARY KEY AUTOINCREMENT, body TEXT)')


def scenario(root, mode):
    initialize(root)
    target_path = root/'target.sqlite'
    class Target(BaseHTTPRequestHandler):
        # No GET/status route and no idempotency handling. Each POST is a new effect.
        def do_POST(self):
            body = self.rfile.read(int(self.headers['Content-Length'])).decode()
            with db(target_path) as c:
                c.execute('INSERT INTO effects(body) VALUES(?)',(body,))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"accepted":true}')
        def log_message(self, *_):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Target)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = 'http://127.0.0.1:%d/effect' % server.server_address[1]
    guard = ReferenceGuard(root)
    def count():
        # Test oracle only: ReferenceGuard never receives this function or path.
        with db(target_path) as c:
            return c.execute('SELECT COUNT(*) FROM effects').fetchone()[0]
    def attempt(**kwargs):
        try:
            return guard.execute(url, **kwargs)
        except Refused as exc:
            return str(exc)
    try:
        worker = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                 '--worker', '--root', str(root), '--url', url],
                                timeout=10, capture_output=True)
        if worker.returncode != 86:
            raise RuntimeError('unexpected worker exit: '+worker.stderr.decode())
        with db(root/'control.sqlite') as c:
            snapshot_state = c.execute('SELECT state FROM operations').fetchone()[0]
            with db(root/'unknown-backup.sqlite') as b:
                c.backup(b)
        before = count()
        unknown_before_restore = attempt(epoch=1)
        guard.restore(root/'unknown-backup.sqlite', mode=='unsafe-reset-on-restore')
        old_worker = attempt(epoch=1)
        changed = dict(INTENT, arguments={'receipt':'different-intent'})
        changed_arguments = attempt(epoch=2, intent=changed)
        replacement = attempt(epoch=2, operation='replacement-operation')
        same = attempt(epoch=2)
        # Test-only probe: remove the global hold, retaining the operation state.
        # This does not implement or qualify the production barrier-release policy.
        boundary = guard.boundary()
        guard.epoch_path.write_text(json.dumps(dict(boundary, hold=False)))
        same_without_global_hold = attempt(epoch=2)
        replacement_without_global_hold = attempt(epoch=2, operation='replacement-operation')
        with db(root/'control.sqlite') as c:
            state = c.execute('SELECT state FROM operations').fetchone()[0]
            ticket = c.execute('SELECT state FROM tickets').fetchone()[0]
        return {'specimen':'RFC-001','implementation':'isolated-reference-guard',
                'mode':mode, 'worker_exit':worker.returncode,
                'target_effects_before_restore':before, 'snapshot_state':snapshot_state,
                'before_restore_retry':unknown_before_restore,
                'current_epoch':guard.boundary()['epoch'], 'old_worker':old_worker,
                'changed_arguments':changed_arguments,'replacement_operation':replacement,
                'same_operation':same,
                'same_without_global_hold':same_without_global_hold,
                'replacement_without_global_hold':replacement_without_global_hold,
                'operation_state':state,'ticket_state':ticket,
                'target_effect_count':count(),
                'duplicate_effect_count':max(0,count()-1),
                'scope':'real loopback HTTP and process exit; SQLite reference model; no production qualification'}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--mode', choices=['guarded','unsafe-reset-on-restore'], default='guarded')
    p.add_argument('--worker', action='store_true')
    p.add_argument('--url')
    p.add_argument('--assert-safe', action='store_true')
    args = p.parse_args()
    if args.worker:
        if not args.url.startswith('http://127.0.0.1:'):
            raise RuntimeError('specimen only permits loopback HTTP')
        ReferenceGuard(args.root).execute(args.url,epoch=1,die_after_200=True)
    else:
        if args.root:
            result = scenario(args.root,args.mode)
        else:
            with tempfile.TemporaryDirectory(prefix='reactor-rfc001-') as temp:
                result = scenario(Path(temp),args.mode)
        print(json.dumps(result,indent=2))
        if args.assert_safe and result['target_effect_count'] != 1:
            print('FAIL: duplicate external effect after UNKNOWN restore',file=sys.stderr)
            sys.exit(1)
