"""Build static v3.2 pages from the immutable v3.0 reference; no dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import copy, re
ROOT=Path(__file__).resolve().parent.parent
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Node:
 def __init__(self,tag='',attrs=(),children=None): self.tag,self.attrs,self.children=tag,dict(attrs),children or []
 def all(self,tag=None,cls=None,id=None):
  out=[]
  for c in self.children:
   if isinstance(c,Node):
    if (tag is None or c.tag==tag) and (cls is None or cls in c.attrs.get('class','').split()) and (id is None or c.attrs.get('id')==id): out.append(c)
    out+=c.all(tag,cls,id)
  return out
 def one(self,tag=None,cls=None,id=None): return self.all(tag,cls,id)[0]
 def text(self): return ''.join(c.text() if isinstance(c,Node) else ('' if c.startswith('<!--') else c) for c in self.children)
 def html(self):
  if not self.tag:return ''.join(c.html() if isinstance(c,Node) else c for c in self.children)
  attrs=''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
  return '<'+self.tag+attrs+'>'+('' if self.tag in VOID else ''.join(c.html() if isinstance(c,Node) else c for c in self.children)+'</'+self.tag+'>')
 def remove(self,pred):
  self.children=[c for c in self.children if not isinstance(c,Node) or not pred(c)]
  for c in self.children:
   if isinstance(c,Node): c.remove(pred)
class Parser(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False);self.root=Node();self.stack=[self.root];self.feed(s)
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in VOID:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
 def handle_entityref(self,s):self.handle_data('&'+s+';')
 def handle_charref(self,s):self.handle_data('&#'+s+';')
 def handle_comment(self,s):self.handle_data('<!--'+s+'-->')
source=Parser((ROOT/'_v3.0-index.html').read_text()).root
def get(id):return copy.deepcopy(source.one(id=id))
def text(id,tag=None,cls=None):
 n=get(id)
 return (n.one(tag,cls) if tag or cls else n).text().strip()
def html(id):return get(id).html()
def inner(n):return ''.join(c.html() if isinstance(c,Node) else c for c in n.children)
def lines(s):return '<br>'.join('<span class="phrase">'+x+'</span>' for x in s.split('|'))
def p(s,cls=''):return '<p'+(' class="'+cls+'"' if cls else '')+'>'+s+'</p>'
def btn(label,href,line=False):return f'<a class="btn" href="{href}"'+(' data-line-cta' if line else '')+'>'+label+'<span class="btn-dot" aria-hidden="true"></span></a>'
def cta():return btn('LINEで無料相談','contact.html#contact',True)
def photo(name,alt=''):return f'<img class="photo" src="assets/{name}.jpg" alt="{alt}" width="1200" height="800" loading="lazy" decoding="async">'
def section(id,body,cls=''):return f'<section id="{id}" class="section {cls}"><div class="container">{body}</div></section>'
def heading(title,desc='',eyebrow=''):return '<div class="section-head">'+(p(eyebrow,'eyebrow') if eyebrow else '')+'<h2>'+title+'</h2>'+(p(desc,'lead') if desc else '')+'</div>'
def grid(cards,cls=''):return '<div class="grid3 '+cls+'">'+''.join(cards)+'</div>'
def card(title,body,img='',label='',cls=''):return '<article class="card '+cls+'">'+img+'<div class="card-body">'+(p(label,'eyebrow') if label else '')+'<h3>'+title+'</h3>'+p(body,'card-copy')+'</div></article>'
def steps(labels,id=''):
 return '<ol class="steps" tabindex="0" aria-label="進め方"'+(' id="'+id+'"' if id else '')+'>'+''.join('<li><span class="step-number" aria-hidden="true">'+str(i+1)+'</span><span>'+label+'</span></li>' for i,label in enumerate(labels))+'</ol>'
benefits=[('AIの活用情報が届く','経営に役立つ AI の使い方を、|定期的にお届けします。'),('いつでも相談できる','「これは AI でできる？」を、|LINE でそのまま聞けます。'),('士業AIを無料で試せる','社労士・税理士など、士業の実務に|特化した AI を体験いただけます。')]
icons=['<path d="M8 8h24v24H8z M14 16h12 M14 24h8"/>','<path d="M8 8h24v20H20l-8 8v-8H8z M14 16h12 M14 22h8"/>','<path d="M20 6v26 M8 12h24 M12 12l-6 12h12z M28 12l-6 12h12z M12 34h16"/>']
def benefitcards():return grid([card(t,lines(b),'<svg class="line-icon" viewBox="0 0 40 40" aria-hidden="true">'+icons[i]+'</svg>') for i,(t,b) in enumerate(benefits)],'benefits')
def linepanel(id='line'):
 return section(id,'<div class="line-frame">'+heading('いまの現状を、<br><span class="phrase">見直すきっかけに。</span>','LINE にご登録いただくと、次の 3 つをご利用いただけます。登録は無料、配信はいつでも止められます。')+benefitcards()+'<div class="line-action">'+cta()+'<img class="qr pc-only" src="assets/line-qr.png" alt="LINE友だち追加QRコード" width="160" height="160"></div></div>')
navs=[('index.html','トップ'),('about.html','会社概要'),('service.html','サービス'),('works.html','実績'),('contact.html','お問い合わせ')]
def nav(page):return ''.join('<a href="'+url+'"'+(' class="is-active" aria-current="page"' if url==page else '')+'>'+label+'</a>' for url,label in navs)
def footer():
 n=copy.deepcopy(source.one(tag='footer'))
 mapping={'#hero':'index.html','#service':'service.html','#works':'works.html','#company':'about.html','#contact':'contact.html','#privacy':'privacy.html'}
 for a in n.all('a'):
  a.attrs['href']=mapping.get(a.attrs.get('href'),a.attrs.get('href','index.html'));a.attrs.pop('data-modal',None)
 return n.html()
def page(name,title,desc,body,home=False):
 head='''<!DOCTYPE html>\n<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#FFFFFF">'''
 head+='<title>'+title+'｜AI Linqs</title><meta name="description" content="'+escape(desc,quote=True)+'">'
 head+='''<link rel="icon" sizes="32x32" href="assets/favicon-32.png"><link rel="icon" sizes="192x192" href="assets/favicon-192.png"><link rel="apple-touch-icon" sizes="180x180" href="assets/favicon-180.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Noto+Sans+JP:wght@400;500&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="css/style.css"><script src="js/main.js" defer></script></head>'''
 header='<body><a class="skip" href="#main">本文へスキップ</a><header class="site-header"><div class="header-inner"><a class="logo" href="index.html">AI Linqs</a><nav class="pill-nav" aria-label="グローバルナビゲーション">'+nav(name)+'</nav><div class="header-end">'+cta()+'<button class="burger" id="burger" type="button" aria-label="メニューを開く" aria-expanded="false" aria-controls="spMenu"><span></span><span></span></button></div></div><nav class="sp-menu" id="spMenu" aria-label="スマートフォン用メニュー" hidden>'+nav(name)+cta()+'</nav><noscript><nav class="nojs-nav" aria-label="ページ一覧">'+nav(name)+'</nav></noscript></header>'
 band='' if home else '<section class="page-band"><div class="container"><h1>'+title+'</h1>'+p(desc)+'</div></section>'
 out=head+header+'<main id="main">'+band+body+'</main>'+footer()+'<div class="sticky-cta" id="stickyCta" hidden>'+cta()+'</div><div class="test-badge" id="testBadge" hidden>テスト版 v3</div></body></html>\n'
 # Protect short sentence endings throughout reused copy, without changing text.
 out=re.sub(r'(?<![\w])((?:ご相談ください|お聞かせください|ご覧ください|していきます|つくります|なりました|しています|ありません|できます|大丈夫です|伴走します|ご提案します)。)(?![^<]*>)',r'<span class="phrase">\1</span>',out)
 (ROOT/name).write_text(out)

# Top: full-bleed video, with the existing poster and no overlaid chips.
hero='<section id="hero" class="hero"><video class="hero-image" autoplay muted loop playsinline preload="metadata" poster="assets/hero-poster.jpg" aria-hidden="true"><source src="assets/hero.mp4" type="video/mp4"></video><div class="hero-inner"><div class="hero-copy">'+p('中小企業のための AI 導入パートナー — KOBE, JAPAN','eyebrow')+'<h1>'+lines('人とAIの|ハイブリッド経営を、|当たり前に。')+'</h1>'+p(text('hero',cls='slide__lead'),'lead')+cta()+'</div></div></section>'
philosophy_intro=['私たちがご提案するのは、業務の効率化だけではありません。','AIに任せられることはAIに任せ、人は、人にしかできない仕事に力を注ぐ。','働きがいが高まり、生産性が上がり、会社の成長につながっていく。','それが、AI Linqs の考える「人とAIのハイブリッド経営」です。']
pillars=[('つながり','人の力を、|AIで引き出す。','AIは、人を減らすための道具じゃない。|一人ひとりが本来の仕事に集中できるように。|人と人の“つながり”を、取り戻すために。'),('伴走','ともに考え、|ともに動く。','外注先ではなく、伴走者として。|御社の現場に入り込み、課題を一緒に解く。|経営者の隣で、共に勝ちにいくパートナーへ。'),('未来','テクノロジーが、|地域の未来を変える。','人とAIのハイブリッド経営を、|日本の新しいスタンダードに。|その一歩を、淡路から、御社から。')]
philosophy=section('philosophy',heading(lines('AIを入れて、|人はもっと、人らしく働く。'),eyebrow='私たちの想い')+'<div class="philosophy-intro"><div class="prose">'+''.join(p(x) for x in philosophy_intro)+'</div>'+photo('philosophy','明るい職場で笑顔で話す社員たちのイメージ')+'</div>'+grid([card(lines(t),lines(b),cls='pillar') for l,t,b in pillars],'pillars')+'<div class="actions">'+btn('会社概要を見る','about.html')+'</div>')
issue_titles=['確認が、社長に集まる','人を増やしても、ラクにならない','紙・Excel・口頭が、混在している']
issue_bodies=['判断や承認が経営者に集中し、売上が伸びるほど業務が詰まる。気づけば現場が止まる原因が自分になっている。','採用しても管理工数が減らず、教育の費用ばかり増える。人手は増えたのに利益改善につながらない。','情報がバラバラで、特定の人がいないと業務が止まる。引き継ぎも属人化し、ノウハウが残らない。']
issues=section('issues',heading('こんなお悩み、<span class="phrase">ありませんか？</span>')+grid([card(t,b,photo(f'issue-0{i+1}')) for i,(t,b) in enumerate(zip(issue_titles,issue_bodies))],'issue-cards'),'surface-section')
timing_copy='人手不足が進むこれからの時代、AIは「人を減らす道具」ではなく、|「人の力を引き出す相棒」になります。早く始めた会社ほど、|現場に合った使い方が育ちます。まずは、できるところから。'
timing=section('timing','<div class="timing-layout"><div class="timing-copy">'+heading('AIを入れるなら、<br>いまです。')+p(lines(timing_copy),'timing-body')+'<div class="actions">'+cta()+'</div></div><div class="timing-visual">'+photo('timing','机の前でひらめいた表情で顔を上げる経営者と、隣の社員')+'<span class="timing-mark" aria-hidden="true">！</span></div></div>')
contract_steps=[
 ('お話を伺う','まずは現状とお悩みをお聞かせください。準備は要りません。「何から始めればいいか分からない」という段階で大丈夫です。業務の流れや困りごとを、経営者の言葉のままお話しいただきます。','応接スペースで経営者の話を聞く担当者'),
 ('必要なことを整理','お聞きした内容をもとに、どの業務から手を付けると効果が大きいかを整理します。今のやり方を否定せず、現場の実情に合わせて、無理のない優先順位を一緒に決めていきます。','業務の流れを紙とホワイトボードで整理する社員たち'),
 ('進め方とお見積もり','何を、どの順番で、どのくらいの期間で進めるのかを、工程表としてお見せします。あわせて、減らせる工数と費用を並べたお見積もりをお出しし、投資に見合うかをご判断いただきます。','机に広げた工程表と見積もりを説明する担当者'),
 ('ご納得のうえご契約','内容と費用にご納得いただいてから、ご契約となります。無理な売り込みはいたしません。ご契約後は 2週間に1回お伺いし、定着するまで隣で伴走します。','笑顔で契約書類を交わす経営者と担当者')]
contract_flow='<div class="contract-flow"><h3>ご契約までの流れ</h3><ol class="contract-steps">'+''.join('<li>'+photo(f'step-0{i+1}',alt)+'<span class="step-number" aria-hidden="true">'+str(i+1)+'</span><div class="contract-copy"><h4>'+title+'</h4>'+p(body)+'</div></li>' for i,(title,body,alt) in enumerate(contract_steps))+'</ol></div>'
reason_titles=['進め方をお見せしてから、|ご契約。','アナログ体制の企業の|支援が得意。','定着まで、|隣で伴走。']
reason_bodies=['AIの導入は「何をされるか分からない」のが|不安のもと。まずお話を伺い、|必要なことを整理し、進め方と|費用対効果のお見積もりをお出しします。|ご納得いただいてから、|ご契約です。','紙や口頭、Excel が中心でも大丈夫です。|「うちはまだ紙がメインで」という|会社こそ、伸びしろがあります。|今のやり方を否定せず、|現場に合わせて|設計します。','資料を渡して終わりにしません。|2週間に1回お伺いし、|いまの課題をお聞きして、|解決策を一緒に見つけます。|御社に合わせたオーダーメイドの仕組みを、|一緒につくります。']
reasons=section('reasons',heading('“研修だけ・導入だけ”で、<br><span class="phrase">終わらせない。</span>',text('reasons',cls='slide__lead'),'選ばれる理由')+grid([card(lines(t),lines(b),label=f'0{i+1}') for i,(t,b) in enumerate(zip(reason_titles,reason_bodies))],'reason-cards')+contract_flow)
svc_ids=['svc-training','svc-aistaff','svc-app']
svc_bodies=['社内にAIを定着させる|3ヶ月の伴走研修。経営者の|言葉に合わせて進めます。','反復業務や確認・管理業務を|AIが担い、担当者依存と|管理負荷を解消。','現場固有のフローを、|そのまま使える仕組みに。|紙・Excel運用を置き換えます。']
def services(detail=False):
 cards=[]
 for i,id in enumerate(svc_ids):
  n=get(id);img=n.one('img').html();title=n.one('h3').text()
  cards.append(card(title,lines(svc_bodies[i]),img)+( '' ))
 return section('service',heading('サービス',text('service',cls='slide__lead'))+grid(cards,'service-cards')+('<div class="actions">'+btn('AI研修・教育を詳しく見る','#detail-training')+btn('AI社員・AI部署長構築を詳しく見る','#detail-aistaff')+'</div>' if detail else '<div class="actions">'+btn('サービスを詳しく見る','service.html')+'</div>'))
# Top case summaries are verbatim excerpts from the full outcomes, with explicit two-line layout.
case_summaries=['確認の手間が大きく減り、|人を増やさずに業務が回る体制になりました。','シフト作成も自動化し、|作業時間を大幅に削減することで経営体制を健全化しました。','資料作成や数値分析、定期作業を自動化し、|社内でAIを使いこなす力が向上。']
# Longer second outcome is excerpted without adding claims.
case_summaries[1]='シフト作成も自動化し、|作業時間を大幅に削減'
case_summaries[0]='確認の手間が大きく減り、|人を増やさずに業務が回る体制になりました。'
workcards=[]
for i in range(3):
 n=get(f'case-{i+1}')
 workcards.append(card(n.one('h3').text(),lines(case_summaries[i]),photo(f'case-0{i+1}'),['運送','自動車関連','オフィス'][i]))
works_top=section('works',heading('導入事例')+grid(workcards,'case-cards')+p('※ 写真はイメージです。','note')+'<div class="actions">'+btn('導入事例を詳しく見る','works.html')+'</div>')
page('index.html','中小企業のためのAI導入パートナー',text('hero',cls='slide__lead'),hero+philosophy+issues+timing+reasons+services()+works_top+linepanel(),True)

# About: original text, comments and all confirmation markers retained.
about=get('company')
about.one(cls='container').attrs['class']='container'
about.attrs['id']='philosophy';about.attrs['class']='section about-content'
about_headings=['AIを通じて、|企業と未来をつなげる','人とAIのハイブリッド経営を、|日本の新しいスタンダードに','「共に」が、|AI Linqsらしさ']
about_bodies=['テクノロジーを「一部の大企業のもの」で|終わらせない。中小企業の現場にこそ、|AIの力を届けます。','人にしかできない仕事に集中できる経営へ。|AIと人が補い合う形を、|当たり前にしていきます。']
for i,id in enumerate(['mission','vision','value']):
 n=about.one(id=id);n.one('h3').children=[lines(about_headings[i])]
 if i<2:n.one(cls='slide__lead').children=[lines(about_bodies[i])]
about.one(cls='grid3').attrs['class']='grid3 values'
about.one(cls='section-head').remove(lambda n:'eyebrow' in n.attrs.get('class','').split() and n.text().strip()=='想い')
about.one(cls='section-head').one(cls='slide__note').children=['Mission・Vision・大切にすること']
for id,label in [('mission','Mission'),('vision','Vision'),('value','大切にすること')]:
 about.one(id=id).one(cls='slide__tag').children=[label]
info=about.one(id='company-info');dl=info.one('dl');rows=[]
original_rows={row.one('dt').text():inner(row.one('dd')) for row in dl.children if isinstance(row,Node)}
for label,value in [('会社名',original_rows['運営会社']),('代表者',original_rows['代表者']),('所在地','〒651-0094 兵庫県神戸市中央区琴ノ緒町7-11-1'),('電話番号','準備中'),('事業内容',original_rows['事業内容'])]:
 rows.append('<tr><th scope="row">'+label+'</th><td>'+value+'</td></tr>')
info.children=[c if c is not dl else '<!-- [要確認] 電話番号・設立年月・資本金などは確定後に追記 --><table class="company-table"><tbody>'+''.join(rows)+'</tbody></table>' for c in info.children]
page('about.html','会社概要',text('company',cls='slide__lead'),re.sub(r' ?<span class="todo">.*?</span>','',about.html()))

# Service: original dialog contents become normal, accessible page sections.
def detail(id):
 n=get(id).one(cls='modal__inner');n.remove(lambda c:c.tag=='form')
 return section(id,'<div class="detail-content">'+inner(n)+'</div>','detail-section')
lineup=get('lineup');container=lineup.one(cls='container')
service_cta=lineup.one(id='service-cta');container.children.remove(service_cta)
compare=lineup.one(id='compare');container.children.remove(compare)
shigyo=lineup.one(id='shigyo');container.children.remove(shigyo)
for a in lineup.all('a'):
 if a.attrs.get('href')=='#compare':a.attrs['href']='#compare'
process_body=heading('導入の流れ')+steps([lines('無料相談|LINEで現状をお聞きします'),lines('整理・提案|優先順位と費用感'),lines('設計・実装|無理のない範囲から'),lines('定着まで伴走|現場が自走するまで')])
process_body+='<div class="process-details">'+''.join('<article><h3>'+text(f'step-{i}','h3')+'</h3>'+p(text(f'step-{i}',cls='slide__lead'))+'</article>' for i in range(1,5))+'</div>'
servicebody=services(True)+lineup.html()+detail('detail-training')+detail('detail-aistaff')+section('comparison',compare.html()+shigyo.html())+section('process',process_body)+html('faq')+section('service-consult',service_cta.html())
page('service.html','サービス',text('service',cls='slide__lead'),servicebody)

# Works: large standalone case articles, no fabricated testimonials.
works=get('works');works.one(cls='grid3').attrs['class']='case-list'
for i in range(1,4):
 n=works.one(id=f'case-{i}');n.attrs['class']='case-detail';n.remove(lambda x:'fig' in x.attrs.get('class','').split())
 body=n.one(cls='card-body');body.children.append('<aside class="voice"><h4>ご担当者様の声</h4><p>導入企業様からのコメントは、ご了承をいただいたものから順次掲載してまいります。</p></aside>')
works.children.append('<!-- [要確認] 各社の掲載許諾（社名・内容の公開可否）を最終確認のこと -->')
page('works.html','実績',text('works',cls='slide__lead'),works.html())

# Contact: use the same benefit cards as the top page.
contact_lead=text('contact',cls='slide__lead')
consult=get('contact-step');consult.attrs['class']='consult-content'
consult_lines=['どこにAIを使う余地があるか、|現状からお伝えします。','何から始めると効果が高いか、|順番を整理します。','どのくらいの規模・費用になりそうか、|目安をお伝えします。']
for node,body in zip(consult.one(cls='icons3').all('div'),consult_lines):
 node.children=[node.one('b'),p(lines(body))]
contactbody=section('contact',heading('まずは、LINEで<br><span class="phrase">無料相談から。</span>',contact_lead)+'<div class="line-frame">'+heading('LINE 登録でできること')+benefitcards()+'</div>'+consult.html()+'<div class="contact-action">'+html('line')+'</div>')
page('contact.html','お問い合わせ',contact_lead,contactbody)
privacy=get('privacy').one(cls='modal__inner');privacy.remove(lambda n:'modal__head' in n.attrs.get('class','').split())
page('privacy.html','プライバシーポリシー','個人情報の取り扱い',section('privacy','<div class="privacy-prose">'+inner(privacy)+'</div>'))

# Resolve inherited one-page links. All generated pages work without JS for navigation.
for name in ['index.html','about.html','service.html','works.html','contact.html','privacy.html']:
 path=ROOT/name;s=path.read_text()
 s=re.sub(r'\sdata-modal(?:="[^"]*")?','',s)
 s=s.replace('href="#privacy"','href="privacy.html"')
 s=s.replace('href="#contact"','href="contact.html#contact"')
 if name=='contact.html':s=s.replace('href="contact.html#contact"','href="#contact"')
 path.write_text(s)
print('Built six static pages from _v3.0-index.html')
