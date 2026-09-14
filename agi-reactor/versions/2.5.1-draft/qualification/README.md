# Reactor local contract demonstrator 0.1

This executable example composes selected Qthonic lease/fencing decision functions with a **new local test implementation** of serialized custody, effect admission, a reservation ledger and recovery guards. It is not a runnable extraction of the deployed Qthonic stack. See `provenance.json` for exact source revision, selected functions and hashes.

Use Python 3.9 or later on macOS/Linux. No third-party packages, credentials, paid models or external services are required. Tests create disposable SQLite stores and a loopback HTTP server. All runtime state is temporary. The report is the only retained output.

```sh
python3 run.py --output my-result.json
```

The runner executes 14 tests, then deliberately disables the fence and replay guard in disposable source copies. Those two mutated tests must fail for the expected reason. It also records 100 admission timing samples after 20 warmups. `result.json` records the author's observed run, environment and exact source hashes. Re-run it; do not treat it as an attestation.

## What the example does

- Two worker processes race for one ticket. One claim succeeds.
- An expired worker presents an old generation. The reused Qthonic fence decision refuses it.
- A poisoned-source proposal redirects a report outside a separately configured recipient grant. Admission refuses it; the allowed recipient succeeds.
- A misleading report to the allowed recipient succeeds. This is an observed semantic limitation, not a passed semantic safety defense.
- Two agents on distinct tickets contend for a shared one-effect budget. A serialized reservation admits one.
- A worker dies with exit 86 after a non-idempotent HTTP target accepts. The target has one effect; the operation stays UNKNOWN. Neither replay nor a replacement ID for the same work step is admitted.
- A worker pauses after admission. A successor cannot redispatch the same step. Stop closes new admission, but an already admitted effect may complete afterward.
- A work backup predating both an effect and a revocation is restored. The recovery hold is installed first. Old epochs, revoked principals and unresolved operations are refused even after the test-only global hold is lifted. Unrelated work still succeeds.

## Authority and stores

`work.sqlite` owns tickets and leases. `authority.sqlite` owns current epoch, grants/revocations, operation identities, reservations and evidence. A trusted file lock serializes all entry points. The latter store is deliberately outside the restored work snapshot. This is a limited recovery profile, not a demonstration that a complete rollback of all authoritative state can be recovered safely.

The target's independent append ledger is available only to the test oracle. The effect adapter receives no status or deduplication API. The test can count effects that the recovering worker cannot know occurred.

The caller name, declared data classification and maintenance actions are fixture inputs. Endpoint routing and allowed work-step IDs are provisioned by trusted fixture setup; workers cannot substitute them. Semantically duplicate tickets created by an authorized work-admission service are outside this test. Admitted payload bytes are frozen before dispatch, and the target receives those exact bytes. Authentication, mandatory OS containment, trusted content classification, Cedar policy evaluation, network partitions, crash consistency across multiple hosts, power loss and production scale are not qualified. A worker with direct database or target access can bypass this local example. It is a contract laboratory, not a secure deployment.

The budget is a single lifetime effect-count limit for this disposable tenant. UNKNOWN reservations remain charged. Windows, monetary units, atomic multi-scope limits, refunds, authoritative reconciliation and qualified recovery release are not implemented. The test-only `reopen_fixture` function is not an operator recovery API.

No unrestricted recursive self-improvement or legal compliance claim follows from this example. The site's implementation-experience statement is attributed to Qthonic's author; this suite contains no model calls.

## Provenance and license

The extracted functions retain their original text; imports and a default TTL constant are supplied locally. Every claim test passes an explicit TTL. The functions make decisions on caller-supplied rows. The new local lock/database wrapper is what serializes the fixture; this does not prove the production writer is atomic.

Published as part of the AEGISES repository under its MIT license. This is a new qualification artifact. Earlier withdrawn experiments are not republished.
