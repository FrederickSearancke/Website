from pathlib import Path
from hashlib import sha256
import json
from html import escape, unescape
import re
from authored import author, approved, document, comparison, paragraph_text

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
PROFILE = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
BASE = '/projects/gpt-finetuning/'
# Selected palette: 01 Cobalt & Amber. Match first paint to dist/theme.css.
THEME_COLOR = '#031B3A'
THEME_CSS_VERSION = sha256((OUT / 'theme.css').read_bytes()).hexdigest()[:12]
STYLES_CSS_VERSION = sha256((OUT / 'styles.css').read_bytes()).hexdigest()[:12]
HOME_CSS_VERSION = sha256((OUT / 'home.css').read_bytes()).hexdigest()[:12]
CHAPTERS = [
 ('data-preparation', 'Training-data preparation', author('gpt-formatting-p01-b06','span')),
 ('quality-control', 'Quality control & curation', author('gpt-quality-p01-b03','span',excerpt='In this section I’ve described the filtering process that went into curating the training data for the deployed model, including the problems with the dataset to motivate these choices.')),
 ('retrieval', 'Retrieval & the vector database', author('gpt-retrieval-p01-b03','span',excerpt='I’ve described how I got the model to know up-to-date company policy and product information.')),
 ('testing-and-integration', 'Testing & live-chat integration', author('gpt-integration-p01-b09','span')),
]

LINKEDIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 2H3.55C2.69 2 2 2.68 2 3.52v16.96C2 21.32 2.69 22 3.55 22h16.9c.86 0 1.55-.68 1.55-1.52V3.52C22 2.68 21.31 2 20.45 2zM7.93 18.75H4.98V9.2h2.95v9.55zM6.45 7.9a1.71 1.71 0 1 1 0-3.42 1.71 1.71 0 0 1 0 3.42zm12.3 10.85H15.8v-4.64c0-1.1-.02-2.52-1.53-2.52-1.54 0-1.78 1.2-1.78 2.44v4.72H9.54V9.2h2.83v1.3h.04c.4-.75 1.36-1.54 2.8-1.54 3 0 3.54 1.98 3.54 4.55v5.24z"/></svg>'
GITHUB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.77-.24.77-.54v-2.1c-3.12.68-3.78-1.33-3.78-1.33-.51-1.3-1.24-1.65-1.24-1.65-1.02-.7.08-.69.08-.69 1.12.08 1.71 1.15 1.71 1.15 1 1.7 2.62 1.21 3.26.93.1-.72.4-1.21.71-1.49-2.49-.29-5.1-1.24-5.1-5.54 0-1.23.44-2.23 1.15-3.02-.11-.28-.5-1.43.11-2.98 0 0 .94-.3 3.08 1.15A10.7 10.7 0 0 1 12 6.14c.95 0 1.9.13 2.79.38 2.14-1.45 3.07-1.15 3.07-1.15.61 1.55.23 2.7.12 2.98.72.79 1.14 1.79 1.14 3.02 0 4.31-2.62 5.25-5.12 5.53.4.35.76 1.03.76 2.08v3.11c0 .3.21.65.77.54A11.2 11.2 0 0 0 12 .8z"/></svg>'

def social_links():
    items = []
    for name, icon in [('linkedin', LINKEDIN), ('github', GITHUB)]:
        if PROFILE.get(name):
            label = 'LinkedIn' if name == 'linkedin' else 'GitHub'
            items.append(f'<a href="{escape(PROFILE[name])}" target="_blank" rel="noopener noreferrer" aria-label="{label} (opens in a new tab)">{icon}</a>')
    return '<div class="socials">' + ''.join(items) + '</div>' if items else ''

def portrait(large=False):
    if PROFILE.get('portrait'):
        if large:
            return f'<div class="portrait-frame"><img class="contact-portrait" src="{escape(PROFILE["portrait"])}" alt="Frederick Searancke" width="1024" height="1536"></div>'
        return '<img class="portrait" src="/assets/profile-avatar-232.png" srcset="/assets/profile-avatar-116.png 116w, /assets/profile-avatar-232.png 232w, /assets/profile-avatar-464.png 464w" sizes="(max-width: 520px) 48px, 58px" alt="Frederick Searancke" width="464" height="464" decoding="async">'
    return '<div class="portrait monogram" aria-label="Frederick Searancke initials">FS</div>' if not large else ''

def header(current='', *, home=False):
    def nav(label, url, key):
        return f'<a href="{url}"' + (' aria-current="page"' if current == key else '') + f'>{label}</a>'
    resume = f'<a class="nav-resume" href="{PROFILE["resume"]}" target="_blank" rel="noopener noreferrer">CV <span aria-hidden="true">↗</span></a>' if PROFILE.get('resume') else ''
    identity = f'<div class="identity-details">{portrait()}<div><p class="identity-name">Frederick Searancke</p><p class="identity-role">Aspiring quant researcher <span aria-hidden="true">·</span> Computer Science, University of Warwick</p></div></div>' if home else ''
    home_button = '' if home else '<a class="nav-home" href="/">Home</a>'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header"><div class="wrap header-inner">{identity}
      <button class="menu-toggle" aria-label="Toggle navigation" aria-expanded="false" aria-controls="main-navigation">Menu <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 7h18M3 16h18"/></svg></button>
      <nav class="main-nav" id="main-navigation" aria-label="Main navigation">
      {home_button}{nav('Skills','/skills/','skills')}{nav('About me','/about/','about')}{nav('Contact','/contact/','contact')}{resume}
      </nav></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap footer-inner"><a class="footer-name" href="/">Frederick Searancke</a><div class="footer-links"><a href="/#projects">Projects</a><a href="/contact/">Get in touch</a>{social_links()}</div></div></footer>'''

def page(title, description, body, *, home=False, current=''):
    title = re.sub(r'<[^>]+>', ' ', title).strip().rstrip('.')
    description = unescape(re.sub(r'<[^>]+>', '', description))
    preload = f'<link rel="stylesheet" href="/home.css?v={HOME_CSS_VERSION}"><link rel="preload" as="image" href="/assets/ebm-options-thumbnail.png">' if home else ''
    return f'''<!doctype html><html lang="en" style="background:{THEME_COLOR};color-scheme:dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} — Frederick Searancke</title><meta name="description" content="{escape(description)}"><meta name="theme-color" content="{THEME_COLOR}"><meta name="color-scheme" content="dark"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css?v={STYLES_CSS_VERSION}"><link rel="stylesheet" href="/theme.css?v={THEME_CSS_VERSION}">{preload}<script src="/app.js" defer></script></head><body class="{'home' if home else 'inner-page'}">{header(current,home=home)}{body}{footer()}</body></html>'''

def write(route, html):
    dest = OUT / route.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html, encoding='utf-8')

def figure(file,alt,caption):
    # Reserve the PNG's space before lazy loading so chapter anchors do not move.
    with (OUT / 'assets' / file).open('rb') as asset:
        png_header = asset.read(24)
    if png_header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Expected a PNG figure: {file}')
    width = int.from_bytes(png_header[16:20], 'big')
    height = int.from_bytes(png_header[20:24], 'big')
    return f'<figure><a href="/assets/{file}" target="_blank" rel="noopener noreferrer" aria-label="Enlarge image: {escape(alt)} (opens in a new tab)"><img src="/assets/{file}" alt="{escape(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption><span class="enlarge">Open image ↗</span>{caption}</figcaption></figure>'

def source(file):
    return f'<div class="source-link"><a class="button" href="/assets/{file}" target="_blank" rel="noopener noreferrer">Read the original PDF <span aria-hidden="true">↗</span></a></div>'

def flow(stages):
    return '<div class="flow">' + '<span class="flow-arrow" aria-hidden="true">→</span>'.join(f'<div class="flow-item"><span>{i:02}</span><strong>{s}</strong></div>' for i,s in enumerate(stages,1)) + '</div>'

def project_hero(label,title,lede,tags):
    return f'<div class="project-hero"><p class="section-label">{label}</p><h1>{title}</h1><p class="lede">{lede}</p><div class="project-tags">' + ''.join(f'<span class="tag">{t}</span>' for t in tags) + '</div></div>'

def summary(items):
    return '<div class="project-summary">'+''.join(f'<div><small>{label}</small><strong>{value}</strong></div>' for label,value in items)+'</div>'

def gpt_pagination(active='overview', position='bottom'):
    sections = [('overview', BASE, 'Project overview')] + [(slug, BASE+slug+'/', title) for slug,title,desc in CHAPTERS]
    index = next(i for i,section in enumerate(sections) if section[0] == active)
    previous = sections[index-1][1:] if index else None
    following = sections[index+1][1:] if index+1 < len(sections) else None
    previous_link = f'<a class="chapter-previous" href="{previous[0]}"><small>← Previous</small>{escape(previous[1])}</a>' if previous else ''
    following_link = f'<a href="{following[0]}"><small>Next →</small>{escape(following[1])}</a>' if following else ''
    return (f'<nav class="chapter-pagination chapter-pagination-{position}" aria-label="Project navigation ({position})">'
            f'{previous_link}'
            f'{following_link}</nav>')

def gpt_page(title,desc,article,active='overview',label='Machine learning · Applied AI'):
    breadcrumb='<div class="breadcrumbs"><a href="/#projects">All projects</a><span aria-hidden="true">/</span><a href="/projects/gpt-finetuning/">GPT fine-tuning</a></div>'
    if active == 'overview':
        breadcrumb='<div class="breadcrumbs"><a href="/#projects">← All projects</a></div>'
    hero=project_hero(label,title,desc,['Python','Fine-tuning','Retrieval','Data engineering'])
    return page(title,desc,f'<main id="main" class="gpt-project"><div class="wrap">{breadcrumb}{gpt_pagination(active,"top")}{hero}<div class="single-article"><article class="article">{article}</article>{gpt_pagination(active)}</div></div></main>',current='projects')

projects = [
 {'slug':'ebm-options-profitability','category':'machine-learning','label':'Machine learning','meta':'Explainable Boosting Machines','image':'ebm-options-thumbnail.png','imageclass':'ebm-options','alt':'EBM: Predicting options profit, with two saved IV-response curves.','width':2000,'height':2000,'title':author('ebm-options-p01-b01','span'),'desc':approved('ebm-options-overview','span',excerpt='I trained an Explainable Boosting Machine (EBM) to predict the profitability of options trades.')+' '+approved('ebm-options-overview','span',excerpt="The AI model wasn't stable across seed values, so I developed the work to predict actionable signals such as variance of the market returns rather than absolute options prices.")},
 {'slug':'gpt-finetuning','category':'machine-learning','label':'Machine learning','meta':'','image':'vectors.png','imageclass':'vector','alt':'RAG visualised: projection of product and policy embeddings','width':2048,'height':1536,'title':'Can GPT-4o Learn to Handle Customer Support?','desc':author('gpt-integration-p01-b03','span',excerpt='I built a Python application that combined the fine-tuned model with retrieval of product and policy information.')},
 {'slug':'blender-pipeline','category':'automation','label':'Automation','meta':'Python + Blender','image':'artwork-to-relief.png','imageclass':'blender','alt':'Full artwork-to-relief comparison: bee artwork, heightmap and generated clay roller','width':1800,'height':850,'title':'From artwork to<br>3D-printable rollers','desc':approved('blender-card-intro')},
 {'slug':'maze-solver','category':'algorithms','label':'Algorithms','meta':'Java','image':'maze-first.png','imageclass':'maze','alt':'Maze from the route-memory controller project','width':910,'height':830,'title':'A maze solver<br>that remembers its route','desc':author('maze-p01-b02','span',excerpt='The final controller could remember a successful route and use it to reach the target more directly on subsequent runs.')},
 {'slug':'ebm-volatility','category':'machine-learning','label':'Machine learning','meta':'Explainable Boosting Machines','image':'ebm-paired-interaction-chart.svg','imageclass':'ebm','alt':'Premarket and opening volatility: 14 by 14 equal square buckets showing learned weights, with 653 observed training days. Blue lowers the forecast and amber raises it.','width':660,'height':430,'title':'Forecasting market volatility using explainable AI.','desc':author('ebm-volatility-user-introduction','span')},
]

def project_thumbnail(p, *, first=False):
    if p['imageclass'] == 'ebm-options':
        # Reframe the supplied PNG in two clipped layers; retain the actual plotted lines.
        loading = 'fetchpriority="high"' if first else 'loading="lazy" decoding="async"'
        layers = ''.join(f'<img class="ebm-options-{layer}" src="/assets/{p["image"]}" alt="" width="{p["width"]}" height="{p["height"]}" {loading}>' for layer in ['labels','plot'])
        return f'<div class="project-image ebm-options" role="img" aria-label="{escape(p["alt"])}"><div class="ebm-thumbnail-layout" aria-hidden="true">{layers}</div></div>'
    if p['imageclass'] == 'blender':
        stages = [
            ('01', 'Source artwork', 'blender-source-artwork.jpg', 1024, 1024, 'artwork'),
            ('02', 'Smoothed heightmap', 'blender-smoothed-heightmap.jpg', 1024, 1024, 'heightmap'),
            ('03', 'Generated relief', 'blender-embossed-detail.png', 640, 1400, 'relief'),
        ]
        panels = ''.join(f'<span class="blender-stage"><span class="blender-stage-label"><span class="blender-stage-number">{number}</span>{label}</span><span class="blender-stage-image {kind}"><img src="/assets/{file}" alt="" width="{width}" height="{height}" loading="lazy" decoding="async"></span></span>' for number,label,file,width,height,kind in stages)
        return f'<div class="project-image blender" role="img" aria-label="The same bee and honeycomb pattern through three stages: original artwork, smoothed grayscale heightmap, and embossed 3D relief">{panels}</div>'
    loading = 'fetchpriority="high"' if first else 'loading="lazy" decoding="async"'
    return f'<div class="project-image {p["imageclass"]}"><img src="/assets/{p["image"]}" alt="{p["alt"]}" {loading} width="{p["width"]}" height="{p["height"]}"></div>'

rows=''
for i,p in enumerate(projects,1):
    metadata = f'<span aria-hidden="true">·</span><span>{p["meta"]}</span>' if p['meta'] else ''
    rows+=f'''<a class="project-row" href="/projects/{p['slug']}/" data-category="{p['category']}">{project_thumbnail(p,first=i==1)}<div class="project-copy"><div class="project-meta"><span class="index">0{i}</span><span>{p['label']}</span>{metadata}</div><h3>{p['title']}</h3><p>{p['desc']}</p></div><span class="row-arrow" aria-hidden="true">↗</span></a>'''

visual_dialog=f'''<dialog class="visual-inspector" id="visual-inspector" aria-labelledby="visual-inspector-title"><form method="dialog" class="visual-close-form"><button class="visual-close" aria-label="Close visual explanation" autofocus><svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></form><div class="visual-inspector-layout"><div class="visual-inspector-figure"><img src="/assets/vectors.png" alt="Two-dimensional projection of product names, short and full descriptions, and company information embeddings" width="2048" height="1536" loading="lazy"></div><div class="visual-inspector-copy"><p class="visual-inspector-kicker">Behind the visual</p><h2 id="visual-inspector-title">A map of the AI’s knowledge.</h2>{approved('rag-knowledge-base','p',excerpt='I implemented the knowledge base in Python as a JSONL dataset, combining product information with company policies and staff training documents.')}{approved('rag-vector-projection','p')}<a class="visual-chapter-link" href="/projects/gpt-finetuning/retrieval/#vector-projection">How I built it <span aria-hidden="true">↗</span></a></div></div></dialog>'''

home=f'''<main id="main"><section class="section wrap project-section" id="projects" aria-labelledby="projects-title"><h1 class="section-label">My projects</h1><div class="section-heading"><h2 id="projects-title">Selected work<span style="color:var(--accent)">.</span></h2></div><div class="filter-bar" role="group" aria-label="Filter projects"><button class="filter" data-filter="all" aria-pressed="true">All projects</button><button class="filter" data-filter="machine-learning" aria-pressed="false">Machine learning</button><button class="filter" data-filter="automation" aria-pressed="false">Automation</button><button class="filter" data-filter="algorithms" aria-pressed="false">Algorithms</button></div><p id="filter-status" class="visually-hidden" aria-live="polite">{len(projects)} projects shown</p><div class="project-list">{rows}</div></section>
{visual_dialog}
</main>'''
write('/',page('Projects & research','Projects in machine learning, software automation and algorithms by Frederick Searancke.',home,home=True))

# TODO: Replace this placeholder with the user's volatility-forecasting writeup when supplied.
volatility_title = 'Forecasting market volatility using explainable AI.'
volatility_hero = project_hero('Machine learning · Explainable Boosting Machines',volatility_title,author('ebm-volatility-user-introduction','span'),[])
write('/projects/ebm-volatility/',page(volatility_title,'I trained an explainable machine learning model to predict late-day intra-day realised volatility of E-mini S&P 500 futures that was stable over many training seeds.',f'<main id="main"><div class="wrap"><div class="breadcrumbs"><a href="/#projects">← All projects</a></div>{volatility_hero}<p class="coming-soon-message">Project writeup coming soon</p></div></main>',current='projects'))

# Preserve source prose except for the user's recorded, approved wording changes.
options_title = paragraph_text('ebm-options-p01-b01')
options_description = approved('ebm-options-overview','span',excerpt='I trained an Explainable Boosting Machine (EBM) to predict the profitability of options trades.')
options_hero = '<div class="project-hero">'+author('ebm-options-p01-b01','h1')+'</div>'
def options_figure(file, caption_id):
    return figure(file,paragraph_text(caption_id),author(caption_id,'span'))
options_article = document('ebm-options',overrides={'ebm-options-p01-b03':approved('ebm-options-overview','p')},after={
 'ebm-options-p01-b06':options_figure('ebm-options-trade-profits.png','ebm-options-p01-b07'),
 'ebm-options-p02-b02':options_figure('ebm-options-training-examples.png','ebm-options-p02-b03'),
 'ebm-options-p03-b04':options_figure('ebm-options-iv-trend.png','ebm-options-p03-b05'),
 'ebm-options-p03-b06':options_figure('ebm-options-correlations.png','ebm-options-p04-b01')+options_figure('ebm-options-feature-overlap.png','ebm-options-p04-b02'),
 'ebm-options-p05-b01':options_figure('ebm-options-iv-comparison.png','ebm-options-p05-b02'),
 'ebm-options-p05-b03':options_figure('ebm-options-iv-diagnostics.png','ebm-options-p06-b01'),
 'ebm-options-p06-b03':options_figure('ebm-options-profit-risk.png','ebm-options-p07-b01'),
 'ebm-options-p07-b07':options_figure('ebm-options-loss-functions.png','ebm-options-p08-b01'),
})+source('ebm-options-profitability.pdf')
write('/projects/ebm-options-profitability/',page(options_title,options_description,f'<main id="main"><div class="wrap"><div class="breadcrumbs"><a href="/#projects">← All projects</a></div>{options_hero}<div class="single-article"><article class="article">{options_article}</article></div></div></main>',current='projects'))


overview='<h2>Overview</h2>'
overview+=author('gpt-formatting-p01-b03',excerpt='I made a fine-tuned machine learning model to accurately answer customer live chats as well as a trained human with up-to-date company policy and product information that was performant enough to converse with real customers in real time. I did this work over the summer of 2024.')
overview+='<h2>The application</h2>'+author('gpt-integration-p01-b03')
overview+='<h2>Evaluation and outcome</h2>'+approved('gpt-evaluation-outcome','p')
write(BASE,gpt_page('Can GPT-4o Learn to Handle Customer Support?',author('gpt-integration-p01-b03','span',excerpt='I built a Python application that combined the fine-tuned model with retrieval of product and policy information.'),overview))

chapter_bodies={}
chapter_bodies['data-preparation']=document('gpt-formatting',after={
 'gpt-formatting-p01-b06':figure('data-transformation.png','An email transcript alongside its normalised intermediate message format','Training-data formatting · intermediate representation'),
})+source('gpt-data-preparation.pdf')

quality_skip={
 'gpt-quality-p03-b03','gpt-quality-p03-b05','gpt-quality-p03-b06',
 'gpt-quality-p03-b10','gpt-quality-p03-b12','gpt-quality-p03-b13',
 'gpt-quality-p04-b01','gpt-quality-p04-b02','gpt-quality-p04-b03','gpt-quality-p04-b04',
 'gpt-quality-p04-b08','gpt-quality-p04-b09','gpt-quality-p04-b10',
}
quality_comparisons={
 'gpt-quality-p02-b08':approved('gpt-evaluation-outcome','p'),
 'gpt-quality-p03-b02':comparison('gpt-quality-p03-b02','gpt-quality-p03-b03','gpt-quality-p03-b05','gpt-quality-p03-b06'),
 'gpt-quality-p03-b09':comparison('gpt-quality-p03-b09','gpt-quality-p03-b10','gpt-quality-p03-b12','gpt-quality-p03-b13'),
 'gpt-quality-p03-b16':author('gpt-quality-p04-b02')+comparison('gpt-quality-p03-b16','gpt-quality-p04-b01','gpt-quality-p04-b03','gpt-quality-p04-b04'),
 'gpt-quality-p04-b07':comparison('gpt-quality-p04-b07','gpt-quality-p04-b08','gpt-quality-p04-b09','gpt-quality-p04-b10'),
}
chapter_bodies['quality-control']=document('gpt-quality',skip=quality_skip,overrides=quality_comparisons)+source('gpt-quality-control.pdf')

chapter_bodies['retrieval']=document('gpt-retrieval',skip={'gpt-retrieval-p04-b02'},overrides={
 'gpt-retrieval-p03-b01':approved('rag-knowledge-base','p'),
 'gpt-retrieval-p02-b04':author('gpt-retrieval-p02-b04','h2').replace('<h2 ', '<h2 id="vector-projection" ', 1),
},after={
 'gpt-retrieval-p01-b13':figure('product-record.png','Product record from the original vector database writeup','Example of product data'),
 'gpt-retrieval-p03-b01':approved('rag-vector-projection','p')+figure('vectors.png','Two-dimensional projection of names, descriptions and general information embeddings','Vector database · 2D projection'),
 'gpt-retrieval-p03-b02':author('gpt-retrieval-p06-b01')+figure('retrieval-matching.png','Product-field embeddings matched against a question and linked back to the original record','Matching embeddings to product records'),
 'gpt-retrieval-p03-b03':author('gpt-retrieval-p05-b02')+figure('retrieval-sequence.png','Sequence from customer question through embedding, local retrieval and model response','The Python application · runtime sequence'),
})+source('gpt-retrieval.pdf')

chapter_bodies['testing-and-integration']=document('gpt-integration',after={
 'gpt-integration-p01-b09':figure('testing-app.png','Python testing application with model controls, retrieved context and a conversation','Testing application'),
})+source('gpt-testing-and-integration.pdf')

for i,(slug,title,desc) in enumerate(CHAPTERS):
    write(BASE+slug+'/',gpt_page(title+'.',desc,chapter_bodies[slug],slug,f'GPT fine-tuning · Part {i+1:02} of 04'))

blender_hero=project_hero('Automation · Python + Blender','From artwork to<br>3D-printable rollers.',approved('blender-card-intro'),['Python','Blender','Procedural modelling','3D printing'])
blender=document('blender',skip={'blender-p03-b01','blender-p03-b04'},after={
 'blender-p01-b05':figure('artwork-to-relief.png',paragraph_text('blender-p03-b03'),author('blender-p03-b02','span')),
 'blender-p02-b03':author('blender-p03-b04','h2')+figure('roller-comparison.png',paragraph_text('blender-p04-b02'),author('blender-p04-b01','span')),
})+source('blender-pipeline.pdf')
write('/projects/blender-pipeline/',page('Automating 3D-printable clay rollers',paragraph_text('blender-p01-b05'),f'<main id="main"><div class="wrap"><div class="breadcrumbs"><a href="/#projects">← All projects</a></div>{blender_hero}{summary([("Product sales","£1,100+"),("Original designs","100+"),("Outputs","BLEND + STL")])}<div class="single-article"><article class="article">{blender}</article></div></div></main>',current='projects'))

maze_hero=project_hero('Algorithms · Java','A maze solver<br>that remembers its route.',author('maze-p01-b02','span',excerpt='The final controller could remember a successful route and use it to reach the target more directly on subsequent runs.'),['Java','Graph traversal','Stacks','Warwick CS118'])
maze_pair='<figure class="maze-comparison"><div class="maze-pair"><a href="/assets/maze-first.png" target="_blank" rel="noopener noreferrer" aria-label="Enlarge first maze image"><img src="/assets/maze-first.png" alt="Maze image from page 4 of the original writeup" loading="lazy"></a><a href="/assets/maze-later.png" target="_blank" rel="noopener noreferrer" aria-label="Enlarge second maze image"><img src="/assets/maze-later.png" alt="Maze image from page 5 of the original writeup" loading="lazy"></a></div><figcaption>'+author('maze-p04-b01-caption','span')+'</figcaption></figure>'
maze=document('maze',skip={'maze-p04-b01'},after={
 'maze-p01-b04':figure('maze-cells.png','Dead end, corridor, junction and crossroads in the maze','Local maze observations · source attribution retained in the original figure'),
 'maze-p01-b07':author('maze-p04-b01','h2')+maze_pair,
 'maze-p01-b10':figure('maze-start.png','Comparison between arriving in a corridor and starting in a corridor with two unexplored exits','The two-exit starting cell · illustration based on CS118 Guide 2024–25, Figure 8.1'),
})+source('java-maze-solver.pdf')
write('/projects/maze-solver/',page('Java maze solver with route memory',paragraph_text('maze-p01-b02'),f'<main id="main"><div class="wrap"><div class="breadcrumbs"><a href="/#projects">← All projects</a></div>{maze_hero}{summary([("Coursework 1","85%"),("Coursework 2","87%"),("Highest section mark","97%")])}<div class="single-article"><article class="article">{maze}</article></div></div></main>',current='projects'))


skills_hero='<div class="project-hero skills-hero"><h1>Skills in practice.</h1><a class="button reading-jump" href="#reading-title">My favourite books <span aria-hidden="true">↓</span></a></div>'
skills_data=json.loads((ROOT / 'content/skills.json').read_text(encoding='utf-8'))
highlighted_skills=set(skills_data.get('highlighted_skills', []))
skill_groups=''.join('<div class="skill-group"><h3>'+escape(group['heading'])+'</h3><ul class="skill-list">'+''.join('<li'+(' class="skill-highlight"' if skill in highlighted_skills else '')+'>'+escape(skill)+'</li>' for skill in group['skills'])+'</ul></div>' for group in skills_data['groups'])
skills=f'''<main id="main"><div class="wrap">{skills_hero}<section class="skills-page" aria-label="Technical skills"><div class="skill-groups">
{skill_groups}
</div></section>
<section class="reading-section" aria-labelledby="reading-title"><h2 id="reading-title">My favourite books</h2>
<ul class="book-list">
<li class="book-item book-item-with-project"><img class="book-cover" src="/assets/book-professional-automated-trading.jpg" alt="" width="300" height="450" loading="lazy" decoding="async"><h3>Professional Automated Trading: Theory and Practice</h3><p class="book-author">Eugene A. Durenard</p>
<!-- TODO(stock-market-trading-bots-project): When Frederick supplies the stock-market trading-bot project to add, connect this book's arrow CTA to that project's final route. Replace the disabled button #trading-bots-project-cta with an anchor using the same class and SVG, set its href to the new project, retain it inside .book-project-tail, update aria-label to "Read about my stock-market trading bots", and remove type, disabled, aria-describedby, title and the #trading-bots-project-status coming-soon label. Keep this placeholder unlinked until that project exists. -->
<p class="book-note">I used this book to build a set of stock-market trading bots, which I run with <span class="book-project-tail">my own money. <button id="trading-bots-project-cta" class="book-project-button" type="button" disabled aria-label="Trading-bot project — coming soon" aria-describedby="trading-bots-project-status" title="Project coming soon"><svg viewBox="0 0 16 16" width="12" height="12" fill="none" aria-hidden="true"><path d="M4 12 12 4M4 4h8v8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button></span><span id="trading-bots-project-status" class="visually-hidden">Project coming soon</span></p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-positional-option-trading.jpg" alt="" width="300" height="445" loading="lazy" decoding="async"><h3>Positional Option Trading: An Advanced Guide</h3><p class="book-author">Euan Sinclair</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-volatility-trading.jpg" alt="" width="300" height="453" loading="lazy" decoding="async"><h3>Volatility Trading</h3><p class="book-author">Euan Sinclair</p></li>
<li class="book-item"><span class="book-cover book-cover-retail-options" aria-hidden="true"><img src="/assets/book-retail-options-trading.png" alt="" width="238" height="357" loading="lazy" decoding="async"></span><h3>Retail Options Trading</h3><p class="book-author">Euan Sinclair and Andrew Mack</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-black-swan.jpg" alt="" width="292" height="450" loading="lazy" decoding="async"><h3>The Black Swan</h3><p class="book-author">Nassim Nicholas Taleb</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-alignment-problem.webp" alt="" width="416" height="628" loading="lazy" decoding="async"><h3>The Alignment Problem</h3><p class="book-author">Brian Christian</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-most-human-human.jpg" alt="" width="292" height="450" loading="lazy" decoding="async"><h3>The Most Human Human</h3><p class="book-author">Brian Christian</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-pattern-on-the-stone.jpg" alt="" width="426" height="640" loading="lazy" decoding="async"><h3>The Pattern on the Stone</h3><p class="book-author">W. Daniel Hillis</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-alexs-adventures-in-numberland.jpg" alt="" width="1516" height="2333" loading="lazy" decoding="async"><h3>Alex’s Adventures in Numberland</h3><p class="book-author">Alex Bellos</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-a-world-without-work.jpg" alt="" width="326" height="500" loading="lazy" decoding="async"><h3>A World Without Work</h3><p class="book-author">Daniel Susskind</p></li>
</ul>
<h3 class="reading-group-title" id="fiction-title">Fiction</h3>
<ul class="book-list" aria-labelledby="fiction-title">
<li class="book-item"><img class="book-cover" src="/assets/book-crime-and-punishment.jpg" alt="" width="300" height="450" loading="lazy" decoding="async"><h3>Crime and Punishment</h3><p class="book-author">Fyodor Dostoevsky</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-brothers-karamazov.jpg" alt="" width="279" height="450" loading="lazy" decoding="async"><h3>The Brothers Karamazov</h3><p class="book-author">Fyodor Dostoevsky</p></li>
<li class="book-item"><span class="book-cover book-cover-earthsea" aria-hidden="true"><img src="/assets/book-wizard-of-earthsea.webp" alt="" width="500" height="750" loading="lazy" decoding="async"></span><h3>A Wizard of Earthsea</h3><p class="book-author">Ursula K. Le Guin</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-andromeda-strain.jpg" alt="" width="292" height="450" loading="lazy" decoding="async"><h3>The Andromeda Strain</h3><p class="book-author">Michael Crichton</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-way-of-kings.jpg" alt="Cover of The Way of Kings, the first Stormlight book" width="1894" height="2853" loading="lazy" decoding="async"><h3>The Stormlight Archives (4/5 books)</h3><p class="book-author">Brandon Sanderson</p></li>
<li class="book-item"><img class="book-cover" src="/assets/book-mistborn.jpg" alt="Cover of the first Mistborn book" width="1840" height="2774" loading="lazy" decoding="async"><h3>Mistborn (8 books)</h3><p class="book-author">Brandon Sanderson</p></li>
</ul></section></div></main>'''
write('/skills/',page('Skills','Skills in machine learning, quantitative research, software and systems, plus my favourite books on trading, AI and fiction.',skills,current='skills'))

about_hero='<div class="project-hero"><h1 class="section-label">About me</h1></div>'
about=f'''<main id="main"><div class="wrap">{about_hero}<div class="about-copy">
<h2>1st place at Saxon Novices 2026.</h2>
<p><strong>I finished first out of 22 fencers, with 12 wins and no losses.</strong> I won the men’s senior foil competition at Saxon Novices on 19 April 2026, going unbeaten through both group rounds and the knockout stages.</p>
<div class="fencing-gallery">
<figure><a href="/assets/fencing-action.jpg" target="_blank" rel="noopener noreferrer" aria-label="Enlarge fencing action photo"><img src="/assets/fencing-action.jpg" alt="Frederick fencing on the right during a foil bout" width="1600" height="739" decoding="async"></a><figcaption>In action on the piste — I’m on the right.</figcaption></figure>
<figure><a href="/assets/fencing-medal-presentation.jpg" target="_blank" rel="noopener noreferrer" aria-label="Enlarge Saxon Novices medal presentation photo"><img src="/assets/fencing-medal-presentation.jpg" alt="Frederick, second from the left, at the Saxon Novices medal presentation" width="1600" height="1200" decoding="async"></a><figcaption>Saxon Novices medal presentation — I’m second from the left.</figcaption></figure>
</div>
<h2 style="margin-top:45px">Skiing</h2>
<p>I hold a BASI Level 1 ski instructor qualification, combining my interest in skiing with teaching others.</p>
<p>I volunteered for 35 hours helping children aged 4–8 learn to ski for the first time. This meant introducing them to the basics and helping them become comfortable on skis.</p>
<h2 style="margin-top:45px">Introducing Python.</h2>
<p>I volunteered at my school's computer science club, teaching Year 7 and Year 8 pupils to code in Python for over 5 years. I really enjoyed the opportunity to share my passion for programming, helping young students see how exciting coding can be.</p>
<h2 style="margin-top:45px">Duke of Edinburgh’s Gold Award.</h2>
<p>I completed my Gold Duke of Edinburgh’s Award.</p>
<div style="margin-top:35px"><a class="button" href="/contact/">Get in touch <span aria-hidden="true">↗</span></a></div></div></div></main>'''
write('/about/',page('About me','Frederick Searancke: Saxon Novices 2026 foil winner, BASI Level 1 ski instructor, and volunteer teaching young skiers and Python beginners.',about,current='about'))

contact_hero='<div class="project-hero"><h1 class="section-label">Contact me</h1></div>'
contact_items=f'''<div class="contact-item"><div><small>Email</small><a href="mailto:{escape(PROFILE['email'])}">{escape(PROFILE['email'])}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div><div class="contact-item"><div><small>Phone</small><a href="tel:{escape(PROFILE['phoneHref'])}">{escape(PROFILE['phone'])}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'''
for label,key in [('LinkedIn','linkedin'),('GitHub','github')]:
    if PROFILE.get(key):
        contact_items+=f'<div class="contact-item"><div><small>{label}</small><a href="{escape(PROFILE[key])}" target="_blank" rel="noopener noreferrer">Find me on {label}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'
if PROFILE.get('resume'):
    contact_items+=f'<div class="contact-item"><div><small>CV</small><a href="{PROFILE["resume"]}" target="_blank" rel="noopener noreferrer">Read my CV</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'
contact=f'<main id="main"><div class="wrap">{contact_hero}<div class="contact-layout"><div class="contact-list">{contact_items}</div><div>{portrait(True)}</div></div></div></main>'
write('/contact/',page('Contact','Contact Frederick Searancke by email or phone.',contact,current='contact'))

print('Built',len(list(OUT.rglob('index.html'))),'portfolio pages.')
