"""Install responsive campaign motion into the native Shopify hero."""
import pathlib,re,json
R=pathlib.Path(__file__).resolve().parents[1]
def write(path,s):(R/path).write_text(s,encoding='utf-8')
p=R/'theme/sections/hero.liquid';s=p.read_text(encoding='utf-8')
media='''<div class="hero-image" data-hero-media>{% if section.settings.image != blank %}{{ section.settings.image | image_url: width: 2400 | image_tag: fetchpriority: 'high', widths: '800,1200,1800,2400', sizes: '100vw' }}{% else %}<img src="{{ 'campaign-01.png' | asset_url }}" width="1672" height="941" alt="Essaint white tee and pale blue striped trousers in an architectural campaign setting" fetchpriority="high">{% endif %}{% if section.settings.animate %}{% assign desktop_video = 'essaint-hero-desktop.mp4' | asset_url %}{% assign mobile_video = 'essaint-hero-mobile.mp4' | asset_url %}{% if section.settings.video != blank %}{% for source in section.settings.video.sources %}{% if source.format == 'mp4' %}{% assign desktop_video = source.url %}{% break %}{% endif %}{% endfor %}{% assign mobile_video = desktop_video %}{% endif %}{% if section.settings.mobile_video != blank %}{% for source in section.settings.mobile_video.sources %}{% if source.format == 'mp4' %}{% assign mobile_video = source.url %}{% break %}{% endif %}{% endfor %}{% endif %}<video data-hero-video data-desktop="{{ desktop_video }}" data-mobile="{{ mobile_video }}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>{% endif %}</div>'''
s=re.sub(r'<div class="hero-image">.*?</div>',media,s,count=1,flags=re.S)
if 'data-motion-toggle' not in s:s=s.replace('<div class="hero-foot">','<button class="motion-toggle" data-motion-toggle type="button" hidden aria-label="Play campaign video"><span data-motion-icon aria-hidden="true">▶</span> <span data-motion-label>PLAY FILM</span></button><div class="hero-foot">',1)
schema=json.loads(re.search(r'{% schema %}(.*?){% endschema %}',s,re.S)[1]);schema['settings']=[x for x in schema['settings'] if x['id'] not in ['animate','video','mobile_video']]+[{'type':'checkbox','id':'animate','label':'Animate the campaign hero','default':True},{'type':'video','id':'video','label':'Desktop video (optional override)'},{'type':'video','id':'mobile_video','label':'Mobile video (optional override)'}]
s=re.sub(r'{% schema %}.*?{% endschema %}','{% schema %}'+json.dumps(schema)+'{% endschema %}',s,flags=re.S);write('theme/sections/hero.liquid',s)
layout=(R/'theme/layout/theme.liquid').read_text(encoding='utf-8')
if "'hero-motion.js'" not in layout:layout=layout.replace('</head>',"<script src=\"{{ 'hero-motion.js' | asset_url }}\" defer></script>{{ 'hero-motion.css' | asset_url | stylesheet_tag }}</head>")
write('theme/layout/theme.liquid',layout)
index=json.loads((R/'theme/templates/index.json').read_text());index['sections']['0']['settings']['animate']=True;write('theme/templates/index.json',json.dumps(index,indent=2))
config=json.loads((R/'theme/config/settings_schema.json').read_text());config[0]['theme_version']='2.2.0';write('theme/config/settings_schema.json',json.dumps(config,indent=2))
print('Installed hero motion settings, controls and poster fallback.')
