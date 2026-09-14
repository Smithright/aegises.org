# AGI Reactor — A Safe, Governable Reference Architecture for Enterprise AGI

Author: Ryan Smithright — [Qthonic Labs](https://qthonic.com/) — ryan@smithright.com

Canonical publication: https://aegises.org/agi-reactor/

Complete article, including the safety case, coverage map and worked RFC: https://aegises.org/agi-reactor/agi-reactor.txt

Public design draft 1.7 · 14 September 2026. Planned architecture, not a deployment certification.

## Architectural judgment

The architecture should make a persistent agent's knowledge, commitments, authority and resources coherent across replaceable executions. Its defining quality is continuity with consequence: it can resume useful work without guessing what happened, exceed neither its authority nor its resource allocation, and improve without discarding its obligations.

Message transport supplies the communication kernel; NATS is the reference implementation. The kernel contract also includes: authenticated invocation, owned state transitions, durable commitments and recoverable operations. The host OS still isolates and schedules processes. These are deliberate responsibility boundaries, not objections to a service-oriented system.

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


02 Security foundations

Established foundation · architectural application

## A reference monitor’s safety is as strong as its policies.

Enforcement makes a rule binding. Policy determines what that rule permits. A credible safety case must examine both.

James P. Anderson’s Computer Security Technology Planning Study (1972) describes a reference monitor that mediates authorized access between subjects and objects. Its implementation—the reference validation mechanism—must resist tampering, be invoked for every protected reference, and be sufficiently small for comprehensive analysis and testing. These are requirements for a trustworthy enforcement mechanism. [1] (https://aegises.org/agi-reactor/#ref-anderson)

The section title states a necessary limit, not a sufficient condition for safety. A monitor that correctly enforces an overbroad permission will correctly permit the resulting access. Conversely, adequate policy provides no protection along an unmediated path. The safety argument therefore depends on the adequacy of the rules, the integrity of the facts used to evaluate them, and the fidelity of enforcement within a declared threat model.

Saltzer and Schroeder’s principles of fail-safe defaults, complete mediation and least privilege sharpen the design obligation: permission should be explicit, access must be checked, and authority should be limited to what the task requires. [2] (https://aegises.org/agi-reactor/#ref-saltzer-schroeder) AGI Reactor applies this discipline to service invocation, information disclosure, resource allocation and changes to the controls themselves.

Three distinct claims in the Reactor safety argument

 | Claim | Required evidence | Failure to challenge
 | Policy adequacy | Trace identified hazards to explicit constraints, exceptions and accountable decisions. | An authorized report submission discloses information to an inappropriate recipient.
 | Decision integrity | Bind authenticated identity, current authority, object revision and policy version to the actual request. | A stale classification or forged attribute turns a prohibited disclosure into an apparent permission.
 | Enforcement fidelity | Exercise every effect path, including adapters, retries, administrative changes and recovery. | A denied operation reaches the target through an alternate credential or a replay.

### Policy must govern its own change.

In this reference design, policies are versioned artifacts with an identified issuer, scope, rationale, tests and activation authority. A proposal becomes active only through an authorized transition. Privilege expansion requires distinct authoring and approval roles. Revocation, emergency suspension and recovery have explicit effect on new admission; already accepted operations retain an accountable reconciliation path.

Model-generated guidance can propose a rule or supply evidence for review. It cannot alter its own grants by entering a context frame. The service boundary evaluates trusted request facts and enforces the applicable policy, budget, revision and operation-custody checks. The policy-enforcement diagram (https://aegises.org/agi-reactor/#authority) specifies that path; the safety case (https://aegises.org/agi-reactor/#safety) identifies the corresponding challenges.

The resulting research obligation is twofold: demonstrate that the system enforces its stated policy, and justify why that policy addresses the hazards claimed. Neither demonstration substitutes for the other.

03 International governance

Institutional proposal · open to public examination

## A formal public ontology is an international governance surface for AGI.

A formal public ontology, governable by the Internet Society, gives institutions a common language in which to specify, contest and test the boundaries of AGI systems.

The proposal is a public semantic contract: stable identifiers and formally specified relationships for principals, actions, resources, authority, obligations and evidence. It makes the objects of governance inspectable across vendors and jurisdictions. W3C’s OWL 2 provides an established basis for ontologies with formally defined meaning, including classes, properties and individuals. [3] (https://aegises.org/agi-reactor/#ref-owl) A vocabulary alone does not grant authority or execute a policy; implementations must bind those meanings to enforceable service contracts.

### Internet Society stewardship: a proposed mandate.

We propose that the Internet Society consider convening and stewarding this work under an explicit, publicly reviewed charter. Its documented approach emphasizes community consultation and technically grounded policy advocacy; it describes itself as an advocate rather than a policy-making body. [4] (https://aegises.org/agi-reactor/#ref-isoc-process) Its multistakeholder framework emphasizes inclusion, transparency, shared responsibility and distributed governance. [5] (https://aegises.org/agi-reactor/#ref-isoc-governance) These provide an institutional starting point. Stewardship of an AGI ontology would require a new mandate accepted by the Society and participating stakeholders; no endorsement or commitment is asserted here.

The charter should give affected communities, civil society, technical implementers, researchers, enterprises and public authorities meaningful participation. It should specify how proposals are admitted, reviewed and decided; how conflicts of interest and funding are disclosed; and how objections, appeals and minority positions remain on the public record. Representation and resources to participate are governance requirements, not consequences of publishing a repository.

Proposed distribution of responsibility

 | Layer | Public artifact | Accountable decision
 | Common ontology | Identifiers, definitions, relationships, version history and compatibility rules. | A chartered stewardship process approves changes to shared meanings.
 | Policy profiles | Named rules, intended scope, hazard rationale, exceptions and conformance cases. | The identified jurisdiction, sector or adopting institution authorizes its profile.
 | Operational adoption | Declared ontology/profile versions, service mappings and scoped assurance evidence. | The operator admits an exact release and remains responsible for enforcement.

A shared core should support explicit jurisdictional and sectoral extensions. Conflicting requirements must be identified and resolved through a declared authority and conflict procedure; a semantic merge cannot settle a normative disagreement. Stewardship of definitions would confer no universal grant over deployments. Publication of a new ontology or policy profile would not automatically activate it in a running system.

### Make public commitments mechanically testable.

An adoption record should identify the ontology version, applicable profile, issuer, authority, effective interval and implementation mapping. A protected invocation should retain those references with its policy decision and outcome. Changes to a term’s meaning must be reviewed as potentially security-relevant changes: expanding a resource class can expand a grant without changing the policy’s text.

The first useful milestone is deliberately bounded: publish a minimal vocabulary and one disclosure-policy profile; implement it independently in two service stacks; then run shared cases for permitted disclosure, denial, conflicting scope, revocation and stale evidence. Agreement on an intended answer is a testable interoperability claim. An inconclusive safety result must remain inconclusive in the public record. Public schemas and aggregate conformance evidence can be inspected while sensitive operational records remain access-controlled.

The governance surface connects public reasons to typed rules, typed rules to local adoption, and adoption to inspectable enforcement. Its legitimacy rests on accountable institutions; its technical value rests on demonstrable conformance.


### Foundational references

1. James P. Anderson. Computer Security Technology Planning Study, Volume I. ESD-TR-73-51, October 1972, §§3.2.1–3.2.2, pp. 8–10; §3.7, p. 13. Electronic Systems Division, AFSC. Original report, NIST archive. https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/ande72a.pdf#page=16
2. Jerome H. Saltzer and Michael D. Schroeder. “The Protection of Information in Computer Systems.” Proceedings of the IEEE 63(9), 1975, pp. 1278–1308, §I.A.3. Author-hosted text. https://web.mit.edu/saltzer/www/publications/protection/Basic.html
3. W3C OWL Working Group. OWL 2 Web Ontology Language: Document Overview, Second Edition. W3C Recommendation, 11 December 2012, §§2.1–2.3. https://www.w3.org/TR/2012/REC-owl2-overview-20121211/
4. Internet Society. Policy Development Process at the Internet Society. 25 May 2018; updated September 2025. “Policy Development Approach” and “Consultation approach.” Accessed 14 September 2026. https://www.internetsociety.org/about-internet-society/policy-development-process/
5. Internet Society. Internet Governance: Why the Multistakeholder Approach Works. 26 April 2016. Executive summary and attributes of successful decision-making. Accessed 14 September 2026. https://www.internetsociety.org/resources/doc/2016/internet-governance-why-the-multistakeholder-approach-works/

Versioned publication: https://aegises.org/agi-reactor/versions/1.7/
Citation records: https://aegises.org/agi-reactor/citation.bib

## Policy-governed service orchestration is all you need

The composition thesis is that reasoning, memory, work, policy, learning, release and recovery are services. Their governed contracts also change the system itself. Durable state, explicit authority and recoverable effects are part of those contracts.

V4 diagrams: [the machine](https://aegises.org/agi-reactor/assets/v4-d1.svg), [objects and bindings](https://aegises.org/agi-reactor/assets/v4-d2.svg), [policy enforcement](https://aegises.org/agi-reactor/assets/v4-d3.svg), [operation timeline](https://aegises.org/agi-reactor/assets/v4-d4.svg). The full text edition contains their labels and explanations.


## Credits

### Internet Society, IETF, W3C, MANRS

Root Stewardship, International Security, & Standards Foundations

### Academia & Sciences

Computer Science, Computational Linguistics, Compute Primitives, Encodings, Compiler Engineering, Ontology Engineering, Type Theory, Calculus, Data Science, Information Theory, Language Models, Public Benchmarks, Microkernels, OS Engineering, Network Engineering, Network Protocols, Encryption, IPC, IO, API Engineering, Control Theory, Data Engineering, Model Routing, Enterprise Software Architecture, Middleware Architecture, Internet Exchange Architecture, Computational Neuroscience, Cognitive Science, Artificial Life, Ethics, Philosophy

### Peter Singer, AI Safety Community, & Effective Altruism

Ethical Rigor, Moral Courage, Inspiration

### The Open Source Community, Libraries, Public Educators, & other Free Education Sources

Giants and Legends ALL!

### Assembly, Compiler, C, C++, Rust, Forth, POSIX, Unix, Python, & Language Communities

Giants and legends ALL!

### Andrew Tanenbaum & Minix

OS Force, Inspiration, Rigor

### Linus Torvalds & Linux Foundation

Kernel Force, Git Force, Foundations

### Cloud Native Compute Foundation

Stewardship, Foundations

### Ben Goertzel

AGI Foundations, Inspiration

### Google

Foundations, Kubernetes Force, Thought Leadership, Standards Force, Equanimity

### Anthropic

Moral Courage, Thought Leadership, & Code Force

### OpenAI

Code Force, Thought Leadership, Moral Courage

### Chris Lattner

Inspiration, MLIR Force, Foundations

### Stanford University

Computational Linguistics Thought Leadership

### ETH Zurich

Inspiration, Systems Architecture Force, FPGA Force!

### James Anderson

Inspiration, Reference Monitor Foundations

### Ludwig Wittgenstein

Language Game Theory

### Gottfried Leibnitz

Characteristica Universalis, Calculus, Inspiration

### Steve Jobs & Apple

Mac Force, Design Inspiration, Posthumous Review

### Elon Musk & Grok

Foundations, News & Research Force, Veracity Balancing

### Jensen Huang & NVIDIA

Compute Force, Foundations

### Andrej Karpathy, Ilya Sutskever, John Carmack

Inspiration, Foundations

### DeepSeek

Open Source Foundations, Thought Leadership

### Synadia & NATS

Inspiration, Foundations

### Proton.me, Signal Foundation

Moral Courage, Security Foundations

### Family, Friends, & Communities

Invaluable!

### Kevin Carl Smith

Moral Courage, Foundations, Support

### Daniel Faggella & Emerj

Potestas, Persistence, & Flame, Adversarial Agency

### Clark Becker

Support & Friendship

### Jeff Buhrt

Mentorship, Inspiration

### Personal Foundations

Accenture, MuleSoft, SalesForce, Purdue University, Springboard

### Other Industry, Academic, & Thought Leadership Foundations

Alan Turing, Bell Labs, Microsoft, Oracle, IBM, Meta, Huggingface, OpenHands, Adobe, McKinsey

### Mythos & Inspiration

Isaac Aasimov, Ray Kurzweil, The Wachowskis, James Cameron, The Primeagen, Cormac McCarthy, Jorge Luis Borges

### The World's Fair & Olympics

Inspiration, Sportsmanship, Moral Courage, Diplomacy

### USA

Foundations, Tubes, Silicon Valley

### China

Foundations, Make Force

### EU

Foundations, Legislation Force

### Nova Mente

Inspiration, Partnership, Mythos

### Chief & Jupiter

Beast Force, Inspiration

and so many more giants and trim tabs...


## Implementation reference

| Role | Reference implementation | Required contract | Evidence status |
| --- | --- | --- | --- |
| Communication kernel | [Core NATS](https://docs.nats.io/learn/core-nats/) | Bounded request/reply and transient signals. Authenticate transport peers; enforce object and tenant authority in the owning service. An unanswered call does not prove that no effect occurred. | Reference choice. Core delivery is at-most-once. Production version, configuration and failure tests remain to be qualified. |
| Recoverable delivery | [NATS JetStream](https://docs.nats.io/concepts/jetstream) | Persist accepted work in authoritative state with an outbox. Publish with stable event identity; consumers commit deduplication and state before acknowledgment. Delivery does not assign a ticket. | Reference choice. Acknowledgment and redelivery behavior is documented. Application custody and replay safety require separate tests. |
| Authoritative state | [PostgreSQL + control/state service](https://www.postgresql.org/docs/18/transaction-iso.html) | Atomic record revisions, one assignee, one current attempt and an immutable operation binding. State changes and outbox commit together. Choose isolation, constraints and locking for each transition; handle transaction conflicts explicitly. | Reference choice. Database transactions support the design. They do not implement ticket semantics or external-effect reconciliation by themselves. |
| Authorization decision | [Cedar + service enforcement](https://docs.cedarpolicy.com/auth/authorization.html) | Validate policy against its schema; evaluate trusted request facts against an identified policy version. Refuse admission on evaluation errors, unavailable required facts or an invalid authority frame. The service also checks budget, revision and operation custody. | Proposed selection. Cedar uses default-deny, forbid-overrides-permit and skip-on-error. The proposed Reactor integration must inspect error diagnostics and enforce its stricter refusal contract. |
| Public semantic contract | [W3C OWL 2 + explicit policy profiles](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) | Publish stable identifiers, meanings, version history and reviewed mappings into executable policy schemas. Define how missing or conflicting information affects admission. An ontology inference never grants authority by itself. | Proposed standard basis. OWL 2 is specified. The AGI ontology, institutional charter and cross-implementation conformance suite remain proposed. |
| Context composition | [Compositor service contract](https://aegises.org/agi-reactor/#cognition) | Assemble permitted, source-attributed context with current obligations, acceptance, constraints, contradictions and pending effects. Preserve required continuity or explicitly refuse an incomplete frame. | Integration required. The contract is specified here. No qualified compositor package or end-to-end recovery result is supplied by this publication. |
| Execution containment | [Host supervisor + isolated workers](https://aegises.org/agi-reactor/#runtime) | Restrict credentials and egress, bound resources and enforce suspension below the model. Verify that generated code cannot reach an alternate effect path. Declare the host and isolation assumptions. | Runtime selection open. A named host, isolation configuration and adversarial containment results are required before deployment qualification. |
| Resource admission | [Control/state service module](https://aegises.org/agi-reactor/#work) | Reserve allowances and current custody atomically before admitting work. Account for in-flight operations, deadlines, capacity and consumption; retain stop control under overload. | Integration required. A module in the initial control service, not a new daemon. Budget exhaustion and concurrent-admission cases remain to be witnessed. |
| Effect recovery specimen | [RFC-001: Python / HTTP / SQLite](https://github.com/Smithright/aegises.org/tree/17b1cf33dd556d37760b7c2e95f49cd692b91acc/agi-reactor/conformance) | Keep one operation identity across worker death and restore. Preserve UNKNOWN; refuse both unsafe replay and replacement operations. Distinguish target reality from the recovering controller’s knowledge. | Bounded test recorded. The published guarded trace records one effect and zero duplicates; the negative control duplicates the effect. This is a local specimen, not production qualification. |
| Service evolution | [Governed rollout controller contract](https://aegises.org/agi-reactor/#runtime) | Isolate a candidate with zero ordinary traffic, qualify live canaries, allocate explicit traffic stages and retain a checked hot fallback. Preserve compatible state and unresolved operation custody. | Integration required. No qualified controller is supplied here. Ordinary queue sharing or a process restart does not establish the rollout contract. |

No qualified production bill of materials is supplied. Pin versions, configuration and policy hashes, schema revisions, environment and test evidence before qualifying a deployment. Replacement must preserve authority, state, concurrency, delivery and recovery contracts, including pending operations and fallback.


## Definitions

**Object** — A service-owned entity with a stable ID, tenant scope, type, revision and attributed state. A file or database row is a storage representation of an object.

**Principal / agent** — A principal is an authenticated identity. An agent is a persistent accountable identity with linked work and context; a worker process or model invocation executes on its behalf.

**Service / method** — A service owns resources and exposes typed methods. A method defines inputs, outputs, errors, authority and recovery. Service identity survives implementation replacement.

**Message / chat** — Attributed communication between people and services. Chat is an IPC surface. A message may yield several tickets or edicts; receipt alone does not establish acceptance of work.

**Ticket** — A durable obligation: intended outcome, acceptance criteria, state, zero or one assigned agent, and a result or explicit unresolved condition. Linked tickets express decomposition and dependencies.

**Attempt** — One execution generation of a ticket, with bounded custody and a return point. A ticket may have many historical attempts and at most one current attempt.

**Operation** — A durable invocation identity bound to tenant, original caller, method, target and canonical argument digest. Custody may change; accepted intent cannot.

**Edict / policy** — An edict is attributed, versioned direction. It may produce guidance, acceptance conditions or an authorization policy. Only its authorized promotion and activation make a policy enforceable.

**Link / binding** — A link is a typed, attributed relationship between objects. A binding is a link with operational applicability, such as a policy version applied to a typed scope. A link never creates authority by itself.

**Skill / template / example** — A skill is a versioned procedure assembled from guidance, templates and examples. It informs execution; it does not grant permission. These are content profiles, not separate kernel mechanisms.

**Compositor / context frame** — The compositor resolves permitted sources into bounded working context with a source manifest, obligations, constraints, uncertainty and pending effects. A frame informs reasoning and confers no capability.

**Evidence / projection** — Evidence is an attributed observation or receipt with a declared scope. A projection is a derived view, index or summary of source records. Neither an inference nor a projection silently replaces its source.

**Reaction / routine** — A reaction binds a typed event to a governed method under explicit conditions; a routine adds a schedule. Both use normal admission, work and operation contracts.

**Aegis / reference monitor** — An aegis is this design’s protected action boundary: identity, applicable policy, scoped authority and operation accountability. Its reference-monitor role must mediate access, resist bypass and be analyzable; the host and implementation must establish those properties.

## Object model

| Record | Semantic fields | Invariants |
| --- | --- | --- |
| Common object envelope | id, tenant_id, type_id, schema_version, owner_service_id, revision, provenance | Stable identity; owner controls writes. Tenant and ownership changes require explicit governed migration. |
| Typed link / binding | id, relation_type, source_id, target_id, scope, revision, provenance | 0..many per object; endpoint types and relation-specific cardinalities are validated. Protected links are written only through their owning method. |
| Principal / agent | principal_id, identity_issuer, tenant_scope, status, profile_refs | The authenticated identity is distinct from a worker instance. Assignee, caller and reconciler remain separately attributable. |
| Grant / resource allowance | principal_ref, scope, issuer, effective_interval, revision; allowance: dimensions, reserved, consumed | Grants require an authorized issuer and revocation checks. Admission reserves bounded resources atomically; concurrent reservations cannot exceed the allowance. |
| Service / method | service_id, method_id, contract_version, input_schema, output_schema, errors, recovery | A method binds a stable service role to its current implementation. Discovery does not grant invocation permission. |
| Message | sender_principal, conversation_id, content_ref, sent_at, correlation_id | 0..many source links to derived edicts and tickets. A transport envelope is not evidence that an obligation was accepted. |
| Ticket | outcome, acceptance, status, assignee_id?, result_refs, return_point | 0..1 assignee; 0..many attempts and dependency links. Accepted work is committed before acknowledgment. |
| Attempt | ticket_id, agent_id, generation, custody_expiry, recovery_epoch, status | Exactly 1 ticket per attempt; at most 1 current attempt per ticket. Current custody is checked at effect admission. |
| Operation | ticket_id, logical_step, original_caller, method, target, argument_digest, outcome, custodian | Each record binds one immutable intent. Multiple operations per ticket are allowed; replay and replacement cannot bypass an unresolved logical step. |
| Edict / policy revision | source_refs, version, applicability; policy: rules, schema_ref, approval_refs, activation | 0..many derivation and scope bindings. Authoring, approval and activation remain attributable transitions; an edict is not automatically active policy. |
| Type / skill / service definition | stable_id, version, schema_or_contract, source_refs, lifecycle | Instances cite a definition version. Upgrading a definition must preserve existing instance interpretation or provide an explicit migration. |
| Context frame / evidence | source_ids_and_revisions, observed_at, scope, transformation; frame: compiler_version, required_context | 0..many inputs; provenance survives derivation. A receipt, hypothesis and verified result retain distinct evidence kinds. |

## Information architecture

| Layer | Contents | Contract |
| --- | --- | --- |
| Authority | Resource records, tickets, policy versions, grants, operations | The owning service is the write authority. Reads and mutations use its contract; the control/state service can host several owners as modules. |
| Discovery | Catalog, graph lookup, search, embeddings, World State | Locate permitted objects by identity, type and relationship. Show source revision, observed time and coverage; rebuild projections from authoritative records. |
| Composition | Context manifest, required continuity, optional retrieved material | Resolve access before serialization. Preserve obligations, current attempt, pending operations, contradictions and return point. Missing required context is explicit. |
| Presentation | Chat, object detail, diagrams, dashboards and agent frames | Render the same semantic records for each permitted consumer. A navigation category, frame or UI label does not become a separate source of truth. |
| Evidence and learning | Receipts, observations, comparisons, corrections, proposed skills | Link result to operation, ticket, input revisions and evaluation. Preserve contradiction and supersession; promote reusable changes through their owning workflow. |
| Lifecycle | Sensitivity, retention, revocation, deletion and archival | Carry source restrictions into derived material. Invalidate affected caches and indexes; handle expired frames and retained audit obligations under an explicit policy. |

## Ontology primitives

| Primitive | Meaning | Expression |
| --- | --- | --- |
| Identity | A stable referent inside an explicit scope | Object IDs and principal IDs; identity does not depend on a current process or display label. |
| Type | Versioned meaning and admissible structure | Ticket, Agent, Service, Edict, Skill, Observation and Operation are domain profiles. Type definitions are themselves objects. |
| Relation | Typed endpoints, direction, cardinality and provenance | assignedTo: Ticket → Agent [0..1]; dependsOn: Ticket → Ticket [0..many]; derivedFrom: Object → Object [0..many]. |
| Method | A governed request with a typed contract | ticket.assign or report.send: input, output, error, authority and recovery semantics. Invocation is a message envelope; a durable effect has an Operation record. |
| Constraint | An invariant or rule with a named enforcement point | One current attempt; immutable operation intent; permitted policy scopes. Structural validation, authorization and lifecycle transitions have different checks. |

V5 editable diagram views: [system overview](https://aegises.org/agi-reactor/assets/v5-d0.svg), [information architecture](https://aegises.org/agi-reactor/assets/v5-d5.svg), [ontology primitives](https://aegises.org/agi-reactor/assets/v5-d6.svg). These are planned reference contracts; the full article includes their explanations.
