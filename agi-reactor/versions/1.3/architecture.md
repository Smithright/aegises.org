# AGI Reactor — A Safe, Governable Reference Architecture for Enterprise AGI

Author: Ryan Smithright — [Qthonic Labs](https://qthonic.com/) — ryan@smithright.com

Canonical publication: https://aegises.org/agi-reactor/

Complete article, including the safety case, coverage map and worked RFC: https://aegises.org/agi-reactor/agi-reactor.txt

Public design draft 1.3 · 14 September 2026. Planned architecture, not a deployment certification.

## Architectural judgment

The architecture should make a persistent agent's knowledge, commitments, authority and resources coherent across replaceable executions. Its defining quality is continuity with consequence: it can resume useful work without guessing what happened, exceed neither its authority nor its resource allocation, and improve without discarding its obligations.

NATS is the communication kernel. The kernel contract is larger: authenticated invocation, owned state transitions, durable commitments and recoverable operations. The host OS still isolates and schedules processes. These are deliberate responsibility boundaries, not objections to a service-oriented system.

The compressed semantic surface is **object, link, message; invoke**. This is a working design constraint, not a claim that three universal tables solve every domain. State machines, authorization, transactional storage, scheduling and reconciliation remain real implementation responsibilities. If compression hides one of these, it has failed.

## Safety scope and assumptions

Safety here means containing identified hazards within a declared operating scope: unauthorized effects, disclosure, duplicate effects, uncontrolled resource consumption and loss of human control. Each consequential service declares permitted use, action constraints, foreseeable hazards, enforcement points and validation specimens. Authorization alone does not establish that an action is appropriate. This architecture does not establish general alignment, harmlessness of every authorized action, or safety against a compromised administrative root.

Workers and generated code run without infrastructure administration credentials or unrestricted external egress. Tool access, model-provider submission and external destinations pass through scoped adapters. Authorization covers reading information and releasing it to a destination. Retrieved instructions remain untrusted content; they cannot change authority. Tenant and sensitivity constraints propagate into frames, derived artifacts, logs and indexes, with explicit retention and deletion behavior.

## Whole-system coverage

| Responsibility | Viable first implementation | Expansion trigger |
|---|---|---|
| Human purpose and control | Conversation, explicit outcome and acceptance, priority, pause/cancel, decisions and observed delivery | Multiple stakeholders need negotiated portfolio allocation |
| Identity and authority | Stable principal, scoped delegation, policy at service boundaries, revocation, tenant isolation | Additional trust domains require federation |
| Shared meaning and state | Typed objects and links, owning services, revision checks, provenance, attributed assertions | Measured query or schema needs exceed the initial relational model |
| Perception and knowledge | Adapters turn observations into attributed records; retrieval carries source, time, uncertainty and contradiction | More modalities or measured retrieval deficits |
| Cognition and learning | Bounded compositor, replaceable models, explicit hypotheses/plans, outcome evaluation, versioned lessons | Demonstrated improvement on held-out tasks warrants more automation |
| Work and coordination | Tickets with one assignee, dependencies, bounded attempts, routines, events, deadlines and cancellation | Measured throughput/fairness needs exceed simple admission |
| Effects and reconciliation | Typed invocation, durable operation identity, target-aware idempotency, outcome query and evidence | New effect domains require new adapters/contracts |
| Runtime and economics | Supervisor, bounded concurrency, admission budgets, health, usage and restart backoff | Actual capacity pressure or availability requirement |
| Evolution and recovery | Isolated candidates, staged traffic, hot fallback, compatible state, backup/restore trial | Failure-domain requirements justify replicated infrastructure |
| Human/agent orientation | World State and UI projections over the same authorized records; visible source freshness | New consumers require new projections, not new authorities |

## Semantic contract

- **Object:** stable ID, type/schema version, owning service, revision, attributed state. Ticket, agent, edict, skill, service, observation, hypothesis and context frame are domain types. A principal is an identity, not a model process. A service identity is not its current implementation instance.
- **Link:** typed relationship between object IDs, with provenance and temporal/revision scope where meaningful. `assigned-to`, `depends-on`, `supports`, `contradicts`, `governed-by`, `implements`, `supersedes`. No fixed semantic fan-out, but every traversal has access, depth, time and result limits. Not every link creates a scheduling dependency; dependency cycles must be rejected or explicitly resolved.
- **Message:** immutable attributed communication with ID, kind/schema, sender, intended recipient/scope, correlation and causation, body and references. Chat is the conversational form of IPC. Natural-language content is not executable authority. Typed commands require admission; events report committed facts. Transient presence and token streams need not be retained as durable commitments.
- **Invoke:** one envelope, typed methods. `invoke(service, method, target, arguments, operation_id, expected_revision?, frame_ref?, attempt_generation?, deadline, budget_ref)` with authenticated caller authority supplied by the transport/session. A request naming a principal does not authenticate it. Responses distinguish rejected, accepted/pending, succeeded, failed and unknown. Cancellation and status are discoverable service methods. This is illustrative notation, not a claim that those exact endpoints exist today.

Keep the domain vocabulary rich and the protocol small. Do not flatten a policy into an ordinary note or an observation into a fact merely because they share a record form.

## Concrete placement

Start with a small number of deployments: NATS + JetStream; one transactional control/state service; a compositor; agent workers; governed effect adapters; a supervisor. Identity, policy, catalog, ticket scheduling, inbox and outbox can begin as modules behind the control service's contracts. Split processes for measured load, independent release or failure containment, not for every noun in the ontology. Untrusted execution belongs outside that process.

The control/state service owns transactional object revisions, links, ticket assignment, active attempt generation and operation records. PostgreSQL is my default backing store for these atomic changes and relational queries. Reuse existing storage only where it provides this contract; changing storage is a separate implementation decision with a migration plan. Blobs, source code and large artifacts remain in suitable stores behind references. “Everything is a service” means stable mediated access; it does not require replacing physical files with individual daemons.

Use Core NATS for bounded request/reply and disposable signals. Use JetStream for recoverable dispatch and committed change propagation. Accepted work must reach durable custody before the UI reports acceptance. SQL state plus outbox event are one transaction; an outbox publisher retries using the same event identity. A consumer deduplicates into its inbox and commits the resulting state before acknowledging. Broker duplicate suppression helps, but is not the permanent application operation ledger.

The control database is authoritative for the records it owns. JetStream is the delivery/replay substrate for retained events, not a second editable ticket authority. Search, embeddings, World State and dashboards are rebuildable projections with source revisions and freshness. Do not begin with a requirement to reconstruct every object solely by replaying all history.

## Ownership is simple; concurrency is enforced

A ticket has zero or one assigned agent, one acceptance contract and a durable result/recovery record. Assignment is updated atomically against an expected revision. Begin with one active attempt per ticket. Parallel work uses linked tickets with separate assignees; it does not make one ticket multiply owned.

Assignment survives worker replacement. An execution attempt has a generation and bounded custody; renewals and reassignment use authoritative state. Workers cannot create their own valid generations. A named-agent dispatch route does not itself authorize execution. Queue groups distribute messages; they do not establish business assignment.

At the effect boundary, the service admits an operation against current authority, ticket/attempt generation and target revision. A stale worker cannot start a new operation. An already admitted operation remains durable owned work and may finish after the initiating worker dies; reassignment does not erase it. The next worker reconciles it. Cancellation is cooperative for work already committed to an external system.

At first admission, bind the operation ID to tenant, authenticated caller, method, target and canonical argument digest. Reuse with a different binding is rejected. Retries and successors recover the ID from the durable workflow step; they do not replace it while the outcome is unresolved. Adapters declare the target idempotency scope and retention window. A successor uses a separately authorized status or reconciliation method referencing the existing operation; it does not resubmit the original effect with a different caller binding. The original initiating principal remains immutable, while the reconciler identity and any custody transfer are separately attributed. Reconciliation cannot widen the admitted effect scope.

An effect gateway must make admission and operation ownership durable and serialize competing attempts for the same operation. A one-time generation check followed by unconstrained direct external calls is insufficient. Where a target supports idempotency keys, reuse the operation ID. Where it supports status lookup, reconcile. Where neither exists, a crash after sending can leave UNKNOWN; stop automatic retries and expose the uncertainty. No database transaction or NATS acknowledgment can erase that boundary.

Different tickets may target the same object: its owning service serializes or rejects conflicting revisions. Tickets are a durable coordination abstraction, not a global lock for every linked object. Multi-service workflows use explicit steps and compensating actions where available; no universal distributed transaction is required.

A durable dispatch notification can be acknowledged once the state service has accepted execution custody and a reconciler can find abandoned work. Do not use an hours-long unacknowledged broker delivery as the only ticket lifecycle. A low-cost deterministic reconciler repairs expired attempts, unpublished outbox entries and stuck operations; it does not wake a model when no reasoning is needed.

## Cognition must include more than context assembly

The compositor receives principal, ticket, permitted sources and resource limits. It resolves access before traversal, retrieves relevant material, and assembles a versioned frame manifest with source revisions and compiler version. Required continuity includes purpose, acceptance, assignee, active attempt, applicable constraints, unresolved operations and return point. Missing required material produces an explicit incomplete frame. Optional material is ranked and bounded.

A frame is a bounded view, not a copy of the entire world or a bearer capability. There is no promise of a global atomic snapshot across external services: each source reports revision/time, and consequential writes recheck their preconditions. An initial deterministic compositor is easier to inspect; model summaries can later become attributed, cached derivative objects.

Perception produces observations. Reasoning produces hypotheses, plans and proposed actions. Evaluation compares expected and observed outcomes. Consolidation proposes corrections, lessons and skill changes with provenance. Do not silently promote a model's confident summary into canonical truth. Preserve conflicting observations and invalidation links; use appropriate uncertainty representations rather than a universal invented confidence number.

Memory retrieval, procedural skills and model inference remain replaceable services. Improved behavior is promoted after representative evaluation and bounded trials. Learned policy suggestions cannot grant authority. Budgets, stop conditions and an independent supervisor bound the loop; cognition may choose to wait or ask a human instead of generating more tasks.

## Authority and human agency

Authenticate principals; bind scoped authority to service methods and resource targets. NATS subject permissions constrain transport; the service still enforces object-level policy and tenant scope. Enforce revocation at new operation admission, with explicit expiry/cache behavior. The policy service must not depend on an LLM to decide ordinary admissibility.

Changing policy, identity, resource ceilings, routing or release controls requires a distinct administrative capability and an attributable versioned change. Ordinary work cannot enlarge its own authority or disable its enforcing boundary. Emergency suspension blocks new effect admission independently of models. If a control service is unavailable, only explicitly defined safe operations remain available; cached authority has bounded expiry.

Edicts retain the original distinction between laws/standards, SOPs, guidelines and examples. Machine-enforceable requirements become versioned policies at the relevant boundary. Advisory guidance informs composition. Ambiguous prose does not become a deny rule by accident. Approval is a scoped decision object with identity, expiry and conditions when required, not a generic confirmation loop.

Human interfaces expose meaningful controls: change priorities, inspect reasons/evidence, pause, cancel future work, decide exceptions and receive a usable result. Pausing cognition, blocking new effect admission and undoing a completed external effect are distinct operations. A supervisor can stop new work even when a model or optional UI is unhealthy. Secret values stay in managed secret storage; ordinary frames contain references and only the minimum needed context.

## Resources, reliability and upgrades

Every execution is admitted against bounded concurrency and a resource allocation: model/token quota, money, CPU/GPU, memory, wall time and downstream capacity are distinct dimensions. Reserve an allowance before dispatch, account usage, cap retries and release unused capacity. Priority and fairness belong in the scheduler. Backpressure, timeout, retry delay, quarantine and load shedding must be specified; they cannot be delegated to “the agent will figure it out.”

Service identity and contract stay stable while implementation instances change. Start vNext isolated with zero ordinary traffic. Qualify with attributable live canaries. A governed router/controller allocates explicit traffic stages. Keep the old version hot and continuously checked through stabilization; stop promotion on stale/failed evidence and return traffic automatically when criteria breach. Ordinary NATS queue sharing is not that rollout controller.

Old and new versions share the authoritative operation ledger. Dispatch, reconciliation, timers and background jobs acquire custody through the same protocol. A rollout cannot grant both versions permission to send the same non-repeatable effect. Compatible continuation and operation formats are qualification requirements. If safe transfer is not established, the old instance retains the operation or it enters reconciliation; upgrades do not justify blind replay.

Stop assigning new work to an old instance, drain bounded in-flight requests, and resume long work from durable continuations. Preserve schema and message compatibility across old/new versions using expand/migrate/contract. Delay destructive cleanup until fallback is no longer required. Secret rotation, routing and policy updates are likewise versioned control-plane changes. The broker, database and host have their own maintenance procedures; avoiding a global application restart does not eliminate maintenance.

Start with one recoverable host if its outage budget permits: persistent volumes, supervised processes, real backups and a witnessed restore. This can survive worker crashes; it does not provide host availability. A multi-node NATS cluster and a highly available database are separate later decisions. Avoid a premature orchestration platform or bespoke storage engine solely to make the architecture sound complete.

Restoring older state begins with new effect admission disabled. Recovery establishes a new runtime epoch, excludes old workers, reconciles retained events and external outcomes, and restores or revalidates authority changes newer than the backup. Missing evidence blocks replay of affected effects. Dispatch resumes only after this recovery barrier is satisfied. The selected workload must define recovery-point and recovery-time objectives before qualification.

## Prove one complete system before widening it

Use a small representative service change requested through chat, with acceptance that a human can verify. Include one relevant knowledge correction and one pause/resume so cognition and human control are tested alongside transport.

1. Receive the request; persist acceptance and link source intent. Lose the acceptance reply and recover the same ticket by operation identity.
2. Admit a budget, assign one agent and race two workers. Exactly one current attempt may admit new effects. A resumed stale worker is refused.
3. Compose bounded context, preserving a contradictory source and a pending operation. Denied material cannot enter the frame. Demonstrate useful planning, not merely valid JSON.
4. Execute a reversible representative effect; redeliver its command and kill the worker after the target accepts but before reply persistence. Reconcile the same operation; never create a replacement solely because its reply was lost.
5. Pause new work and exhaust a small test budget. Neither condition should depend on the model politely stopping; the service boundary refuses further admission. Already admitted work remains visible.
6. Upgrade the effect service through isolated candidate, canary and a small traffic stage while the old instance remains hot. Inject a failed/stale canary and demonstrate rollback. Preserve the ticket and operation identities across versions.
7. Deliver a result the recipient can use; record their acceptance and update the derived World State. Consolidate a source-linked lesson; compare a follow-up task against baseline before promoting a new skill.
8. Restore durable state from backup in an isolated environment and recover unresolved commitments. Check object revisions, operation status and replay boundaries together, not just that the process boots.

Measure completion quality, latency, total cost, recovery time, duplicate effects, stale-worker refusals and usability of the result. Set numerical SLOs from the chosen workload before implementation qualification. These are planned acceptance specimens, not reported test results.

## Design judgment / explicit decisions

- Persist obligations and evidence; make model executions replaceable.
- Prefer rich domain meaning over many protocols or transport-specific nouns.
- Put enforcement beneath simple interactions. A user assigns one agent; the runtime handles attempts and failures.
- Spend cognition on ambiguity and invention; use deterministic code for routine coordination.
- Treat uncertainty as state that can be resolved, not prose that gets forgotten.
- Build service contracts first, with few deployments. Separate implementations when evidence justifies it.
- Pay for redundancy and abstraction when a named consumer needs them.
- Evaluate learning and usefulness as seriously as delivery and authorization.
- Make continuing, stopping and recovering understandable to both human and agent.


Primary transport reference: https://docs.nats.io/learn/jetstream/acknowledgment


## Executable reference specimen

[RFC-001: accepted effect, worker death and an UNKNOWN backup](https://aegises.org/agi-reactor/conformance/RFC-001.md) specifies the worked failure case, operator contract and executable falsification test. The reference guard uses local HTTP and SQLite; it does not qualify the production NATS/PostgreSQL runtime.
