"""Original, deterministic SVG figures. No inferred numeric maturity scores."""
from pathlib import Path
import json, html, textwrap
from datetime import date
ROOT=Path(__file__).resolve().parents[1]
states=json.loads((ROOT/'data/states.json').read_text())['states']
INK='#15313d'; MUTED='#597078'; TEAL='#087e80'; GOLD='#b47a32'; LINE='#d5dfdd'; PAPER='#f5f6f0'; NAVY='#102c39'
COLORS={'targeted':'#7b8290','sectoral':'#d4a45d','rights':'#5c9ba1','institutional':'#a0b7ae','lifecycle':'#43c1b5','unclassified':'#344956'}
NAMES={'targeted':'Targeted harm / content','sectoral':'Sector / interaction safeguards','rights':'Consumer decision rights','institutional':'Public institutions / programs','lifecycle':'Structured accountability','unclassified':'Unclassified / proposal'}
NUM={'targeted':'1','sectoral':'2','rights':'3','institutional':'4','lifecycle':'5','unclassified':'?'}
class SVG:
 def __init__(self,w,h,title,desc,dark=False):
  self.w=w;self.h=h;self.ink='#f3f5ee' if dark else INK;self.muted='#b4c7ca' if dark else MUTED;self.rule='#35505b' if dark else LINE
  self.p=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><style>text{{font-family:Inter,Arial,sans-serif}}.serif{{font-family:Georgia,serif}}a:focus rect{{stroke:#fff;stroke-width:4}}</style>',f'<rect width="{w}" height="{h}" fill="{NAVY if dark else PAPER}"/>']
 def text(self,x,y,t,size=18,color=None,weight=400,anchor='start',cls=''):
  self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or self.ink}" font-weight="{weight}" text-anchor="{anchor}" class="{cls}">{html.escape(str(t))}</text>')
 def wrap(self,x,y,t,width=45,size=18,color=None,leading=26,weight=400):
  for i,line in enumerate(textwrap.wrap(t,width=width)): self.text(x,y+i*leading,line,size,color,weight)
 def rect(self,x,y,w,h,fill,stroke='none',rx=0): self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
 def line(self,x1,y1,x2,y2,color=None,dash='',width=1): self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or self.rule}" stroke-width="{width}" stroke-dasharray="{dash}"/>')
 def dot(self,x,y,r=6,fill=TEAL,stroke='none'):self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 def header(self,n,title,sub):
  self.text(40,42,f'AEGISES   /   STATE AI LEGISLATIVE MATURITY   /   FIGURE {n}',12,self.muted,600)
  self.text(40,86,title,32,weight=500,cls='serif'); self.text(40,119,sub,16,self.muted)
 def footer(self,t):
  self.line(40,self.h-55,self.w-40,self.h-55);self.text(40,self.h-28,t,13,self.muted);self.text(self.w-40,self.h-28,'14 SEP 2026 · v1.0',12,self.muted,anchor='end')
 def save(self,name):
  self.p.append('<metadata>'+html.escape(json.dumps({'publication':'https://aegises.org/ai-legislation/','as_of':'2026-09-14','sources':[{'state':v['code'],'url':v['source_url']} for v in states]}))+'</metadata>')
  (ROOT/'assets'/f'{name}.svg').write_text('\n'.join(self.p+['</svg>']))

s=SVG(1200,640,'Maturity requires a chain of evidence','Six evidence stages, from proposal through measured outcomes. Examples establish limited stages for named instruments, not scores for whole states.',True)
s.header('01','From a law on the books to a working institution','An evidence ladder. Each transition needs a different kind of proof.')
steps=[('00','Proposed','Bill text and current status','A prospective date is not an enacted duty.'),('01','Enacted','Final act and signing record','Identify the exact version and covered actors.'),('02','Effective','Provision-level start date','An operative duty can still lack delivery evidence.'),('03','Implemented','Published rule, form or system','An available artifact does not prove its use.'),('04','Exercised','Attributable operational record','Show actual reviews, notices or remedies.'),('05','Evaluated','Outcomes and a credible baseline','Test effectiveness, cost and uneven impacts.')]
for i,(num,title,proof,note) in enumerate(steps):
 x=40+i*188;y=230-i*13
 s.rect(x,y,177,260,'#173643');s.rect(x,y,177,4,'#43c1b5' if i<4 else '#d4a45d')
 s.text(x+16,y+39,num,18,'#7fb1b0');s.text(x+16,y+73,title,21,weight=600)
 s.wrap(x+16,y+108,proof,18,16,'#f3f5ee',23);s.wrap(x+16,y+174,note,20,14,'#b4c7ca',21)
s.text(40,539,'OBSERVED IN THIS REVIEW',12,'#43c1b5',600)
s.text(40,568,'CA reporting surface · CT published inventory · OH model policy: implementation artifacts',17)
s.text(40,596,'UT program operation: agency-reported. Comparative outcomes: not evaluated in this edition.',15,'#b4c7ca')
# Compact bespoke footer because the last evidence note takes the standard footer area.
s.save('01-evidence-ladder')

s=SVG(1200,870,'Legislative architecture landscape','A categorical three-by-three comparison of selected instruments. Columns identify reach; rows identify accountability mechanisms. Positions are editorial categories, not measured scores.')
s.header('02','Different laws mature along different paths','Selected instruments, classified by legal reach and accountability mechanism. No numeric ranking.')
x0=236;y0=196;cw=301;rh=171
for j,t in enumerate(['Public operations','Defined use / actor class','Cross-sector decisions']):s.text(x0+j*cw+cw/2,170,t,17,weight=600,anchor='middle')
labels=[('Ongoing process','Frameworks, reporting,','institutional review'),('Rights & review','Notice, recourse,','human judgment'),('Specific guardrails','Prohibited conduct,','disclosure, identity')]
for i,(a,b,c) in enumerate(labels):
 y=y0+i*rh;s.text(40,y+50,a,19,weight=600);s.text(40,y+80,b,15,MUTED);s.text(40,y+103,c,15,MUTED)
 for j in range(3):s.rect(x0+j*cw+4,y+4,cw-8,rh-8,'#fff',LINE)
items=[(0,0,'CT · MD · VT','Government inventories','and oversight duties'),(0,1,'CA · NY','Frontier frameworks','NY: effective Jan 2027'),(0,2,'—','No specimen assigned','in this selected comparison'),(1,0,'NH','Public-sector AI','oversight safeguards'),(1,1,'AZ · IL','Medical review /','employment protections'),(1,2,'CO · MN · VA','Decision rights / recourse','CO: effective Jan 2027'),(2,0,'TX [public use]','Specified government','AI restrictions'),(2,1,'ME · WA · TN','Chatbot disclosure /','companion safety / likeness'),(2,2,'TX [covered uses]','Specified prohibitions','and enforcement')]
for r,c,title,l1,l2 in items:
 x=x0+c*cw+22;y=y0+r*rh+45
 s.text(x,y,title,23,TEAL,600);s.text(x,y+37,l1,17);s.text(x,y+64,l2,15,MUTED)
s.text(40,756,'REACH IS NOT BREADTH OF PROTECTION',12,TEAL,600)
s.wrap(40,785,'A frontier law can have deep duties for a narrow developer class. A privacy law can reach many businesses but cover only particular consumer decisions. Texas appears twice because one statute contains different mechanisms.',135,16,MUTED,24)
s.footer('Sources: state ledger and selected statutory texts. Placement: AEGISES editorial assessment.')
s.save('02-architecture-landscape')

positions={'AK':(0,0),'ME':(11,0),'WI':(5,1),'VT':(10,1),'NH':(11,1),'WA':(0,2),'ID':(1,2),'MT':(2,2),'ND':(3,2),'MN':(4,2),'IL':(5,2),'MI':(6,2),'NY':(9,2),'MA':(10,2),'OR':(0,3),'NV':(1,3),'WY':(2,3),'SD':(3,3),'IA':(4,3),'IN':(5,3),'OH':(6,3),'PA':(7,3),'NJ':(8,3),'CT':(9,3),'RI':(10,3),'CA':(0,4),'UT':(1,4),'CO':(2,4),'NE':(3,4),'MO':(4,4),'KY':(5,4),'WV':(6,4),'VA':(7,4),'MD':(8,4),'DE':(9,4),'AZ':(1,5),'NM':(2,5),'KS':(3,5),'AR':(4,5),'TN':(5,5),'NC':(6,5),'SC':(7,5),'DC':(8,5),'OK':(3,6),'LA':(4,6),'MS':(5,6),'AL':(6,6),'GA':(7,6),'HI':(0,7),'TX':(3,7),'FL':(8,7)}
assert set(positions)=={x['code'] for x in states}
s=SVG(1200,1020,'Fifty states, several legislative pathways','Equal-area tile cartogram. Each state is colored by its selected anchor pathway, not its full legal portfolio. Missouri proposal and DC research gap are unclassified. Numbers are category keys, not maturity scores.',True)
s.header('03','A national mosaic, not a league table','Representative anchors for all 50 states; the District of Columbia is shown separately.')
for st in states:
 col,row=positions[st['code']];x=43+col*93;y=165+row*80;p=st['pathway']
 s.p.append(f'<g><title>{html.escape(st["name"]+": "+NAMES[p]+". "+st["instrument"])}</title>')
 s.rect(x,y,84,70,COLORS[p],stroke='#728691' if p=='unclassified' else 'none',rx=2)
 fg='#f3f5ee' if p=='unclassified' else '#102c39'
 s.text(x+12,y+32,st['code'],25,fg,600);s.text(x+69,y+55,NUM[p],14,fg,600,anchor='end')
 if st['source_type'] in ['mixed','secondary']:s.text(x+12,y+56,'†',16,fg)
 s.p.append('</g>')
s.text(890,690,'DC shown',14,'#b4c7ca');s.text(890,712,'separately',14,'#b4c7ca')
for i,p in enumerate(NAMES):
 x=43+(i%2)*565;y=848+(i//2)*37;s.rect(x,y-17,22,22,COLORS[p],stroke='#728691' if p=='unclassified' else 'none');s.text(x+34,y,NUM[p]+'  '+NAMES[p],17)
s.footer('Category numbers are keys, not scores. † Mixed / secondary verification. Selected corpus; see ledger.')
s.save('03-state-pathways')

domains=[('decisions','Decisions'),('frontier','Frontier'),('interaction','Chatbots'),('health','Health'),('employment','Jobs'),('media','Media'),('public','Public'),('infrastructure','Infra.')]
s=SVG(1200,1220,'State-by-domain evidence matrix','Eight domains, 50 states and DC. Filled circle means primary-supported enacted anchor, open circle means mixed or secondary verification, P means proposal, dash means not assessed. Counts measure this corpus only.')
s.header('04','Where the selected evidence sits','One filled cell establishes an anchor in this corpus. A dash does not establish an absence of law.')
for panel,subset in enumerate([states[:26],states[26:]]):
 x=40+panel*580
 for j,(_,label) in enumerate(domains):s.text(x+111+j*58,166,label,12,MUTED,600,anchor='middle')
 for i,st in enumerate(subset):
  y=207+i*33
  if i%2==0:s.rect(x,y-23,551,32,'#eaf0ec')
  s.text(x+10,y,st['code'],17,weight=600)
  for j,(key,_) in enumerate(domains):
   cx=x+111+j*58
   if key in st['domains']:
    if st['status']=='proposal':s.text(cx,y,'P',15,GOLD,600,anchor='middle')
    elif st['source_type'] in ['mixed','secondary']:s.dot(cx,y-5,6,PAPER,TEAL)
    else:s.dot(cx,y-5,6)
   else:s.text(cx,y,'—',13,'#8da09f',anchor='middle')
s.dot(55,1100,6);s.text(72,1105,'Enacted · primary',16)
s.dot(307,1100,6,PAPER,TEAL);s.text(324,1105,'Enacted · mixed / secondary',16)
s.text(690,1105,'P',16,GOLD,600);s.text(712,1105,'Proposal',16)
s.text(870,1105,'—',16,MUTED);s.text(896,1105,'Not assessed',16)
s.text(40,1141,'Media includes election integrity, likeness, intimate imagery and synthetic-content interests.',15,MUTED)
s.footer('Sources: machine-readable state ledger. Coverage of this review is not coverage of each state’s law.')
s.save('04-domain-matrix')

s=SVG(1200,790,'Selected obligation dates','Timeline from January 2025 to August 2027. Observation cut is September 14, 2026. Effective dates and later reporting or adoption deadlines are distinct event types.')
s.header('05','The implementation horizon is uneven','Selected dates, tied to particular provisions. Enactment is not the same event as an obligation starting.')
start=date(2025,1,1);end=date(2027,8,1)
def tx(d):return 360+(date.fromisoformat(d)-start).days/(end-start).days*755
cut=tx('2026-09-14')
s.rect(cut,174,1115-cut,479,'#f0e6d2');s.line(cut,160,cut,650,GOLD,'5 5',2)
s.text(cut+12,153,'OBSERVATION CUT',12,GOLD,600)
for d,l in [('2025-01-01','JAN 2025'),('2026-01-01','JAN 2026'),('2027-01-01','JAN 2027')]:
 x=tx(d);s.line(x,174,x,650);s.text(x,689,l,14,MUTED,600)
events=[('IL · TX · RI','Selected laws take effect','2026-01-01','Effective'),('Arizona','Medical review requirement','2026-07-01','Effective'),('Ohio','School policy adoption','2026-07-01','Deadline'),('Colorado','Replacement decision framework','2027-01-01','Effective'),('New York','Amended frontier framework','2027-01-01','Effective'),('Washington','Companion-chatbot framework','2027-01-01','Effective'),('California','Companion-chatbot annual reporting','2027-07-01','Reporting starts')]
for i,(name,label,d,kind) in enumerate(events):
 y=208+i*63;x=tx(d);c=GOLD if d>'2026-09-14' else TEAL
 s.text(40,y,name,19,weight=600);s.text(40,y+24,label,14,MUTED)
 s.line(360,y+2,1115,y+2);s.dot(x,y+2,7,c);s.text(x-13,y-12,date.fromisoformat(d).strftime('%d %b %Y').lstrip('0'),14,c,600,anchor='end')
 s.text(x-13,y+27,kind,12,MUTED,anchor='end')
s.text(40,728,'Dates do not establish compliance, enforcement readiness or the status of every provision in a law.',16,MUTED)
s.footer('Sources: provision-level dates in the state ledger and article references.')
s.save('05-obligation-horizon')

s=SVG(1200,790,'From a legal duty to an accountable control','Four selected legal mechanisms mapped to responsible actors, operating actions, proposed evidence objects and redress or reporting routes. Suggested evidence objects are analytical translations, not additional statutory duties.')
s.header('06','Translate the statute into an accountable control','The practical unit: a scoped obligation, an owner, a witnessed action and a route for challenge.')
xs=[40,232,445,705,988];ws=[183,204,251,274,172]
for x,w,title in zip(xs,ws,['Legal mechanism','Responsible actor','Operating action','Suggested evidence','Challenge / reporting']):s.text(x,169,title,15,TEAL,600)
rows=[['CO · decisions','Covered developer / deployer','Document use; explain an adverse decision; enable human review.','Versioned documentation; notice receipt; review disposition.','Consumer review; Attorney General.'],['IL · employment','Covered employer','Give required notice and prevent discriminatory AI use.','Notice record; selection assessment; accountable decision owner.','Civil-rights complaint process.'],['CA · frontier','Covered frontier developer','Maintain applicable framework and submit required reports.','Published framework; version history; incident submission record.','State reporting; Attorney General.'],['OH · schools','Covered school governing body','Adopt an AI-use policy after the state model is issued.','Approved policy; adoption date; assigned school owner.','Public governance and oversight.']]
for i,row in enumerate(rows):
 y=194+i*120;s.rect(40,y,1120,111,'#fff',LINE)
 for j,txt in enumerate(row):s.wrap(xs[j]+12,y+31,txt,[17,20,27,29,18][j],16,TEAL if j==0 else INK,23,600 if j==0 else 400)
s.text(40,714,'Evidence objects are AEGISES implementation suggestions. Verify legal coverage, exceptions and procedure first.',15,MUTED)
s.footer('Sources: Colorado SB26-189; Illinois PA103-0804; California SB53; Ohio ORC3301.24.')
s.save('06-obligation-to-control')
print('Generated six SVG analytical figures.')
