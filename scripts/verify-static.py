"""Static integrity checks only; this does not claim browser/render verification."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit
import re,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
# Reuse the tiny parser without running the page generator.
ns={'__file__':str(ROOT/'scripts/build-site.py')}
exec((ROOT/'scripts/build-site.py').read_text().split('source=Parser')[0],ns)
Parser=ns['Parser'];Node=ns['Node']
names=['index.html','about.html','service.html','works.html','contact.html','privacy.html']
docs={name:Parser((ROOT/name).read_text()).root for name in names}
old=Parser((ROOT/'_v3.0-index.html').read_text()).root
checks=[]
def check(label,condition):
 checks.append({'check':label,'passed':bool(condition)})
 if not condition:print('FAIL:',label)
def norm(s):return re.sub(r'\s+','',unescape(s))
def domtext(n):return norm(n.text())
for name,doc in docs.items():
 ids=[n.attrs['id'] for n in doc.all() if 'id' in n.attrs]
 check(name+': unique IDs',len(ids)==len(set(ids)))
 check(name+': one h1',len(doc.all('h1'))==1)
 check(name+': noindex,nofollow',any(n.attrs.get('name')=='robots' and n.attrs.get('content')=='noindex,nofollow' for n in doc.all('meta')))
 check(name+': no dialogs',not doc.all('dialog'))
 check(name+': shared CSS/JS',any(n.attrs.get('href')=='css/style.css' for n in doc.all('link')) and any(n.attrs.get('src')=='js/main.js' for n in doc.all('script')))
 check(name+': favicons',len([n for n in doc.all('link') if n.attrs.get('rel') in ['icon','apple-touch-icon']])==3)
 for n in doc.all():
  for attr in ['href','src']:
   if attr not in n.attrs:continue
   url=urlsplit(n.attrs[attr])
   if url.scheme or url.netloc:continue
   target=ROOT/(url.path or name)
   check(name+': local '+n.attrs[attr],target.exists())
   if url.fragment and target.suffix=='.html':
    target_doc=docs.get(target.name)
    check(name+': anchor '+n.attrs[attr],target_doc is not None and bool(target_doc.all(id=url.fragment)))
 check(name+': reference is not linked','_v3.0-index.html' not in (ROOT/name).read_text())
 if name!='privacy.html':
  check(name+': active navigation',len([n for n in doc.all('a') if n.attrs.get('href')==name and n.attrs.get('aria-current')=='page'])==3)
# Full substantive dialog text is preserved, excluding obsolete dialog controls.
for id in ['detail-training','detail-aistaff']:
 previous=old.one(id=id);previous.remove(lambda n:n.tag=='form')
 check(id+': full original copy',domtext(previous)==domtext(docs['service.html'].one(id=id)))
previous=old.one(id='privacy');previous.remove(lambda n:'modal__head' in n.attrs.get('class','').split())
check('privacy: full original copy',domtext(previous)==domtext(docs['privacy.html'].one(id='privacy')))
check('FAQ: all eight original questions and answers',len(docs['service.html'].all('details'))==8 and [domtext(n) for n in old.all('details')]==[domtext(n) for n in docs['service.html'].all('details')])
for i in range(1,4):
 previous=old.one(id=f'case-{i}');current=docs['works.html'].one(id=f'case-{i}')
 check(f'case-{i}: original company and outcomes',domtext(previous.one('h3'))==domtext(current.one('h3')) and domtext(previous.one('dl'))==domtext(current.one('dl')))
 check(f'case-{i}: no old diagram',not current.all(cls='fig'))
 check(f'case-{i}: pending consent copy',domtext(current.one(cls='voice').one('p'))==norm('導入企業様からのコメントは、ご了承をいただいたものから順次掲載してまいります。'))
for id in ['issue-1','issue-2','issue-3']:
 i=int(id[-1])-1
 check(id+': original body',domtext(old.one(id=id).one(cls='slide__lead'))==domtext(docs['index.html'].one(id='issues').all(cls='card-copy')[i]))
for i,id in enumerate(['svc-training','svc-aistaff','svc-app']):
 for page in ['index.html','service.html']:
  check(page+': '+id+' original body',domtext(old.one(id=id).one(cls='slide__lead'))==domtext(docs[page].one(id='service').all(cls='card-copy')[i]))
check('hero: explicit three lines',len(docs['index.html'].one('h1').all('br'))==2)
check('philosophy: explicit two lines',len(docs['index.html'].one(id='philosophy').one('h2').all('br'))==1)
for n in docs['index.html'].all(cls='pillar'):
 check('pillar: two heading / three body lines',len(n.one('h3').all('br'))==1 and len(n.one(cls='card-copy').all('br'))==2)
check('removed top sections and copy',not any(term in docs['index.html'].text() for term in ['計算の例','AIがいる会社の、1日。','迷ったら、ここから','広げ方の順番','損']))
check('hero: no chips',not docs['index.html'].all(cls='hero__chips'))
css=(ROOT/'css/style.css').read_text()
colors=sorted(set(re.findall(r'#[0-9a-fA-F]{6}\b',css)))
radii=sorted(set(re.findall(r'border-radius:\s*([^;}]+)',css)))
check('CSS: only six approved colors',set(colors)=={'#FFFFFF','#EDF1F9','#327AFA','#0F0F11','#616267','#9798A1'})
check('CSS: only approved radii',set(radii)<={'4px','12px','16px','24px','32px','9999px'})
check('CSS: no gradients/shadows/extra color functions',not re.search(r'(?:box-shadow|text-shadow|gradient\(|rgba?\(|hsla?\()',css))
images=[]
for name in ['issue-01','issue-02','issue-03','philosophy','case-01','case-02','case-03','service-aistaff']:
 p=ROOT/'assets'/f'{name}.jpg';im=Image.open(p)
 item={'file':str(p.relative_to(ROOT)),'size':list(im.size),'bytes':p.stat().st_size,'format':im.format};images.append(item)
 check(name+': JPEG 1200x800 under 250KB',im.format=='JPEG' and im.size==(1200,800) and p.stat().st_size<250000)
for i in range(1,4):check(f'old case {i} retained',(ROOT/f'assets/_old-case-0{i}.jpg').exists())
report={'type':'static only — no browser rendering','checks':checks,'colors':colors,'radii':radii,'images':images,'reference_sha256':hashlib.sha256((ROOT/'_v3.0-index.html').read_bytes()).hexdigest()}
(ROOT/'verification/static-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'{sum(x["passed"] for x in checks)}/{len(checks)} static checks passed')
print('colors:',', '.join(colors));print('radii:',', '.join(radii))
if not all(x['passed'] for x in checks):raise SystemExit(1)
