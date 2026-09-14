from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/states.json').read_text())
names={'targeted':'Targeted harm / content','sectoral':'Sector / interaction safeguards','rights':'Consumer decision rights','institutional':'Public institutions / programs','lifecycle':'Structured accountability','unclassified':'Unclassified / proposal'}
types={'primary':'Primary source','mixed':'Mixed verification','secondary':'Secondary verification','none':'Research gap'}
rows=[]
for s in data['states']:
    sources=f'<a href="{escape(s["source_url"],quote=True)}">{escape(s["instrument"])} <span aria-hidden="true">↗</span></a>'
    for src in s['additional_sources']:sources+=f'<a href="{escape(src["url"],quote=True)}">{escape(src["title"])} <span aria-hidden="true">↗</span></a>'
    rows.append(f'''<article class="state-record" id="state-{s['code']}" data-pathway="{s['pathway']}"><div class="state-identity"><span class="state-code {s['pathway']}">{s['code']}</span><h3>{escape(s['name'])}</h3><span class="record-pathway">{names[s['pathway']]}</span></div><div class="state-evidence"><div class="record-meta"><span class="status {s['status']}">{s['status'].capitalize()}</span><span>{types[s['source_type']]}</span></div><p>{escape(s['claim'])}</p><p class="record-boundary"><strong>Boundary.</strong> {escape(s['boundary'])}</p><p class="implementation"><strong>Implementation evidence:</strong> {escape(s['implementation'])}.</p><div class="record-sources">{sources}</div></div></article>''')
page=(ROOT/'research/article.html').read_text().replace('{{STATE_LEDGER}}','\n'.join(rows))
figs=[('01-evidence-ladder','Maturity requires distinct evidence at each stage. The examples establish limited observations for named mechanisms; they do not score entire states.'),('02-architecture-landscape','Selected instruments positioned by legal reach and accountability mechanism. Categorical placements are editorial judgments, not measured scores. Relevant sources are linked in the state ledger.'),('03-state-pathways','An equal-area cartogram of selected legislative anchors. Category keys are not rankings. Alabama and Alaska use mixed verification; Idaho uses secondary verification. Missouri and DC remain unclassified.'),('04-domain-matrix','Eight analytical domains. A filled cell means an enacted primary-supported anchor in this corpus; an open circle means mixed or secondary verification. A dash means not assessed, never no law.'),('05-obligation-horizon','A selected timeline of effective dates, an adoption deadline and a reporting start. The shaded area lies after the September 14, 2026 observation date. See the ledger for source instruments.'),('06-obligation-to-control','Suggested evidence objects translate legal mechanisms into operating controls. These suggestions are analytical, not additional statutory requirements. Scope and exceptions must be checked against the law.')]
for i,(name,caption) in enumerate(figs,1):
    page=page.replace('{{FIGURE_'+str(i).zfill(2)+'}}',f'''<figure id="figure-{i}" class="analytical-figure"><div class="figure-top"><span>FIGURE {str(i).zfill(2)}</span><a href="assets/{name}.svg" download>Download SVG ↗</a></div><span class="mobile-figure-hint">Swipe to read the figure · tap to open at full size</span><a class="figure-image" href="assets/{name}.svg" aria-label="Open figure {i} at full size"><img src="assets/{name}.svg" alt="{escape(caption)}" loading="{'eager' if i==1 else 'lazy'}" width="1200" height="{[640,870,1020,1220,790,790][i-1]}"></a><figcaption><b>{str(i).zfill(2)} /</b> {caption}</figcaption></figure>''')
(ROOT/'index.html').write_text(page)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style','nav','form'):self.skip+=1
  if t in ('p','h1','h2','h3','li','article','section','figcaption'):self.out.append('\n\n')
  if t=='a' and not self.skip:
   self.link=dict(a).get('href','')
  if t=='br':self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','nav','form'):self.skip-=1
  if t=='a' and not self.skip and getattr(self,'link','').startswith('https://'):self.out.append(' ('+self.link+')')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
p=Text();p.feed(page)
import re
text=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',''.join(p.out))
(ROOT/'ai-legislation.txt').write_text(text.strip()+'\n')
with zipfile.ZipFile(ROOT/'assets/figures.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name,_ in figs:z.write(ROOT/'assets'/f'{name}.svg',f'{name}.svg')
print('Built static publication, plain text and SVG bundle.')
