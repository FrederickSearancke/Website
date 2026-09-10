from pathlib import Path
import json
from html import escape, unescape
import re
from authored import author, approved, document, comparison, paragraph_text

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
PROFILE = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
BASE = '/projects/gpt-finetuning/'
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
        return f'<img class="{"contact-portrait" if large else "portrait"}" src="{escape(PROFILE["portrait"])}" alt="Frederick Searancke" width="{300 if large else 62}" height="{375 if large else 62}">'
    return '<div class="portrait monogram" aria-label="Frederick Searancke initials">FS</div>' if not large else ''

def header(current=''):
    def nav(label, url, key):
        return f'<a href="{url}"' + (' aria-current="page"' if current == key else '') + f'>{label}</a>'
    resume = f'<a class="nav-resume" href="{PROFILE["resume"]}" target="_blank" rel="noopener noreferrer">Resume <span aria-hidden="true">↗</span></a>' if PROFILE.get('resume') else ''
    return f'''<a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header"><div class="wrap header-inner">
      <button class="menu-toggle" aria-label="Toggle navigation" aria-expanded="false" aria-controls="main-navigation">Menu <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 7h18M3 16h18"/></svg></button>
      <nav class="main-nav" id="main-navigation" aria-label="Main navigation">
      {nav('Projects','/#projects','projects')}{nav('Skills','/#skills','skills')}{nav('About me','/about/','about')}{nav('Contact','/contact/','contact')}{resume}
      </nav></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap footer-inner"><a class="footer-name" href="/">Frederick Searancke</a><div class="footer-links"><a href="/#projects">Projects</a><a href="/contact/">Get in touch</a>{social_links()}</div></div></footer>'''

def page(title, description, body, *, home=False, current=''):
    title = re.sub(r'<[^>]+>', ' ', title).strip().rstrip('.')
    description = unescape(re.sub(r'<[^>]+>', '', description))
    preload = '<link rel="preload" as="image" href="/assets/vectors.png">' if home else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)} — Frederick Searancke</title><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#101e2b"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css">{preload}<script src="/app.js" defer></script></head><body class="{'home' if home else 'inner-page'}">{header(current)}{body}{footer()}</body></html>'''

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

def chapter_nav(active='overview'):
    menu = f'<a href="{BASE}" class="{"active" if active=="overview" else ""}"'+(' aria-current="page"' if active=='overview' else '')+'><span>—</span>Project overview</a>'
    for i,(slug,title,desc) in enumerate(CHAPTERS,1):
        menu += f'<a href="{BASE}{slug}/" class="{"active" if active==slug else ""}"'+(' aria-current="page"' if active==slug else '')+f'><span>{i:02}</span>{title}</a>'
    return f'<aside class="chapter-nav"><h2>Explore the project</h2><nav class="chapter-links" aria-label="Project chapters">{menu}</nav><a class="chapter-back" href="/#projects">← All projects</a></aside>'

def gpt_page(title,desc,article,active='overview',label='Machine learning · Applied AI'):
    breadcrumb='<div class="breadcrumbs"><a href="/#projects">All projects</a><span aria-hidden="true">/</span><a href="/projects/gpt-finetuning/">GPT fine-tuning</a></div>'
    hero=project_hero(label,title,desc,['Python','Fine-tuning','Retrieval','Data engineering'])
    return page(title,desc,f'<main id="main"><div class="wrap">{breadcrumb}{hero}<div class="reading-layout">{chapter_nav(active)}<article class="article">{article}</article></div></div></main>',current='projects')

projects = [
 {'slug':'gpt-finetuning','category':'machine-learning','label':'Machine learning','meta':'4 chapters','image':'vectors.png','imageclass':'vector','alt':'Projection of product and policy embeddings','title':'GPT-4o fine-tuning<br>for customer live chat','desc':author('gpt-integration-p01-b03','span',excerpt='I built a Python application that combined the fine-tuned model with retrieval of product and policy information.'),'stat':'74,000+','statlabel':'messages parsed'},
 {'slug':'blender-pipeline','category':'automation','label':'Automation','meta':'Python + Blender','image':'artwork-to-relief.png','imageclass':'blender','alt':'Generated bee and honeycomb relief on a clay roller model','title':'From artwork to<br>3D-printable rollers','desc':approved('blender-card-intro'),'stat':'£1,100+','statlabel':'in product sales'},
 {'slug':'maze-solver','category':'algorithms','label':'Algorithms','meta':'Java','image':'maze-first.png','imageclass':'maze','alt':'Maze from the route-memory controller project','title':'A maze solver<br>that remembers its route','desc':author('maze-p01-b02','span',excerpt='The final controller could remember a successful route and use it to reach the target more directly on subsequent runs.'),'stat':'85% &amp; 87%','statlabel':'coursework marks'},
]

rows=''
for i,p in enumerate(projects,1):
    rows+=f'''<a class="project-row" href="/projects/{p['slug']}/" data-category="{p['category']}"><div class="project-image {p['imageclass']}"><img src="/assets/{p['image']}" alt="{p['alt']}" loading="lazy" decoding="async" width="530" height="352"></div><div class="project-copy"><div class="project-meta"><span class="index">0{i}</span><span>{p['label']}</span><span>·</span><span>{p['meta']}</span></div><h3>{p['title']}</h3><p>{p['desc']}</p></div><div class="project-stat"><strong>{p['stat']}</strong><small>{p['statlabel']}</small><span class="row-arrow" aria-hidden="true">↗</span></div></a>'''

visual_dialog=f'''<dialog class="visual-inspector" id="visual-inspector" aria-labelledby="visual-inspector-title"><form method="dialog" class="visual-close-form"><button class="visual-close" aria-label="Close visual explanation" autofocus><svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button></form><div class="visual-inspector-layout"><div class="visual-inspector-figure"><img src="/assets/vectors.png" alt="Two-dimensional projection of product names, short and full descriptions, and company information embeddings" width="2048" height="1536" loading="lazy"></div><div class="visual-inspector-copy"><p class="visual-inspector-kicker">Behind the visual</p><h2 id="visual-inspector-title">A map of the AI’s knowledge.</h2>{approved('rag-knowledge-base','p',excerpt='I implemented the knowledge base in Python as a JSONL dataset, combining product information with company policies and staff training documents.')}{approved('rag-vector-projection','p')}<a class="visual-chapter-link" href="/projects/gpt-finetuning/retrieval/#vector-projection">How I built it <span aria-hidden="true">↗</span></a></div></div></dialog>'''

home=f'''<main id="main"><section class="hero project-first" aria-labelledby="home-title"><img class="hero-art" src="/assets/vectors.png" width="2048" height="1536" alt="" fetchpriority="high"><div class="hero-shade"></div><div class="wrap hero-inner"><p class="featured-label">Featured project <span aria-hidden="true">/</span> Machine learning</p><h1 id="home-title">GPT-4o fine-tuning<br>for customer<br>live chat<span style="color:var(--accent)">.</span></h1><div class="hero-cta"><a class="button primary" href="#projects">View projects <span aria-hidden="true">↓</span></a><a class="featured-project-button" href="/projects/gpt-finetuning/">Learn about this project <span aria-hidden="true">↗</span></a></div><div class="hero-bottom"><a class="scroll-link" href="#projects"><span aria-hidden="true">↓</span> Scroll to projects</a><a class="visual-trigger" href="/projects/gpt-finetuning/retrieval/#vector-projection" data-open-visual aria-haspopup="dialog" aria-controls="visual-inspector"><span class="visual-trigger-icon" aria-hidden="true">+</span><span>Explore this visual</span></a></div></div></section>{visual_dialog}
<section class="section wrap" id="projects" aria-labelledby="projects-title"><p class="section-label">Projects</p><div class="section-heading"><h2 id="projects-title">Selected work<span style="color:var(--accent)">.</span></h2></div><div class="filter-bar" role="group" aria-label="Filter projects"><button class="filter" data-filter="all" aria-pressed="true">All projects</button><button class="filter" data-filter="machine-learning" aria-pressed="false">Machine learning</button><button class="filter" data-filter="automation" aria-pressed="false">Automation</button><button class="filter" data-filter="algorithms" aria-pressed="false">Algorithms</button></div><p id="filter-status" class="visually-hidden" aria-live="polite">3 projects shown</p><div class="project-list">{rows}</div></section>
<section class="identity-section wrap" aria-label="About the author"><div class="identity-details">{portrait()}<div><h2>Frederick Searancke</h2><p>Quant Researcher <span aria-hidden="true">·</span> Computer Science, University of Warwick</p></div></div><a class="identity-about" href="/about/">About me <span aria-hidden="true">↗</span></a></section>
<section class="section skills-section wrap" id="skills" aria-labelledby="skills-title"><div class="skills-layout"><div><p class="section-label">Technical toolkit</p><h2 id="skills-title">Skills in practice.</h2></div><div class="skill-groups">
<div class="skill-group"><h3>Machine learning</h3><ul class="skill-list"><li>EBM model training</li><li>Loss functions &amp; regularisation</li><li>Overfitting &amp; underfitting diagnostics</li><li>LLM fine-tuning &amp; RAG</li></ul></div>
<div class="skill-group"><h3>Quantitative research</h3><ul class="skill-list"><li>Walk-forward backtesting</li><li>Hypothesis testing &amp; null models</li><li>Parameter sweeps &amp; overfitting</li><li>Volatility &amp; slippage modelling</li></ul></div>
<div class="skill-group"><h3>Software &amp; data</h3><ul class="skill-list"><li>Python and Java</li><li>SQL</li><li>Data pipelines</li><li>Feature engineering</li></ul></div>
<div class="skill-group"><h3>Building systems</h3><ul class="skill-list"><li>End-to-end project delivery</li><li>Modular system architecture</li><li>TCP APIs · IBKR TWS</li><li>REST API integration</li></ul></div>
</div></div></section></main>'''
write('/',page('Projects & research','Projects in machine learning, software automation and algorithms by Frederick Searancke.',home,home=True))


overview='<h2>Overview</h2>'
overview+=author('gpt-formatting-p01-b03',excerpt='I made a fine-tuned machine learning model to accurately answer customer live chats as well as a trained human with up-to-date company policy and product information that was performant enough to converse with real customers in real time. I did this work over the summer of 2024.')
overview+=summary([('Data processing','74,000+ messages'),('Retrieval index','2,402 embeddings'),('Project context','Summer 2024')])
overview+='<h2>Explore the project</h2><div class="chapter-cards">'
for i,(slug,title,desc) in enumerate(CHAPTERS,1):
    overview+=f'<a class="chapter-card" href="{BASE}{slug}/"><span class="chapter-num">{i:02}</span><div><h3>{title}</h3><p>{desc}</p></div><span class="arrow" aria-hidden="true">↗</span></a>'
overview+='</div><h2>The application</h2>'+author('gpt-integration-p01-b03')
overview+='<h2>Evaluation and outcome</h2>'+approved('gpt-evaluation-outcome','p')
write(BASE,gpt_page('GPT-4o fine-tuning<br>for customer live chat.',author('gpt-integration-p01-b03','span',excerpt='I built a Python application that combined the fine-tuned model with retrieval of product and policy information.'),overview))

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
    pagination='<nav class="chapter-pagination" aria-label="Adjacent chapters">'
    prev = (BASE,'Project overview') if i==0 else (BASE+CHAPTERS[i-1][0]+'/',CHAPTERS[i-1][1])
    pagination+=f'<a href="{prev[0]}"><small>← Previous</small>{prev[1]}</a>'
    if i<3:
        pagination+=f'<a href="{BASE}{CHAPTERS[i+1][0]}/"><small>Next →</small>{CHAPTERS[i+1][1]}</a>'
    else:
        pagination+='<a href="/#projects"><small>Continue exploring →</small>All projects</a>'
    pagination+='</nav>'
    write(BASE+slug+'/',gpt_page(title+'.',desc,chapter_bodies[slug]+pagination,slug,f'GPT fine-tuning · Part {i+1:02} of 04'))

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

about_hero=project_hero('About me','Beyond the projects.','Computer science at Warwick, an interest in quantitative research, and time away from the screen.',[])
about=f'''<main id="main"><div class="wrap">{about_hero}<div class="about-copy"><h2>Thinking through making.</h2><p>My projects span applied machine learning, software automation and algorithms. I enjoy taking a problem apart, building something that works, and understanding the decisions that shape the result.</p><p>I study Computer Science at the University of Warwick. This portfolio collects my work and the technical detail behind it.</p><h2 style="margin-top:45px">Away from the screen.</h2><p>My interests include fencing, skiing and boxing. I hold a BASI Level 1 ski instructor qualification and have completed the Gold Duke of Edinburgh’s Award.</p><div style="margin-top:35px"><a class="button" href="/contact/">Get in touch <span aria-hidden="true">↗</span></a></div></div></div></main>'''
write('/about/',page('About me','About Frederick Searancke: Computer Science at Warwick, quantitative research interests, and sport.',about,current='about'))

contact_hero=project_hero('Contact','Let’s get in touch.','For conversations about quantitative research, software, or any of the projects here.',[])
contact_items=f'''<div class="contact-item"><div><small>Email</small><a href="mailto:{escape(PROFILE['email'])}">{escape(PROFILE['email'])}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div><div class="contact-item"><div><small>Phone</small><a href="tel:{escape(PROFILE['phoneHref'])}">{escape(PROFILE['phone'])}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'''
for label,key in [('LinkedIn','linkedin'),('GitHub','github')]:
    if PROFILE.get(key):
        contact_items+=f'<div class="contact-item"><div><small>{label}</small><a href="{escape(PROFILE[key])}" target="_blank" rel="noopener noreferrer">Find me on {label}</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'
if PROFILE.get('resume'):
    contact_items+=f'<div class="contact-item"><div><small>Resume</small><a href="{PROFILE["resume"]}" target="_blank" rel="noopener noreferrer">Read my resume</a></div><span class="external-arrow" aria-hidden="true">↗</span></div>'
contact=f'<main id="main"><div class="wrap">{contact_hero}<div class="contact-layout"><div class="contact-list">{contact_items}</div><div>{portrait(True)}</div></div></div></main>'
write('/contact/',page('Contact','Contact Frederick Searancke by email or phone.',contact,current='contact'))

print('Built',len(list(OUT.rglob('index.html'))),'portfolio pages.')
