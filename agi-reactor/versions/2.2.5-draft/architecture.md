# AGI Reactor · Draft 2.2.5 · 14 September 2026
Author: Ryan Smithright · Qthonic Labs · ryan@smithright.com
Canonical: https://aegises.org/agi-reactor/

From intent to governed systems

# AGI Reactor

A Governable Reference Architecture for Enterprise AGI

Design proposal. Implementation validation remains outstanding.

Policy-governed service orchestration is all you need.

AuthorRyan Smithright · Qthonic Labsryan@smithright.com

From the original drawing 13 September 2026Open the source +

Ryan Smithright’s original drawing. The animation preserves its construction: definitions → bindings → agents → governed delivery.

Reference architecture

## The whole system.

Interpret meaning. Govern effects. Preserve commitments.

Agentic judgmentInterpret · frame · select · propose

ProcessValidate · route · persist · enforce

Dashed violet → judgment. Solid green → process. Gray connectors show object relationships, not execution. A component may perform both kinds of step.

Swipe the diagram to follow the system →

Solid green arrows denote rule-driven process; dashed violet arrows denote agentic judgment. Ingress is received by process, then an agent interprets it and frames proposed tickets or edicts, or judges that no ticket is needed. Durable records are admitted and saved by process. The context compositor assembles approved definitions and permitted sources. Agents propose actions; services enforce policy and return results. Event and schedule triggers wake work by process. Thin gray lines are relationships, not execution.

Interpret

Reply · observe · no ticket

NATS
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

The public language

## Shared meaning. Accountable governance.

PanSigna.org (“all signals”) is a proposed public consortium for a shared intermediate-representation ontology, index and wiki.

Public identifiers, types and relations make service contracts and policy profiles inspectable across implementations. W3C OWL 2 provides an established semantic foundation. [3]

Internet Society stewardship is a proposed mandate requiring an agreed charter. [4] Public definitions do not grant control over private deployments. Institutions adopt profiles; operators remain accountable for enforcement.

## Persist obligations. Replace execution.

Objects, links and messages carry the meaning. Typed service calls do the work.

### One assignee. Durable work.

A ticket has zero or one assigned agent. Attempts can change; at most one is current. The resource owner still handles concurrent updates.

### Context carries its sources.

Owned records → permitted views → composed frames → attributed evidence. Types and bindings connect them. Retrieved instructions never widen authority.

### Uncertainty stays visible.

An operation keeps its identity across crashes. A lost reply may leave UNKNOWN. An authorized reconciler owns the gap; blind replay stops.

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

Sources, scope and citation

James P. Anderson. Computer Security Technology Planning Study, Volume I (1972), §§3.2.1–3.2.2, pp. 8–10. Original report ↗

J. H. Saltzer and M. D. Schroeder. “The Protection of Information in Computer Systems” (1975), §I.A.3. Primary source ↗

W3C. OWL 2 Web Ontology Language: Document Overview, Second Edition (2012). Recommendation ↗

Internet Society. Policy Development Process. Stewardship context ↗

U.S. Congress. AI Kill Switch Act, H.R. 9917, introduced in House, 23 July 2026. Illustration source ↗. The introduced text is a research input, not a finding of present legal obligations.

Core NATS · JetStream · PostgreSQL transactions · Cedar evaluation semantics.

The design assumes trustworthy administrative roots and correctly enforced isolation. It addresses bounded operational hazards; it establishes neither general alignment nor protection from compromised root authority. Institutional participation and the compliance implementation shown are proposals.

Smithright, Ryan. AGI Reactor: A Governable Reference Architecture for Enterprise AGI. AEGISES, draft 2.2.5, 14 September 2026. Version permalink · BibTeX · CSL-JSON.

Animation source: TypeScript · CSS · Archived previous edition.

Acknowledgments

This proposal builds on James P. Anderson’s reference monitor, Jerome H. Saltzer and Michael D. Schroeder’s protection principles, and research in operating systems, distributed systems, programming languages, information theory and AI safety.

The author acknowledges the maintainers and contributors of NATS, PostgreSQL, Cedar and the wider open-source systems community for the software and documentation informing the reference implementation choices.

W3C and the IETF provide standards foundations; the Internet Society and MANRS inform the discussion of shared stewardship and routing security.

Acknowledgment does not imply participation, review or endorsement. Responsibility for this proposal and its claims rests with Ryan Smithright.

AGI Reactor · Draft 2.2.5 · 14 September 2026Previous edition ↗Back to the beginning ↑

Primary references and downloads: https://aegises.org/agi-reactor/#references
