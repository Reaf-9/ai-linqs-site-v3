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
  for attr in ['href','src','poster']:
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
# v3.2 requirements, checked against the supplied specification.
home=docs['index.html'];about=docs['about.html'];spec=(ROOT/'SPEC-v3.2.md').read_text()
video=home.one(id='hero').one('video')
check('hero: video attributes',all(k in video.attrs for k in ['autoplay','muted','loop','playsinline']) and video.attrs.get('preload')=='metadata' and video.attrs.get('aria-hidden')=='true')
check('hero: supplied media',video.attrs.get('poster')=='assets/hero-poster.jpg' and video.one('source').attrs.get('src')=='assets/hero.mp4')
check('philosophy: growth flow and pillar labels removed',not home.all(cls='growth-flow') and not any(n.all(cls='eyebrow') for n in home.all(cls='pillar')))
check('issues: removed explanatory copy','ひとつでも当てはまるなら、AIで変えられる余地があります。' not in home.one(id='issues').text())
sections=[n.attrs.get('id') for n in home.one('main').all('section')]
check('timing: immediately follows issues',sections[sections.index('issues')+1]=='timing')
timing=home.one(id='timing')
check('timing: explicit two heading lines',timing.one('h2').text()=='AIを入れるなら、いまです。' and len(timing.one('h2').all('br'))==1)
expected=''.join(re.search(r'- 本文（3 行）：\n(.*?)\n- CTA',spec,re.S).group(1).splitlines()).replace('  ','')
check('timing: verbatim body with three explicit lines',timing.one(cls='timing-body').text()==expected and len(timing.one(cls='timing-body').all('br'))==2)
check('timing: separate HTML badge',timing.one(cls='timing-mark').text()=='！')
check('timing: CTA',timing.one('a').text()=='LINEで無料相談' and 'data-line-cta' in timing.one('a').attrs)
flow=home.one(cls='contract-flow')
check('contract: heading and four rows',flow.one('h3').text()=='ご契約までの流れ' and len(flow.one('ol').all('li'))==4 and not home.one(id='reasons').all(cls='steps'))
expected_steps=re.findall(r'  [1-4]\. \*\*(.*?)\*\* ─ (.*)',spec)
for i,(node,(title,body)) in enumerate(zip(flow.all('li'),expected_steps),1):
 check(f'contract {i}: verbatim title and body',node.one('h4').text()==title and node.one('p').text()==body)
 check(f'contract {i}: image',node.one('img').attrs.get('src')==f'assets/step-0{i}.jpg')
check('about: no small philosophy label',not about.one(cls='section-head').all(cls='eyebrow'))
check('about: revised labels',[about.one(id=id).one(cls='slide__tag').text() for id in ['mission','vision','value']]==['Mission','Vision','大切にすること'])
check('about: revised note',about.one(cls='section-head').one(cls='slide__note').text()=='Mission・Vision・大切にすること')
rows=about.one(cls='company-table').all('tr')
check('about: company row order',[n.one('th').text() for n in rows]==['会社名','代表者','所在地','電話番号','事業内容'])
check('about: exact address and pending phone',rows[2].one('td').text()=='〒651-0094 兵庫県神戸市中央区琴ノ緒町7-11-1' and rows[3].one('td').text()=='準備中')
check('about: confirmation immediately before table','<!-- [要確認] 電話番号・設立年月・資本金などは確定後に追記 --><table' in (ROOT/'about.html').read_text())
css=(ROOT/'css/style.css').read_text()
colors=sorted(set(re.findall(r'#[0-9a-fA-F]{6}\b',css)))
radii=sorted(set(re.findall(r'border-radius:\s*([^;}]+)',css)))
check('CSS: only six approved colors',set(colors)=={'#FFFFFF','#EDF1F9','#327AFA','#0F0F11','#616267','#9798A1'})
check('CSS: only approved radii',set(radii)<={'4px','12px','16px','24px','32px','9999px'})
check('CSS: no gradients/shadows/extra color functions',not re.search(r'(?:box-shadow|text-shadow|gradient\(|rgba?\(|hsla?\()',css))
images=[]
for name in ['issue-01','issue-02','issue-03','philosophy','case-01','case-02','case-03','service-aistaff','timing','step-01','step-02','step-03','step-04']:
 p=ROOT/'assets'/f'{name}.jpg';im=Image.open(p)
 item={'file':str(p.relative_to(ROOT)),'size':list(im.size),'bytes':p.stat().st_size,'format':im.format};images.append(item)
 check(name+': JPEG 1200x800 under 250KB',im.format=='JPEG' and im.size==(1200,800) and p.stat().st_size<250000)
for i in range(1,4):check(f'old case {i} retained',(ROOT/f'assets/_old-case-0{i}.jpg').exists())
report={'type':'static only — no browser rendering','checks':checks,'colors':colors,'radii':radii,'images':images,'reference_sha256':hashlib.sha256((ROOT/'_v3.0-index.html').read_bytes()).hexdigest()}
(ROOT/'verification/static-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(f'{sum(x["passed"] for x in checks)}/{len(checks)} static checks passed')
print('colors:',', '.join(colors));print('radii:',', '.join(radii))
if not all(x['passed'] for x in checks):raise SystemExit(1)
