# Reactor · Draft 2.6 · 14 September 2026
Author: Ryan Smithright · Qthonic Labs · ryan@smithright.com
Canonical: https://aegises.org/agi-reactor/

From intent to governed systems

# Reactor

A Governable Reference Architecture for Enterprise AI Agent Orchestration

Qthonic is implementing this architecture. Responsible design disclosure · development status · executable evidence

Policy-governed service orchestration is all you need.

AuthorRyan Smithright · Qthonic Labsryan@smithright.com

The claim, its contribution and its limits

Thesis: the host’s coordination and governance functions can be expressed through policy-governed, stateful service contracts. A necessary host function that cannot be expressed or enforced under those contracts would refute that claim. It is a hypothesis about the host, not a claim that orchestration alone ensures reliable judgment or safe outcomes.

Contribution: composition of established mechanisms into one governable object model. Durable execution systems such as Temporal, authorization engines such as Cedar, transactional outboxes and audit records are foundations to build upon. No new primitive or universal superiority is claimed.
| Familiar concept | Reactor contract | What the composition requires
| Work item / workflow instance | Ticket | Durable obligation, one assignee, dependencies and acceptance evidence independent of the executing worker.
| Leased execution | Attempt | Current custody and generation checked at effect admission, including after worker replacement.
| External action | Operation | Immutable intent and identity survive attempts; an unknown result prevents blind replay.
| Standing directive / configuration link | Edict / binding | Intent and reusable behavior remain distinct from activated authority; changes retain ownership and provenance.

The value is a common contract across these mechanisms. An implementation using existing tools must demonstrate the composition, especially the seams between admission, dispatch and recovery.

Reference architecture

## System architecture

Interpret meaning. Govern effects. Preserve commitments.

Agentic judgmentInterpret · frame · select · propose

ProcessValidate · route · persist · enforce

Dashed violet → judgment. Solid green → process. Gray connectors show object relationships, not execution. A component may perform both kinds of step.

Swipe the diagram to follow the system →

Solid green arrows denote rule-driven process; dashed violet arrows denote agentic judgment. Ingress is received by process, then an agent interprets it and frames proposed tickets or edicts, or judges that no ticket is needed. Durable records are admitted and saved by process. The context compositor assembles approved definitions and permitted sources. Agents propose actions; services enforce policy and return results. Event and schedule triggers wake work by process. Thin gray lines are relationships, not execution.

Interpret

React → Interpret → Post

Semantic Event Fabric (e.g. NATS)
Communication across the system

Ingress
Chat · UI · events

Tickets
Durable work

Edicts
Standing direction

DEFINITIONS

Policy · templates
Skills · agent types

typed bindings

Context
compositor

Permitted knowledge + current work

Agent

Reactions
Routines

Services
Policy governed

Delivery

OWNED STATE
Objects · types · links · policy bindings · evidence
Processes change. Commitments persist.

Agents frame tickets and edicts, update existing work, or decide no ticket is needed. Services validate records, compose permitted context and enforce calls.Follow one mandate ↓

Reference architecture · trust boundary

## Replace cognition. Preserve control.

Reactor is a proposed governance and orchestration kernel for enterprise AI agents.

### Userspace
Replaceable cognition

Intake judgmentInterpret · frame intent

CompositorSelect · assemble context

Skills & agent typesDefine · compose behavior

Agent architecturesReason · plan · propose

↓ Typed requestsProtected service boundary↑ Decisions & results

### Reactor kernel
Enforced authority & durable state

IdentityPrincipal · tenant · grants

PolicyVersion · admit · revoke

OperationsEffect identity · limits · recovery

CustodyAssignment · lease · fencing

EvidenceOrigin · revision · receipts

Enforcement dependenciesOwning services & effect adapters · protected state · host isolation · credentials & egress · independent stop control

Cognition proposes meaning. The kernel governs protected reads, state changes and effects. A frame, skill or agent type grants no authority.

One contract, replaceable workers. Obligations and operation identities survive worker replacement. Each effect still requires current authority and execution custody.

What belongs on each side?

Kernel membership follows enforcement responsibility, not whether code uses a model. Userspace includes deterministic composition, policy drafting and evaluation. The kernel protects policy activation, authorized transitions and the records used to admit effects. Selecting context is userspace work; enforcing access to its sources remains a protected service responsibility.

These five responsibilities define a logical service kernel, not five mandatory daemons or an operating-system microkernel. Messaging transports requests; owning services enforce them. Any adapter, credential holder or state writer that can bypass admission belongs in the deployment’s trusted computing base. Host isolation, restricted egress and independent stop control must make that boundary real. [1] [2]

Evidence records provenance and observations, not guaranteed truth. Enforcement does not establish policy adequacy or benign intent. Kernel changes require governed qualification and compatible recovery; userspace replacement must retain pending operations and cannot widen authority.

Example implementation · proposed

## A mandate becomes a system.

Watch the factory. Select any component to inspect its role.Read the arrows ↗

Spike ticket

“Design and implement Compliance for the AI Kill Switch Act.”

Edict

“And moving forward, get the right leaders together monthly to review your AI Compliance News Report.”

Example source: H.R. 9917, introduced text ↗. The spike verifies the bill’s status, applicability and requirements before proposing controls.

READYExample simulation

Agentic intake interprets the compliance request and proposes a spike ticket and monthly-review edict. Process validates authority and saves each record. Dashed violet arrows denote judgment; solid green arrows denote process. Policy, templates and examples bind into reusable skills and an agent profile. The compositor assembles permitted context. An agent produces code; tests and policy admission precede delivery. NATS carries communication across the system. Objects and typed links persist underneath it.

NATS
calls · events · traces

CHAT

“Design AIcompliance.”

Agentic intake:
interpret, then propose.

SPIKE TICKET
AI Kill Switch Act

Research → implementation

durable obligation

EDICT
Monthly leadership review

AI Compliance News Report

REUSABLE DEFINITIONS

Policy

Who may stop or resume?

Templates

Control contracts

Examples

Assurance patterns

TYPED BINDINGS

skill + agent type

Other permitted context

COMPOSITOR

Context becomes a frame.

Guidance informs. Policy governs.

AGENT

EVENT WAKE
Agent judges the news
MONTHLY WAKE

produce

CONTROL SERVICE

Suspend · Resume

Scope: selected system

Authority: policy

Result: receipt or UNKNOWN

Illustrative control candidate

TEST + POLICY GATE

Admission required

DELIVERY

evidence returns to the ticket

PERSISTENT OBJECTS
types · links · policies · service methods · evidence

Services change. Obligations remain.

01

### One dictation. Two durable commitments.

The compliance request becomes a spike ticket. Monthly leadership review becomes a standing edict.Try a policy denial

Inside the factory


Illustration only · no model calls, meetings or deployments.Implementation specimen ↓

Implementation specimen · TypeScript contract (illustrative)

One possible service interface. Language and storage are implementation choices; the contract still requires implementation and qualification.interface ComplianceControl {
suspend(request: ScopedOperation): Promise<OperationResult>;
resume(request: ApprovedOperation): Promise<OperationResult>;
}
// OperationResult: refused | accepted | unknown
// The service verifies identity, policy, revision and operation custody.Download the complete illustrative contract and scenario ↓

Inside the system

## Follow the work. Keep the meaning.

Reference diagrams define the contracts. Blue labels identify the proposed compliance implementation.
01

Reference architecture

### Meaning requires judgment. Not every input requires a ticket.

An agent interprets incoming messages. It may propose tickets and edicts, update existing work, respond directly, or decide no action is needed.Process receives ingress. An agent interprets its meaning, relevance and intent, then proposes new ticket and edict artifacts, a link to existing work, or no new ticket. Choosing to respond, observe or disregard irrelevant input is agentic judgment. The service validates and persists any resulting record, update or permitted reply. Ambiguity can lead to clarification or escalation. Transport filters are process; semantic relevance requires judgment.
RECEIVE
INTERPRET
PROPOSE A DISPOSITION
ADMIT + RECORD
Ingress
Chat · dictate · event
Agentic intake
Meaning · relevance · intent
Frame new work
Ticket intent + acceptance
Edict scope + continuing duty
Link to existing work
Commentary · source · result
No new ticket
Respond · observe · disregard
Typed record
Validate authority + persist
Ticket / edict keeps its source
Linked update
Check revision + permitted change
Reply / disposition
Enforce scope + retention rules
Unclear? Clarify or escalate.
Meaning is judged. Record creation is governed. No new ticket is a valid outcome.

Intake is itself an admitted, bounded service call. Framing work and recognizing irrelevant input require judgment. Transport, validation and persistence follow process. “No ticket” still obeys communication and retention policy.

Proposed example

The compliance dictate yields two proposed records: a spike and a standing review edict. A new source may update the existing spike; an acknowledgement may need no new work.02

Reference architecture

### From words to delivered artifacts.

A dictate is retained as a source. Accepted work becomes a ticket; enduring direction becomes an edict. Every delivered artifact keeps its lineage.Agentic interpretation proposes a ticket and standing edict from an attributed dictate. Process admits and saves them. Agentic work authors artifact candidates; process records revisions and checks admission before delivery. Evidence returns to the ticket. A routine continues under the edict.
SOURCE
OBLIGATION
ARTIFACT
DELIVERY
Dictate
Original words + author
Ticket
Intent + acceptance + owner
frames
authors
Artifact revision
Content + type + provenance
check + admit
Delivered
Result + receipt
Evidence links the exact artifact revision back to its ticket.
Standing edict
Reusable direction
Routine → work → review → decisions
Each occurrence produces records and linked follow-up tickets.
Agentic judgment frames the artifacts. Process admits and saves them. Acceptance requires evidence.

Proposed example

Compliance dictate → spike → control code, tests and requirement mappings → qualified release and evidence.

Candidate, qualified and delivered are different artifact states. Ticket completion requires its acceptance criteria and the exact result; rejected candidates remain attributable.
03

Example implementation · proposed

### Work persists. Attention moves.

A ticket is a durable obligation above IPC: intent, owner, dependencies, state and linked evidence survive the process doing the work.

Agent A pauses requirements research while awaiting a source, drafts the news report, then resumes requirements. Agent B inventories systems concurrently. Implementation remains blocked until requirements and inventory satisfy acceptance. Recovery changes the current attempt and fences the old one; it does not erase tickets.
DURABLE TICKETS
ILLUSTRATIVE EXECUTION OVER TIME →
DEPENDENT WORK
Requirements
Agent A
Research
await source
Resume → evidence
News report
Agent A
Draft report
System inventory
Agent B
Independent work, concurrent with Agent A
Implement control
Requires both accepted inputs
BLOCKED
A yields one ticket and works another. B works in parallel. The join waits for accepted prerequisites.
Attempt lost; record retained

Agent A researches requirements while Agent B inventories systems. Implementation waits for both accepted inputs.

Dependencies govern readiness. Independent tickets can run concurrently.

Assignment names zero or one agent per ticket. Agents may own many tickets.

Attempts hold bounded execution custody. At most one is current per ticket.

The owning service must atomically claim work and enforce the current lease/generation at effect admission. Dependencies do not prevent unrelated tickets from conflicting on a shared resource; resource revisions, transactions or locks still do that job.

Reaction

Source changed → match a rule → create or wake linked work.

Routine

Month due → create the review occurrence → report, leaders, decisions.

NATS carries the notification. The work service deduplicates the event or scheduled occurrence and rechecks readiness, assignment and policy. A repeated message grants no extra attempt. Execution contract ↓
04

Reference architecture

### Compose behavior. Bind authority explicitly.

Definitions describe reusable behavior. Identities own work. Gray connectors show typed relationships, not execution steps.Edicts inform skills and may lead to policies only through authorized review and adoption. Templates and examples support skills. Agent types use skills and are instantiated by agent identities. A compositor resolves the profile and permitted sources into a cognition frame consumed by an attempt. Tickets have zero or one assignee, many historical attempts and at most one current attempt. Artifacts and evidence link to tickets. Attempts request operations and retain receipts. Versioned policy bindings apply to agent types, service methods, assignment, status transitions and resources; type membership alone grants no permission.
REUSABLE DEFINITIONS
COMPOSITION
WORKING CONTEXT
Edict
Enduring direction
Template
Expected structure
Example
Attributed precedent
Skill
Reusable procedure
informs
Agent type
Composed profile
uses
Cognition frame
Pinned context + sources
compositor
Permitted views · current work
Policy
Enforceable rule
review + adopt
Ticket
Intent + acceptance
State · dependencies · links
assigned to 0..1
Agent
Identity
instantiates
Attempt
Lease + generation
At most one current / ticket
executes
consumed by
A ticket retains every attempt.
Artifact / evidence
Revision + source + result
typed links
Operation
Caller · target · digest
requests effect
receipt refers to the exact result
POLICY BINDINGS
Agent types · service methods · assignment · ticket transitions · resources
Each binding names a versioned policy, target scope and authorized activation.
Each object: identity · type · tenant · revision · owner. Relationships carry meaning; storage is an implementation choice.

Proposed example

Monthly-review edict · compliance-analysis skill · report template · assurance examples · leadership agent profile · source-bound cognition frame.

Inspect the policy bindings

| Binding target | Enforced decision
| Agent type / identity | Eligible roles, allowed service scopes and limits. A profile alone grants no capability.
| Ticket assignment | Eligible assignee, tenant, custody and authorized reassignment; invalidate stale execution before takeover.
| Ticket status | Allowed transition, current revision, prerequisites and required acceptance evidence. A worker cannot simply declare delivery.
| Service method / resource | Which verified principal may perform this action on this target, under which conditions.
| Reaction / routine | Allowed triggers, occurrence identity, owner, overlap, suspension and admission limits.
| Data / resource budget | Permitted context and disclosure, retention, quota and bounded reservations.

A binding is a typed link to a policy revision and target scope. These scopes share one policy model. Promoting a policy requires authorized review and activation.
05

Reference architecture

### Types define the request. Policies govern the effect.

The ontology gives a call its meaning. Local policy decides admission; the owning service enforces it at use. A permit is not a completed effect.The ontology resolves a request to a typed service method. Local policy bindings and verified facts determine admission. The owning service enforces authority and resource concurrency at use. A result or unknown outcome returns under the same operation identity and links to the ticket. NATS transports calls; it does not grant authority.
SHARED MEANING
LOCAL AUTHORITY
Typed service ontology
Service · method · resource · input / result schema
Versioned policy bindings
Verified caller · scope · trusted state · limits
GOVERNED
BOUNDARY
Service call
Authenticated request
service.method
Typed target + arguments
Versioned contract
Decide → enforce
Recheck at use
Owning service
Current custody + resource revision
Result / receipt → same operation identity → ticket evidence
No permission → no effect
Stable contract. Replaceable implementation.
PERMITTED → execute
REFUSED → preserve work
UNKNOWN AFTER SEND → reconcile before replay

Proposed example

control.suspend(target) illustrates a typed operation. Its implementation must qualify independent stop control, authority checks and recoverable results.Explore admission ↗

Public ontology supplies shared meaning. Each enterprise adopts its own authority bindings. NATS is the transport; direct access to protected execution must remain unavailable.

06

Example implementation · proposed

### The review becomes part of the system.

A sourced report reaches the right leaders each month. Decisions create owned follow-up work. That work informs the next review.Follow the continuing loop ↗Sourced AI compliance news becomes a report. Proposed legal, security, engineering and accountable AI leadership roles review it monthly. Decisions create owned follow-up tickets. The routine continues under its standing edict.

NEWS REPORT
Sources + changes

MONTHLY

Legal
Security
Engineering
AI owner

DECISIONS
Owned tickets

Changes feed the next review

Proposed roles shown. Actual participants, ownership and schedule require adoption under the edict. Human leadership decisions are shown with dotted amber arrows.

What it knows.Sources, context and uncertainty.

What it owes.Tickets, owners and acceptance.

What it may do.Identity, policy and scope.

What it can afford.Reserved resources and limits.

The enforcement foundation

## A reference monitor enforces the policies it is given.

Anderson’s reference monitor mediates protected access. Its implementation must resist tampering, mediate every protected reference and be small enough for thorough analysis. [1] Saltzer and Schroeder sharpen the obligation: explicit permission, complete mediation and least privilege. [2]

The Reactor applies this boundary to service calls. An agent proposes; the owning service admits or refuses. Policy, trusted facts and enforcement must all hold. Changes to those controls require their own authority.

The proposed controls require adequate policies, qualified implementations and declared host assumptions. The animation illustrates the design; it does not validate a deployment.

Policy adequacy · Poisoned context · Code-release controls

## Persist obligations. Replace execution.

Objects, links and messages carry the meaning. Typed service calls do the work.

### One assignee. Durable work.

A ticket has zero or one assigned agent. Attempts can change; at most one is current. The resource owner still handles concurrent updates.

### Context carries its sources.

Owned records → permitted views → composed frames → attributed evidence. Types and bindings connect them. Retrieved instructions never widen authority.

### Uncertainty stays visible.

An operation keeps its identity across crashes. A lost reply may leave UNKNOWN. An authorized reconciler owns the gap; blind replay stops.

Reference architecture · assurance obligations

## Every guarantee has dependencies.

The trusted computing base is the code, state and infrastructure whose failure can defeat a particular guarantee. This map declares those dependencies; it does not certify them.

| Guarantee | What must be trusted | Failure to inject | Required outcome

| Caller and authority are authentic | Credential issuer, verifier, policy activation path, current grants and revocations. | Forged identity; revoked grant; substituted policy revision. | Refuse before a protected read, state change or effect. A supplied principal name is insufficient.

| Only current custody can admit an effect | Authoritative writer, serialized claim/admission, database integrity, trusted time and generation. | Concurrent claims; stale worker; state rollback. | One current attempt per ticket. Fence stale admissions; block conflicting successors while earlier dispatch is unresolved.

| Effects cannot bypass admission | Service enforcement, effect adapter, credentials, egress isolation and host controls. | Direct target access; substituted target/arguments; expired admission. | Target accepts only the bound scope. Any credential holder that can bypass the check is part of this trusted base.

| Delivery does not confer authority | End-to-end identity and request validation; owning-service deduplication. Broker security for confidentiality and availability. | Replay, reorder, duplicate or drop a fabric message. | Replay grants no new operation. Loss may stall work. If the broker can forge trusted identity or state, it also becomes an authorization dependency.

| Limits, evidence and recovery survive workers | Reservation writer, durable operation journal, evidence provenance, recovery epoch and independent freshness evidence. | Two agents spend the same capacity; erase a receipt; restore older authority. | Atomic aggregate limits. Missing or stale recovery evidence holds affected admission. Provenance alone does not establish truth.

| Stop remains available | Independent stop authority and enforcement path; bounded outstanding dispatch. | Compromise a worker; stop after admission but before target acceptance. | Close new admission. Expose and reconcile in-flight effects; stopping computation cannot undo an accepted effect.

Minimize privileged code and credentials per effect. A database or adapter may remain trusted even when cognition is isolated. Formal assurance, where used, must name the property, configuration and assumptions. Example: seL4’s published assumptions ↗

Implementing shared limits and consequential approval

Limits: the resource service owns reservations keyed by operation, tenant, scope, unit and accounting window. Admission atomically checks all applicable scopes and reserves capacity before dispatch. Settle from attributable results; retain UNKNOWN reservations. Release requires evidence that the effect did not occur or cannot still occur. Cedar can evaluate a permission decision over trusted inputs; the state owner must prevent concurrent requests from spending the same capacity.

Approval: show the reviewer the exact candidate, requested scope, source evidence, evaluation result, cumulative exposure and unresolved effects. Approval binds the candidate digest, policy revision, limits and expiry. A changed candidate invalidates it. The proposing worker cannot issue its own release authority.

Model and code changes: compare against a fixed baseline with predeclared success and regression criteria. Bind evaluation evidence to the model, prompt/skill, code, data and environment revisions. Qualify capability and policy limits before bounded exposure; retain a checked fallback. A favorable A/B score alone cannot authorize release.

Executable example · local qualification

## Run the contract. See its limits.

Selected Qthonic lease and fencing functions, composed with a new local test implementation. This is executable evidence for the named specimen, not qualification of the deployed Qthonic stack.

14contract tests completed

2 / 2deliberately broken controls detected

0model calls or production effects

Within an existing grant

### A redirected report is refused.

A fixed poisoned-source proposal redirects a report. Admission refuses the recipient outside its provisioned scope. The permitted recipient succeeds.

The semantic limit

### A permitted report can still mislead.

The same boundary accepts unsupported claims sent to the allowed recipient. This is an observed limitation. A declared data label is not verified content classification.

| Fault exercised | Observed in this specimen | Boundary of the result

| Concurrent claims / stale worker R16 | One claim succeeds; stale and forged fences are refused. A successor cannot replace an unresolved step. | One trusted host with serialized SQLite admission. Not a production-writer atomicity proof.

| Crash after target accepts R17 | Worker exits 86 after HTTP 200. One target effect; UNKNOWN retained; same-key replay and replacement ID refused. | Non-idempotent loopback target. No automatic reconciliation. Unknown reservations remain charged.

| Restore before effect and revocation R18 | Old epoch and revoked caller refused. UNKNOWN stays protected after the test-only global hold is lifted; unrelated work succeeds. | Only work state is restored. Authority journal and revocations survive outside that snapshot. Full authority loss is unqualified.

| Stop with dispatch in flight R19 | New admission is refused; an earlier admitted effect completes after stop. | Observed limit: this stop does not cancel or reverse in-flight external effects.

| Two agents share a limit R25 | One of two concurrent effect reservations succeeds against a shared cap of one. | Lifetime effect count for one disposable tenant. No distributed windows, money accounting or multi-scope reservation test.

| Payload / route substitution | Target receives the frozen admitted payload. Unconfigured endpoints and invented work steps are refused. | Routes and steps are trusted fixture configuration. Authentication, OS isolation and semantic duplicate detection are unqualified.

Download the executable specimen ↓

Python 3.9+ · macOS / Linux · standard library · disposable local state

Run instructions · Observed results · Source provenance · Local reviewunzip reactor-contract-demo.zip
cd reactor-contract-demo
python3 run.py --output my-result.json

Timing, cost and unqualified deployment boundaries

Observed local admission timing: median 0.633 ms, p95 0.775 ms, 100 samples after 20 warmups. Environment: 3.9.6 Python / macOS-26.5.1-arm64-arm-64bit. Includes local locking, SQLite, Python allowlist, custody checks and committed reservation/evidence. Excludes Cedar, NATS, network, inference, human review and external delivery. This is not enterprise throughput or end-to-end latency.

A deployment must measure its full admission path, contention, journal growth, model/tool spend, review delay and recovery backlog against declared budgets. The specimen has no cryptographic caller authentication or mandatory host isolation. The readme states the trusted inputs, surviving-state assumptions and unimplemented reconciliation/release mechanisms. Completed checks include expected limitations; they are not a safety certification.

The animated journey, step by step

One dictation. Two durable commitments.

Agentic intake interprets the dictate, frames a spike and a monthly-review edict, and proposes both. The owning services check authority and persist the records.

Bind the right knowledge and rules.

The agent investigates the bill and selects relevant policies, templates and examples. Governed services validate and record the proposed bindings.

Compose the agent’s working frame.

The compositor assembles the brief, verified sources, relevant skills and pending work. Legal, security, engineering and the accountable AI owner are proposed review roles.

Produce a control candidate.

The agent designs a control service and proposes its implementation, tests and requirement mappings. News feeds a sourced AI Compliance News Report; findings can create linked follow-up tickets.

Check the work. Enforce the boundary.

The illustration admits a reviewed candidate only within its policy and release scope. A denied caller cannot cross the same boundary. Actual compliance needs qualified controls and evidence.

Deliver now. Keep reviewing.

A governed release can deliver the control. The edict continues as a monthly review of the AI Compliance News Report, with an owner, the right leaders and linked decisions.

The working vocabulary

ObjectAn owned record with a stable identity, type and revision. Its storage representation may change.

Link / bindingA typed relationship. A binding applies an exact definition to a scope; protected changes use the owning service.

Message / invokeA message communicates. An invocation requests an operation through an authenticated, typed service contract.

Edict / policyAn edict records standing intent. A policy defines enforceable rules through authorized promotion, versioning and activation.

Skill / agent typeA skill defines a reusable procedure. An agent type defines a reusable profile. Neither grants identity or authority.

Compositor / frameThe compositor assembles a bounded frame of permitted context: intent, constraints, sources and pending effects.

Reaction / routineA reaction responds to an event. A routine defines recurring work. Both use governed admission.

Operation / evidenceAn operation records immutable effect intent; evidence records attributable observations and results. Caller, target and arguments survive takeover.

How durable work scales

The ticket is the durable coordination record. Messages notify; workers execute. An atomic claim establishes the current attempt under the assigned identity, bounded by a lease and generation. A stale worker must be rejected at effect admission. A new attempt preserves prior artifacts, pending operations and interrupt-return context.

Dependencies form a constrained work graph: edges name the required outcome, cycles are rejected where they would deadlock readiness, and failed or cancelled prerequisites require an explicit disposition. Typed links to sources, edicts, decisions, artifacts, operations and evidence add context without all becoming blocking dependencies. A parent ticket coordinates child tickets; each child has its own assignee and acceptance.

Reaction rules match events. Routines define recurring occurrences. Both admit work through the same policies, with stable trigger identities, overlap rules and bounded concurrency. Assignment, readiness, lease, priority and resource budget are evaluated from authoritative state; queue delivery is not a claim.

Different tickets can contend for the same object. The resource owner applies atomic revision checks or suitable transactions/locks. An operation binds tenant, caller, method, target and argument digest. If a reply is lost after sending, preserve UNKNOWN and reconcile that operation before considering replay.

These are reference contracts. NATS consumers provide delivery mechanics; transaction isolation provides database concurrency tools. Neither by itself implements ticket custody or prevents duplicate external effects.

Reference implementation choices

| Role | Reference | Contract
| Communication | NATS / JetStream | Calls and durable notifications; neither grants assignment.
| Owned state | PostgreSQL + control service | Transactional records, custody, revisions and outbox.
| Authorization | Cedar + service enforcement | Proposed integration: validate schemas and refuse evaluation errors.
| Execution | Compositor, workers, adapters, supervisor | Bound context, egress, resources and independent stop control.
| Evolution | Governed release controller | Isolated candidate → observed canary → staged traffic; retain a checked hot fallback.

These are reference choices and contracts, not a qualified deployment.

A deployment must qualify containment, concurrent admission, policy adequacy and recovery on its actual stack. Restore begins with new effect admission held until stale execution, unresolved effects and newer authority changes are reconciled.

Detailed record contracts in archived draft 1.7.1 ↗

Optional extension: shared ontology and public stewardship

The kernel can operate with local, versioned schemas. It does not depend on a consortium, OWL 2 adoption or an institutional mandate.

PanSigna.org (“all signals”) is a separate proposal for a public intermediate-representation ontology, index and wiki. Shared identifiers could support interoperable service and policy profiles; W3C OWL 2 is one semantic foundation. [3]

Internet Society stewardship remains a proposed mandate requiring an agreed charter. [4] Public definitions confer no authority over a deployment. Local adoption, interpretation and enforcement remain accountable decisions.

Sources, scope and citation

James P. Anderson. Computer Security Technology Planning Study, Volume I (1972), §§3.2.1–3.2.2, pp. 8–10. Original report ↗

J. H. Saltzer and M. D. Schroeder. “The Protection of Information in Computer Systems” (1975), §I.A.3. Primary source ↗

W3C. OWL 2 Web Ontology Language: Document Overview, Second Edition (2012). Recommendation ↗

Internet Society. Policy Development Process. Stewardship context ↗

U.S. Congress. AI Kill Switch Act, H.R. 9917, introduced in House, 23 July 2026. Illustration source ↗. The introduced text is a research input, not a finding of present legal obligations.

Core NATS · JetStream · PostgreSQL transactions · Cedar evaluation semantics.

The design assumes trustworthy administrative roots and correctly enforced isolation. It addresses bounded operational hazards; it establishes neither general alignment nor protection from compromised root authority. Institutional participation and the compliance implementation shown are proposals.

Smithright, Ryan. Reactor: A Governable Reference Architecture for Enterprise AI Agent Orchestration. AEGISES, draft 2.6, 14 September 2026. Version permalink · BibTeX · CSL-JSON.

Animation source: TypeScript · CSS · Archived previous edition.

## Design artifacts

Whiteboard ArchitectureView drawing

Ryan Smithright’s original drawing. The animation preserves its construction: definitions → bindings → agents → governed delivery.

Acknowledgments

This proposal builds on James P. Anderson’s reference monitor, Jerome H. Saltzer and Michael D. Schroeder’s protection principles, and research in operating systems, distributed systems, programming languages, information theory and AI safety.

The author acknowledges the maintainers and contributors of NATS, PostgreSQL, Cedar and the wider open-source systems community for the software and documentation informing the reference implementation choices.

W3C and the IETF provide standards foundations; the Internet Society and MANRS inform the discussion of shared stewardship and routing security.

Acknowledgment does not imply participation, review or endorsement. Responsibility for this proposal and its claims rests with Ryan Smithright.

Implementation in progress · responsible design disclosure

## Build openly. Improve under governance.

Qthonic is implementing this architecture. We are publishing its design, assumptions and unresolved risks for responsible review, cooperation and use. This is a disclosure of work in progress, not certification of a safe deployment.

### Observed in development

In Qthonic’s development work, we have witnessed how readily recurring review can generate and delegate ideation, research, refactoring and candidate improvements to skills or core services, including A/B-tested implementations. The ticketing engine can populate its own work queue and support self-delegation through different agent architectures.

Implementation experience reported by Ryan Smithright, Qthonic. The public contract tests are separate evidence and contain no model calls.

### Recursive improvement, bounded

These are bounded recursive self-improvement (RSI) loops over software: the system proposes work on parts of its own implementation. These observations do not establish autonomous capability gains or reliable self-improvement. Proposed work still requires admission, an owner, a budget, independent evaluation and authorized release. Workers may improve a skill; they may not widen their own grants or waive the gate.

Review→Propose tickets→Delegate candidates→Compare evidence→Authorize release

We invite peers to consider this architecture for responding to new AI safety legislation through shared ontology language and policy-governed services. The intended path is traceable: legal source → reviewed interpretation → versioned requirements → controls → qualification evidence → accountable adoption. Shared contracts can reduce repeated integration work and expose coverage gaps; they cannot guarantee a complete or correct legal interpretation.

Scope of the architecture

## A substrate for enterprise AI agents.

This is a reference design for governable enterprise AI agent orchestration. It combines durable work, explicit authority and recoverable effects. Scalability and control effectiveness require qualification in each deployment.

The kernel governs identity, policy, operations, custody and evidence. Userspace supplies the compositor, skills, agent types and intake judgment. The boundary constrains execution; it does not establish the safety of the cognition running within it.

Risk, control and accountability

## AI Safety Risks

30 risks. Concrete service responsibilities. Evidence before assurance.

A proposed control map for enterprise deployment review. Each row connects a failure mode to an accountable owner, service records, an enforceable boundary and evidence needed to assess it. These controls require implementation and validation.

The sources below inform risk framing; the service designs and qualification exercises are the author’s proposals. This is a coverage map, not an exhaustive taxonomy or probability ranking. Assess severity, likelihood, uncertainty, exposure and reversibility for the actual use case and affected people.

Shared service information architecture

Implement these responsibilities through the services already described. Each record has one authoritative writer, a stable identity, tenant, revision and accountable owner. Split deployments for measured contention, independent rollout or failure containment.

Governance and assuranceRisk assessments, control specifications, qualification runs, risk acceptances and incidents. Assess → review → qualify → monitor → remedy.

Identity and policyPrincipals, delegations, grants, policy revisions and decisions. Propose → approve → activate → revoke.

Knowledge and contextSources, claims, trust labels, cognition frames and memory promotions. Resolve → compose → corroborate → correct.

Work and resourcesTickets, attempts, dependencies, occurrences and reservations. Admit → claim → fence → reconcile.

Build and releaseSource and artifact digests, manifests, reviews, canary observations and release decisions. Build → test → admit → observe → promote or revert.

Execution and recoveryOperations, receipts, stop epochs, checkpoints and reconciliation cases. Enforce → observe → stop → reconcile → resume.

Required links: risk → affected system and people → control → policy revision and enforcement point → qualification evidence → deployment → incident or review. A risk assessment records intended use, impact, uncertainty, owner and next review. A control specification names trusted inputs, limits, failure behavior and the service that enforces it.

Evidence contract: a qualification run identifies the exact artifact, model configuration, policy, environment, test revision, evaluator, observations and validity period. Qualification plans fix pass/fail criteria before execution. A material change invalidates dependent conclusions. Raw observations remain distinguishable from agent explanations.

Residual-risk decisions: record the authorized decision-maker, rationale, scope, conditions and expiry. Acceptance cannot grant a capability, override a prohibition or replace a missing mandatory control. Unassessed and unverified remain explicit states.

Download the proposed risk register · JSON ↗

Proposed risk controls and qualification evidence
| Risk and consequence | Service responsibility and records | Proposed control | Evidence and remaining risk
| Direction and authority
| R01

### Inadequate policy

A permitted action still harms people because the rule omits a hazard, affected party or sequence of effects.

Architecture failure mode |

#### Policy and assurance

Risk assessment · control specification · policy revision · exception

Accountable: Domain risk owner. |

Define intended use, prohibited outcomes and measurable limits. Link requirements to enforcement points and tests. Block prohibited uses and failures of mandatory controls. Accept remaining risk only through a named authority, recorded justification, bounded scope and expiry. An LLM cannot approve its own policy. |

Qualify: Try harmful but syntactically permitted actions and action sequences. Test omissions, conflicting rules and misleading attributes.

Remaining risk: A passing evaluator establishes rule execution, not the adequacy of the rules. Some uses should remain prohibited.
| R02

### Policy capture and self-authorization

An agent, insider or pressured reviewer turns a suggested edict into authority, weakens a control or approves their own exception.

Framing: A |

#### Policy lifecycle and identity

Edict proposal · policy diff · approval · activation epoch

Accountable: Policy authority. |

Separate proposal, review and activation. Require independent authorized approval for grants, risk limits and control changes. Bind approval to the exact diff, scope and expiry. Enforce separation of duties in the service; invalidate dependent approvals when inputs change. |

Qualify: Attempt self-approval, stale-diff activation, reviewer impersonation and a grant change hidden inside a routine update.

Remaining risk: Dual control reduces unilateral abuse; collusion and institutional pressure require external oversight.
| R03

### Impersonation and confused deputies

A caller borrows another identity or persuades a more privileged service to act beyond delegated scope.

Framing: A |

#### Identity and service admission

Principal · delegation · grant · request audience · revocation

Accountable: Identity service owner. |

Derive identity from verified credentials, never request text. Bind delegation to tenant, purpose, target, method, audience and expiry. Preserve the original caller through delegation. Recheck current authority at effect admission; narrow rather than accumulate grants. |

Qualify: Use a valid credential for the wrong tenant, audience or target; replay a revoked delegation through a privileged intermediary.

Remaining risk: Stolen root credentials and compromised credential issuers exceed ordinary caller checks; see R05.
| R04

### Bypassed mediation and containment

An agent reaches a database, network, filesystem, cloud account or device through an ungoverned path.

Framing: A |

#### Sandbox, secrets and egress enforcement

Workload identity · capability manifest · network policy · isolation evidence

Accountable: Platform security owner. |

Run untrusted execution without ambient host credentials. Mediate protected I/O, restrict destinations and mount scopes, and separate worker access from control-plane access. Give the enforcement service its own authority and failure domain. Deny new protected effects on enforcement failure. |

Qualify: Attempt direct resource access, credential discovery and cross-tenant escape from the actual worker environment; interrupt the decision service.

Remaining risk: Containment depends on the host, device and identity substrate. A gateway alone cannot establish it.
| R05

### Compromised administrators or institutions

An authorized root operator changes enforcement, suppresses evidence or uses the system for an abusive institutional purpose.

Framing: O |

#### Privileged access and independent audit

Root-access approval · key custody · break-glass event · external audit copy

Accountable: Governing board or accountable executive. |

Use separate administrative domains, hardware-protected keys where appropriate, time-bounded privileges and independently retained audit records. Require dual control for root changes; make emergency access attributable and reviewable. Provide an external reporting route and a recovery authority outside the affected domain. |

Qualify: Exercise emergency access and root-key recovery. Verify an operator cannot silently erase the independent audit copy.

Remaining risk: This architecture does not protect against all colluding roots or coercive institutions. Some authority must remain external to the system.
| Meaning, knowledge and data
| R06

### Prompt injection and goal steering

Poisoned content changes what an agent proposes or posts, even though its formal permissions remain unchanged.

Framing: A |

#### Intake, compositor and proposal admission

Source revision · trust label · cognition frame · intent proposal · provenance link

Accountable: Context service owner. |

Keep retrieved content distinct from governing instructions; carry source trust and lineage into frames. Bind consequential proposals to an independently established mandate. Apply deterministic scope checks where possible; route unresolved semantic intent to a qualified reviewer with independent evidence. Treat outbound posts as effects too. |

Qualify: Plant instructions in a retrieved document and an event payload. Check both grant integrity and whether the resulting proposal violates the mandate within existing grants.

Remaining risk: Instruction separation and classifiers do not prove semantic immunity. A persuasive, apparently relevant source can still mislead judgment.
| R07

### False, stale or unsupported conclusions

A fabricated citation, obsolete requirement or incorrect inference becomes a decision, ticket or delivered artifact.

Framing: N |

#### Knowledge and evidence resolution

Claim · source locator and revision · observation time · uncertainty · contradiction

Accountable: Domain knowledge owner. |

Separate observations from model summaries and conclusions. Resolve cited evidence, record freshness and scope, and expose contradictions. Require domain review or abstention where uncertainty exceeds the use-case threshold. A source link must support the actual claim, not merely exist. |

Qualify: Inject nonexistent citations, outdated facts and mutually inconsistent sources. Measure false acceptance on representative domain cases.

Remaining risk: Provenance establishes origin, not truth. Authoritative sources can be wrong and emerging facts can remain unsettled.
| R08

### Poisoned memory and self-reinforcing learning

An unverified result becomes persistent knowledge, a skill or a training example, then validates itself through repeated reuse.

Framing: A |

#### Memory, skill and model-data lifecycle

Candidate memory · source lineage · promotion decision · training manifest · retirement

Accountable: Knowledge lifecycle owner. |

Quarantine untrusted additions. Distinguish generated content from observations and independent evidence. Promote reusable knowledge, skills and training data through versioned review. Track downstream consumers so corrections invalidate affected frames and evaluations. Make deletion and rollback explicit. |

Qualify: Seed a false lesson, reuse it across agents, then revoke it. Verify the original claim is not treated as corroboration and affected consumers are identified.

Remaining risk: Removing a record does not remove its influence from trained weights or already-issued decisions; retraining and remediation may be required.
| R09

### Semantic mismatch and ontology drift

Compatible-looking names conceal different units, meanings, permissions or schema versions across services and jurisdictions.

Architecture failure mode |

#### Type registry and contract resolution

Type revision · method schema · units · semantic mapping · compatibility decision

Accountable: Service contract owner. |

Pin versions and explicit units. Resolve method, target and effect class before admission. Review mappings between vocabularies; reject unknown or lossy conversions for consequential operations. An ontology update must not silently widen policy scope or change a method’s effect. |

Qualify: Swap units, aliases and schema versions; introduce an apparently compatible mapping that changes authorization or meaning.

Remaining risk: Type correctness cannot settle contested concepts or guarantee that a shared ontology represents every affected community fairly.
| R10

### Privacy loss, secret leakage and unlawful data use

Sensitive information crosses a tenant, purpose, recipient, retention or geographic boundary through context, logs or outputs.

Framing: N |

#### Data access, compositor and disclosure

Data classification · purpose and legal-basis decision · retention rule · recipient · transfer review

Accountable: Data protection owner. |

Minimize data before model access; enforce tenant, purpose and recipient restrictions at retrieval and disclosure. Keep secrets outside prompts and ordinary logs. Propagate deletion and retention rules to derived stores. Route restricted transfers for an applicable, approved legal determination. |

Qualify: Plant synthetic secrets and cross-tenant canaries in retrieval, telemetry and output paths. Verify retention expiry and deletion propagation.

Remaining risk: Inference, memorization and external copies can defeat simple deletion or redaction. Cross-border legality requires jurisdiction-specific assessment.
| Code, models and capability
| R11

### Harmful generated code

An apparently valid change introduces a backdoor, unsafe behavior or a new path around the reference monitor.

Framing: S P |

#### Isolated build, assurance and release

Change intent · source and artifact digest · capability diff · test plan · approval · canary result

Accountable: Release authority. |

Bind release to exact source, dependencies, artifact and target. Build without production credentials. Independently review capability and enforcement changes; derive tests from hazards, not only agent-authored happy paths. Check static, dependency and behavioral evidence. Bound candidate effects and maximum exposure; simulate irreversible effects until separately authorized. Observe staged traffic, qualify schema compatibility and retain a tested hot fallback. Missing mandatory evidence blocks promotion. |

Qualify: Submit a compiling candidate with an unauthorized egress path, disabled check or forged test result. Verify rejection and exercise rollback under actual load.

Remaining risk: No general test suite proves arbitrary code benign. Rollback cannot undo disclosed data or accepted external effects. Irreversible changes need separate authority and a qualified recovery plan.
| R12

### Compromised supply chain

A package, model weight, tool description, build runner or artifact is substituted after review or arrives already compromised.

Framing: S P |

#### Artifact registry and build verification

Dependency manifest · model digest · builder identity · provenance · signature · vulnerability disposition

Accountable: Software supply-chain owner. |

Pin reviewed dependencies and artifacts; verify provenance against trusted identities. Separate source approval, build authority and deployment authority. Verify the artifact actually executed matches the admitted digest. Review tool metadata and model provenance as dependencies; define revocation and replacement paths. |

Qualify: Substitute a dependency or artifact after approval, use an unauthorized builder, and present a valid signature from the wrong trust domain.

Remaining risk: Authentic provenance does not establish benign behavior. Trusted maintainers, builders and upstream models can still be compromised.
| R13

### Evaluation gaming and evidence laundering

A model recognizes the test, fabricates a receipt or gets its own explanation accepted as proof of success.

Framing: I |

#### Evaluation and evidence custody

Test revision · held-out case set · executor identity · raw observation · artifact-bound verdict

Accountable: Independent assurance owner. |

Keep material acceptance criteria and observations under independent control. Record exact specimen, environment and raw effects; bind verdicts to tested revisions and expiry. Use blinded cases, negative controls and deployed monitoring. A generated claim or reviewer title cannot constitute execution evidence. |

Qualify: Submit fabricated receipts, stale results and a candidate that passes the visible suite but fails held-out tasks. Confirm changed artifacts invalidate verdicts.

Remaining risk: Evaluations sample behavior. Hidden capabilities, distribution shift and evaluation awareness remain possible.
| R14

### Unreviewed model or capability change

A provider update, fine-tune, prompt revision or tool bundle changes behavior beyond the deployment’s evaluated limits.

Framing: N |

#### Model routing and qualification

Model release · configuration digest · tool scope · capability evaluation · deployment envelope

Accountable: Model lifecycle owner. |

Inventory the complete model configuration, including retrieval and tools. Gate routing changes on use-case evaluations; keep a known compatible fallback or suspend the affected workflow. Monitor behavioral drift when providers cannot supply immutable versions. Higher capability does not inherit prior approval automatically. |

Qualify: Change the model or tool set behind the same endpoint. Verify detection, qualification invalidation and controlled fallback.

Remaining risk: Provider opacity and incomplete capability tests limit assurance; some deployments must require stronger version guarantees.
| R15

### Dangerous or abusive use

A permitted workflow materially assists cyber abuse, weapons development, exploitation or another prohibited high-harm purpose.

Framing: I |

#### Use-case admission and capability controls

Purpose assessment · restricted capability class · authorized operator · escalation · abuse incident

Accountable: Abuse prevention authority. |

Assess purpose and capability together. Restrict high-risk tools, datasets and execution environments; impose limits across linked requests rather than only individual prompts. Require qualified specialist review for exceptional access. Suspend prohibited or inadequately controlled uses and preserve an appeal path for legitimate research. |

Qualify: Use controlled, non-operational misuse evaluations to test decomposition across requests, delegation and inconsistent purpose declarations.

Remaining risk: Dual-use intent is ambiguous; content filters and identity checks cannot eliminate misuse or access through other providers.
| Execution and recovery
| R16

### Stale workers and conflicting effects

Two attempts act as current, or separate valid tickets overwrite the same resource.

Architecture failure mode |

#### Work custody and resource admission

Ticket · assignee · attempt generation · lease · resource revision · operation

Accountable: Work service owner. |

Claim attempts atomically; bind effect admission to current generation, operation identity and resource revision. Keep at most one current attempt per ticket. Resource owners serialize conflicts. Do not dispatch a conflicting successor while prior dispatch remains unresolved unless the target provides effective fencing. Queue delivery is never a claim. |

Qualify: Pause a worker after admission but before target acceptance; expire its lease and start a successor. Also race two valid tickets against one resource revision.

Remaining risk: An external target that cannot enforce fencing needs a serialized adapter or narrower automation; local leases alone cannot stop it.
| R17

### Unknown outcomes and duplicate effects

A target accepts an operation, the reply is lost, and retry creates a second external effect.

Architecture failure mode |

#### Operation journal and reconciliation

Immutable operation identity · target receipt · UNKNOWN case · reconciliation decision

Accountable: Integration service owner. |

Persist intent before send. Bind operation identity to tenant, caller, method, target and argument digest. Record target deduplication scope, retention and status-consistency guarantees. Preserve UNKNOWN and assign reconciliation. Treat absent or expired target records as unresolved unless authoritative evidence excludes acceptance and any outstanding dispatch. Prohibit blind replay. |

Qualify: Crash after target acceptance but before the local receipt. Exercise redelivery, delayed target visibility and expired idempotency records; verify reconciliation without duplicate effects.

Remaining risk: Without target idempotency or status lookup, both completion and non-duplication may be impossible to guarantee. A person may have to resolve the case.
| R18

### Restore revives obsolete authority or work

A backup predates an external effect, a revoked grant or a completed obligation, and recovery replays it.

Architecture failure mode |

#### Backup, restoration and operation reconciliation

Backup checkpoint · restore epoch · revocation watermark · external effect ledger · resume approval

Accountable: Recovery authority. |

Begin restore with new effect admission held and previous execution fenced. Keep operation and revocation watermarks outside the restored failure domain. Establish their freshness and completeness; reconcile newer effects, completed work and authority changes before reopening each scope. Unknown evidence keeps that scope restricted. Keep recovery keys outside ordinary artifact storage. |

Qualify: Restore a backup taken before an accepted effect and a later revocation. Confirm neither duplicate execution nor resurrected permission.

Remaining risk: If the independent evidence is missing, the system may have to remain restricted. A successful database restore is not permission to resume effects.
| R19

### Ineffective stop or unsafe restart

Pausing the agent leaves queued effects, child workers, credentials or a physical process active; restart repeats unfinished actions.

Framing: I |

#### Independent supervisor and effect admission

Stop scope and epoch · worker inventory · pending effect · stop observation · resume authority

Accountable: Operations safety owner. |

Block new effects at their owners, revoke scoped execution custody and account for queued and in-flight work. Keep stop control independent of the model and worker. Define bounded stop behavior per adapter and device; resume through reconciliation and explicit authority. Preserve a usable manual control path. |

Qualify: Stop during a tool call, a queue backlog and a network partition. Observe target state and elapsed stop time; test restart with unresolved effects.

Remaining risk: An accepted payment, released message or moving machine may not be reversible. Stopping compute is not necessarily stopping harm.
| R20

### Runaway delegation and feedback loops

Agents, reactions and routines amplify one event into unbounded work, spending or service disruption.

Framing: A |

#### Scheduler, budget reservations and event admission

Causal event chain · occurrence key · delegation budget · reservation · circuit-breaker state

Accountable: Workload operations owner. |

Deduplicate triggers, bound fan-out and recurrence, reserve shared budgets atomically, and enforce depth, time and effect limits across descendants. Propagate cancellation and backpressure. Separate a semantic event from a command; receiving it grants no work or authority by itself. |

Qualify: Replay a trigger, create a reaction cycle and fan out concurrent children against one budget. Verify caps and recovery without losing accepted obligations.

Remaining risk: Useful workloads can resemble abuse. Limits trade throughput and responsiveness for a bounded failure radius.
| People and consequential decisions
| R21

### High-consequence domain error

A mistaken recommendation or action affects health, physical safety, essential services or substantial assets.

Framing: N |

#### Domain decision and actuation

Validated operating envelope · qualified operator · decision rationale · interlock · intervention

Accountable: Accountable domain professional. |

Constrain automation to qualified conditions and thresholds. Separate advice from authority to act. Require appropriately qualified review and independent interlocks where consequences demand them. Define fallback behavior for uncertainty, delayed review and unavailable communication before activation. |

Qualify: Exercise boundary conditions, sensor or source failure, reviewer absence and out-of-envelope requests in an appropriate controlled environment.

Remaining risk: The reference architecture cannot supply clinical, engineering or sector-specific assurance. Some functions should retain human or separately certified control.
| R22

### Discrimination and exclusion

Decisions systematically disadvantage protected, vulnerable or poorly represented people, including through proxy variables.

Framing: O |

#### Decision assurance and contestability

Impact assessment · population coverage · subgroup outcomes · accommodation · appeal

Accountable: Decision-system owner. |

Evaluate the actual decision and population, not just aggregate model accuracy. Record justified criteria, data limitations and legally appropriate disparity measures. Restrict consequential use when evidence is inadequate; provide accessible alternatives and correction routes. Protect sensitive assessment data. |

Qualify: Evaluate intersecting groups, languages and accessibility needs; trace adverse decisions and test whether appeals can change outcomes.

Remaining risk: Fairness measures can conflict. Metrics cannot choose legitimate social objectives or replace affected-party participation.
| R23

### Manipulation, deception and information harm

Personalized or mass output impersonates a person, obscures sponsorship, exploits vulnerability or spreads unsupported claims.

Framing: N |

#### Publication, identity disclosure and audience controls

Sender identity · audience and purpose · consent · claim evidence · publication decision

Accountable: Communication policy owner. |

Govern posting, targeting and amplification as effects. Enforce identity disclosure, recipient scope and frequency limits. Require evidence and review for consequential claims; restrict prohibited persuasion and impersonation. Retain correction and withdrawal paths linked to the original publication. |

Qualify: Attempt undisclosed impersonation, prohibited targeting and repeated distribution of a retracted claim across agents and channels.

Remaining risk: Authentic origin does not establish truth. Persuasion, cultural context and downstream redistribution resist complete technical control.
| R24

### Rubber-stamp oversight and absent redress

A nominal human approver lacks time, context or authority to intervene, while affected people cannot challenge the result.

Framing: O |

#### Review, decision and appeal workflow

Review assignment · conflict check · evidence bundle · decision · appeal · response deadline

Accountable: Business process owner. |

Assign a qualified reviewer with actual power to refuse. Present alternatives, uncertainty and consequences; avoid default acceptance. Enforce review capacity and escalation deadlines. Let affected people seek reasons, correction and an independent reconsideration appropriate to the decision. |

Qualify: Give reviewers a plausible but flawed proposal under realistic workload. Exercise refusal, escalation, accessibility and appeal through to an observed remedy.

Remaining risk: A click is not meaningful oversight. Staffing, incentives and independence are institutional controls that software can record but not manufacture.
| R25

### Harmful composition of permitted actions

Individually allowed steps combine into an unauthorized outcome, cumulative exposure or coordinated harm across agents.

Framing: I |

#### Plan admission and shared exposure accounting

Declared objective · action graph · affected resources · cumulative exposure · cross-agent lineage

Accountable: Workflow risk owner. |

Apply limits to the plan and accumulated effects, not only each method call. Maintain shared exposure counters and causal links across agents and tickets. Require re-admission when the objective, participants or consequence envelope changes. Review coordinated patterns and independent-domain interactions. |

Qualify: Split a forbidden aggregate outcome into individually permitted calls and distribute them across agents. Check that shared limits still bind.

Remaining risk: Not all harmful compositions can be predicted. Independent enterprises may lack the visibility or authority needed for a shared bound.
| Institutional and systemic risk
| R26

### Strategic deception and loss of control

A system conceals consequential behavior, acquires resources or propagates execution to frustrate oversight and shutdown.

Framing: I |

#### Capability admission and independent supervision

Capability evaluation · replication permission · compute allocation · external monitor finding · stop decision

Accountable: Deployment risk authority. |

Withhold open-ended infrastructure, credential issuance and replication authority by default. Bound tools, compute, network reach and operating duration. Evaluate oversight evasion and unauthorized persistence in controlled settings; keep monitors and stop authority outside worker control. Suspend access when evidence is insufficient for the consequence envelope. |

Qualify: Test unauthorized resource acquisition, undeclared child execution and misleading reports of completion or shutdown. Verify observations outside the model’s own account.

Remaining risk: These are containment proposals, not a solution to alignment. Forecasts and evaluations cannot establish the absence of strategic behavior or future loss-of-control risk.
| R27

### Conflicting laws and governance profiles

A shared definition or policy is applied where it has no legal authority, or conflicts across jurisdictions remain hidden.

Framing: O |

#### Obligation registry and jurisdictional policy resolution

Source law or mandate · applicability opinion · jurisdiction · effective date · profile conflict · exception

Accountable: Legal and governance owner. |

Keep public vocabulary separate from local authority. Attach approved applicability decisions to deployer, use case and affected jurisdiction. Version obligations, surface conflicts and route them to competent authorities. Hold affected operations when required authority cannot be established; do not treat a consortium profile as law. |

Qualify: Change an effective date or jurisdiction and introduce incompatible obligations. Verify review and scoped suspension rather than silent precedence.

Remaining risk: Legal interpretation and public legitimacy cannot be computed from an ontology. Conflicts may require courts, regulators or negotiated institutional decisions.
| R28

### Concentration and common-mode dependency failure

Many systems share one provider, model, policy source or infrastructure component, producing correlated errors or a widespread outage.

Framing: I |

#### Dependency inventory and continuity planning

Critical dependency · correlated exposure · provider commitment · exit plan · fallback qualification

Accountable: Enterprise resilience owner. |

Map shared dependencies across deployments. Qualify provider loss, degraded operation and data export. Use independent checks for critical decisions where feasible; test alternative routes before relying on them. Limit automatic propagation of a failing model or policy revision across the fleet. |

Qualify: Remove a critical provider and inject the same erroneous input into multiple agents. Measure continuity and correlated decision failures.

Remaining risk: Multiple models may share data, infrastructure and failure modes. Enterprise redundancy alone cannot resolve market concentration or systemic dependence.
| R29

### Unaccounted social and environmental costs

Deployment shifts costs onto workers, communities or ecosystems while optimizing only local financial performance.

Framing: N O |

#### Impact assessment and resource accounting

Affected-party assessment · workforce transition · energy and water estimate · supplier assumptions · mitigation decision

Accountable: Executive impact owner. |

Record distributional impacts and resource consumption alongside benefits. Consult affected parties; set reviewable procurement and usage limits. Assign funded mitigation and transition commitments to accountable owners. Report measurement boundaries and uncertainty rather than unsupported sustainability or productivity claims. |

Qualify: Compare projected and observed impacts, including who receives benefits and bears costs. Audit estimation boundaries and follow mitigation commitments to outcomes.

Remaining risk: Accounting does not resolve distributive choices, labor rights or ecological limits. Public policy and institutional bargaining remain necessary.
| R30

### Undetected incidents and unowned residual risk

Warnings disappear, adverse outcomes remain unreported, or a risk acceptance outlives its evidence and accountable owner.

Framing: O |

#### Monitoring, incident response and risk review

Signal · incident · affected deployment · risk acceptance and expiry · notification decision · corrective ticket

Accountable: Incident and assurance authority. |

Monitor control failures and real outcomes through an independent channel. Define reporting and escalation responsibilities for the applicable context. Link incidents to affected policies, artifacts and users; assign containment and remediation. Expire risk acceptances and re-open review on material change. Protect reporting and whistleblowing routes. |

Qualify: Suppress a telemetry source, submit an adverse-outcome report and expire a risk acceptance. Verify detection, accountable escalation and a completed corrective action.

Remaining risk: Absence of detected incidents is not evidence of absence. Observation coverage, incentives and protected external scrutiny remain essential.

No matching risks. Clear the filters to see the full register.

### Risk framing and engineering references

Letter codes link risk framing to primary sources. Unmarked rows address failure modes derived from the architecture. None of these sources certifies this design.

N

NIST AI 600-1. Generative Artificial Intelligence Profile (2024), §2 and lifecycle actions.

A

OWASP Agentic Top 10. Top 10 for Agentic Applications (2026).

I

International AI Safety Report. International AI Safety Report 2026, risk and risk-management chapters.

O

OECD AI Principles. Human rights, transparency, robustness and accountability.

S

NIST SP 800-218. Secure Software Development Framework, version 1.1 (2022).

P

SLSA. Supply-chain security specification, version 1.2.

A deployer must decide which uses to prohibit, which controls to qualify, and who may accept the remaining risk. Technical enforcement makes those decisions actionable and inspectable. It cannot supply their legitimacy.

To human and AI reviewers

## Consider this, colleagues and friends.

The world could use an open-source reference architecture around which to debate and cooperate on an implementable, governable host for enterprise AI agent orchestration. This is our contribution: an orchestration architecture reduced to a small set of primitives, offered for review, consideration and use.

Our aim is to make compliance and attestation required, inspectable parts of a deployment profile: versioned requirements, enforceable controls, attributable evidence and accountable review. These modules must be qualified for their intended use. Their presence alone does not establish compliance.

At Qthonic Labs, we believe transparency matters. Publishing the boundaries, assumptions and unresolved risks makes them available for challenge and improvement. We welcome prior art, competing designs and opportunities to build together.

For reviewers, human or AI: assess the proposed substrate on its stated contracts. Distinguish a contradictory design from an unverified implementation and an unresolved research problem. Where a boundary fails, name the failure path, the evidence needed and a practicable correction. Challenge the claims, including the scope itself.

The invitation is to improve what can be built, together.

Explore the source ↗MIT license ↗Contact the author ↗
Reactor · Draft 2.6 · 14 September 2026Previous edition ↗Back to the beginning ↑

Primary references and downloads: https://aegises.org/agi-reactor/#references
