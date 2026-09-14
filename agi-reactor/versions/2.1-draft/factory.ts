// The factory is an explanation, not a live agent or deployment controller.
type Phase = { title: string; detail: string; ticket: string; code: string; gate: string };
const phases: Phase[] = [
 {title:'One dictation. Two durable commitments.',detail:'“Design and implement Compliance for the AI Kill Switch Act.” becomes a spike ticket. Monthly leadership review becomes a standing edict.',ticket:'Accepted · one assignee',code:'Awaiting research and context',gate:'Admission required'},
 {title:'Bind the right knowledge and rules.',detail:'The spike resolves the bill text, status and applicability. Policy, control templates and assurance examples bind to the task; the edict defines the continuing review.',ticket:'Research → implementation',code:'Sources and requirements linked',gate:'Rules remain separately governed'},
 {title:'Compose the agent’s working frame.',detail:'The compositor assembles the brief, verified sources, relevant skills and pending work. Legal, security, engineering and the accountable AI owner are proposed review roles.',ticket:'Working context linked',code:'Working frame composed',gate:'Context does not grant authority'},
 {title:'Produce a control candidate.',detail:'The agent drafts service code, tests and requirement mappings. News feeds a sourced AI Compliance News Report; findings can create linked follow-up tickets.',ticket:'Candidate → review',code:'Control + tests + source mapping',gate:'Candidate awaits admission'},
 {title:'Check the work. Enforce the boundary.',detail:'The illustration admits a reviewed candidate only within its policy and release scope. A denied caller cannot cross the same boundary. Actual compliance needs qualified controls and evidence.',ticket:'Review and admission',code:'Candidate held at service boundary',gate:'Illustrated admission: permitted'},
 {title:'Deliver now. Keep reviewing.',detail:'A governed release can deliver the control. The edict continues as a monthly review of the AI Compliance News Report, with an owner, the right leaders and linked decisions.',ticket:'Result linked · review due',code:'Candidate and review plan delivered',gate:'Illustrated admission: permitted'}
];
const notes: Record<string,[string,string]> = {
 chat:['Dictation','The original words remain attributable. One message can create both owned work and enduring direction.'],
 ticket:['Spike ticket','One accountable agent investigates scope and uncertainty, then coordinates linked implementation work. Acceptance must include a source-to-control mapping and evidence.'],
 edict:['Standing edict','“Get the right leaders together monthly to review your AI Compliance News Report.” Its owner, participants, reporting scope and decision records stay explicit.'],
 definitions:['Reusable definitions','Policies constrain action. Templates supply structure. Examples supply precedent. Definitions are versioned and bound to the work; guidance cannot silently become authority.'],
 bindings:['Typed bindings','A binding connects an exact definition to its scope. Skills and agent profiles compose reusable behavior; policy bindings remain enforceable at service boundaries.'],
 context:['Other permitted context','Enterprise systems, prior findings, current obligations and source revisions are resolved through their owning services. A projection remains attributable to its sources.'],
 compositor:['Context compositor','Intent, acceptance, skills, applicable constraints and pending effects become one bounded working frame. The frame informs reasoning; it grants no capability.'],
 agent:['Replaceable agent execution','One assignee owns the ticket. Historical attempts may change. Current custody and resource-level revision checks govern new effects.'],
 code:['Control candidate','The code is an illustrative service contract for scoped halt and resume. It is not an implementation of H.R. 9917 or a legal-compliance determination.'],
 gate:['Independent enforcement','The owning service checks caller, policy, budget, revision and operation custody. Stop and resume require explicit authority. Refusal prevents the effect, even if a model asks for it.'],
 delivery:['Delivery and continuing review','A qualified release preserves a hot fallback. The review routine follows the edict: sourced report → accountable leaders → recorded decisions → follow-up tickets. No meeting is scheduled by this animation.']
};
const q = <T extends HTMLElement>(s: string): T => { const el = document.querySelector<T>(s); if (!el) throw new Error(`Missing ${s}`); return el; };
const factory=q<HTMLElement>('#factory'), play=q<HTMLButtonElement>('#play'), progress=q<HTMLElement>('#progress');
const steps=Array.from(document.querySelectorAll<HTMLButtonElement>('[data-step]'));
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
let stage=0, elapsed=0, running=false, speed=1, previous=0, denied=false;
const duration=6500;
function render():void {
 const phase=phases[stage]; factory.dataset.stage=String(stage);factory.classList.toggle('running',running);factory.classList.toggle('paused',!running);factory.classList.toggle('denied',denied);
 q('#step-number').textContent=String(stage+1).padStart(2,'0');
 q('#step-title').textContent=denied && stage>=4 ? 'Policy refused. The effect stops here.' : phase.title;
 q('#step-detail').textContent=denied && stage>=4 ? 'This caller lacks the required authority. The service records refusal and preserves the ticket. The standing monthly-review edict remains; it grants no permission to bypass the gate.' : phase.detail;
 document.getElementById('ticket-label')!.textContent=phase.ticket;
 document.getElementById('code-label')!.textContent=phase.code;
 document.getElementById('gate-label')!.textContent=denied&&stage>=4?'REFUSED · no release':phase.gate;
 document.getElementById('delivery-label')!.textContent=denied&&stage>=4?'HELD':stage===5?'DELIVERED':'DELIVERY';
 q('#play-label').textContent=reduced.matches?'Next step':running?'Pause':stage===5?'Replay':'Run the factory';
 q('#play-icon').textContent=running?'Ⅱ':stage===5?'↺':'▶';
 play.setAttribute('aria-pressed',String(running));
 steps.forEach((button,index)=>{if(index===stage)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');});
 q('#run-state').textContent=denied&&stage>=4?'HELD':running?'RUNNING':stage===5?'COMPLETE':stage>0||elapsed>0?'PAUSED':'READY';
 q('#outcome').textContent=denied&&stage>=4?'Illustrated outcome: release refused.':'Illustration only · no model calls, meetings or deployments.';
}
function jump(next:number):void {stage=Math.max(0,Math.min(5,next));elapsed=0;running=false;render();updateProgress();}
function updateProgress():void {progress.style.width=`${((stage+(stage===5?1:elapsed/duration))/6)*100}%`;}
function tick(now:number):void {
 const delta=previous ? Math.min(now-previous,100) : 0;previous=now;
 if(running){elapsed+=delta*speed;if(elapsed>=duration){elapsed=0;if(stage<5){stage++;render();}else{running=false;render();}}updateProgress();}
 requestAnimationFrame(tick);
}
play.addEventListener('click',()=>{if(reduced.matches){jump(stage===5?0:stage+1);return;}if(stage===5&&!running){stage=0;elapsed=0;}running=!running;render();});
steps.forEach(button=>button.addEventListener('click',()=>jump(Number(button.dataset.step))));
q<HTMLSelectElement>('#speed').addEventListener('change',event=>{speed=Number((event.target as HTMLSelectElement).value);});
q<HTMLInputElement>('#denied').addEventListener('change',event=>{denied=(event.target as HTMLInputElement).checked;jump(4);});
const inspection=q('#inspection');let lastInspected:Element|null=null;
function inspect(key:string,origin:Element):void {const note=notes[key];if(!note)return;running=false;render();q('#inspect-title').textContent=note[0];q('#inspect-body').textContent=note[1];inspection.hidden=false;lastInspected=origin;q<HTMLButtonElement>('#close-inspection').focus();}
document.querySelectorAll<SVGElement>('[data-inspect]').forEach(el=>{el.addEventListener('click',()=>inspect(el.dataset.inspect!,el));el.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();inspect(el.dataset.inspect!,el);}});});
function closeInspection():void {inspection.hidden=true;(lastInspected as SVGElement|null)?.focus();}
q('#close-inspection').addEventListener('click',closeInspection);
q('#expand').addEventListener('click',()=>{const expanded=factory.classList.toggle('expanded');document.body.classList.toggle('scene-expanded',expanded);q('#expand').textContent=expanded?'Close view ↙':'Expand ↗';q('#expand').setAttribute('aria-expanded',String(expanded));});
q('#zoom').addEventListener('click',()=>{const pane=q('#scene-window');const zoomed=pane.classList.toggle('zoomed');pane.classList.toggle('fit',!zoomed);q('#zoom').textContent=zoomed?'Fit':'Zoom +';if(!zoomed)pane.scrollTo(0,0);});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(!inspection.hidden)closeInspection();if(factory.classList.contains('expanded'))q('#expand').click();}});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&running){running=false;render();}});
reduced.addEventListener('change',()=>{running=false;render();});
const bundle={kind:'illustrative-architecture-output',scenario:'AI Kill Switch Act compliance spike and monthly leadership review',status:'Proposed design; not legal advice, verified compliance or a live schedule',source:'https://www.govinfo.gov/app/details/BILLS-119hr9917ih',spike:{intent:'Design and implement Compliance for the AI Kill Switch Act.',acceptance:['Verify source, status, applicability and requirements','Map requirements to owned controls','Implement candidate and qualification specimens','Admit release through policy and hot-fallback stages']},edict:{intent:'And moving forward, get the right leaders together monthly to review your AI Compliance News Report.',cadence:'monthly',proposed_roles:['Legal','Security','Engineering','Accountable AI owner'],decision_record:'Report sources, findings, owner, decisions and linked follow-up tickets',activation:'Owner, actual participants and schedule require governed adoption'},code:`// Illustrative contract: implementation and qualification required.\nexport interface ComplianceControl {\n  suspend(request: {\n    operationId: string;\n    target: string;\n    expectedRevision: number;\n    reasonRef: string;\n  }): Promise<{ status: "refused" | "accepted" | "unknown"; evidenceRef: string }>;\n  resume(request: {\n    operationId: string;\n    target: string;\n    approvalRef: string;\n    expectedRevision: number;\n  }): Promise<{ status: "refused" | "accepted" | "unknown"; evidenceRef: string }>;\n}\n// The owning service supplies authentication, policy evaluation,\n// durable operation custody and independent enforcement.\n`};
q('#download').addEventListener('click',event=>{event.preventDefault();const link=document.createElement('a');const url=URL.createObjectURL(new Blob([JSON.stringify(bundle,null,2)],{type:'application/json'}));link.href=url;link.download='agi-reactor-compliance-factory-example.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
document.querySelectorAll<HTMLElement>('[data-jump]').forEach(el=>el.addEventListener('click',()=>jump(Number(el.dataset.jump))));
// Print the explanatory content even when it is normally disclosed on demand.
let printOpen:HTMLDetailsElement[]=[];
window.addEventListener('beforeprint',()=>{printOpen=Array.from(document.querySelectorAll<HTMLDetailsElement>('.details-stack details:not([open])'));printOpen.forEach(el=>el.open=true);});
window.addEventListener('afterprint',()=>{printOpen.forEach(el=>el.open=false);printOpen=[];});
render();updateProgress();requestAnimationFrame(tick);
// A hand-stepped specimen: durable ticket identity is separate from execution time.
const moments=[
 'Agent A researches requirements while Agent B inventories systems. Implementation waits for both accepted inputs.',
 'Requirements waits for a source. Agent A checkpoints it and drafts the news report. Agent B continues independently; no ticket changes assignee.',
 'Requirements resumes and is accepted; inventory is accepted too. Their dependency join makes implementation ready for its own assignment and admission.',
 'Alternate path: before acceptance, the requirements attempt is lost. After its lease expires and pending effects are reconciled, a new generation resumes under Agent A. Old-generation calls are fenced out; implementation remains blocked.'
];
const concurrency=document.querySelector<HTMLElement>('.concurrency-demo');
if(concurrency){
 const buttons=Array.from(concurrency.querySelectorAll<HTMLButtonElement>('button[data-moment]'));
 buttons.forEach(button=>button.addEventListener('click',()=>{
  const moment=Number(button.dataset.moment);concurrency.dataset.moment=String(moment);
  buttons.forEach(b=>{if(b===button)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});
  q('#moment-caption').textContent=moments[moment];
  document.getElementById('join-state')!.textContent=moment===2?'READY · admission required':'BLOCKED';
  concurrency.querySelector('.req-resume text')!.textContent=moment===3?'New generation → resume':'Resume → evidence';
 }));
}
