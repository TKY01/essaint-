import json,pathlib,re,shutil,html
R=pathlib.Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
P=json.loads((R/'data/catalog.json').read_text());by={p['handle']:p for p in P}
shutil.copytree(R/'theme/assets',D/'assets',dirs_exist_ok=True)
def basic(s):
 s=re.sub(r'{% schema %}.*?{% endschema %}','',s,flags=re.S)
 for a,b in {'{{ routes.root_url }}':'/','{{ routes.all_products_collection_url }}':'#shop','{{ routes.search_url }}':'#shop','{{ cart.item_count }}':'0',"{{ 'now' | date: '%Y' }}":'2026'}.items():s=s.replace(a,b)
 s=re.sub(r"{{ '([^']+)' \| asset_url }}",r'assets/\1',s)
 return s
def read(n):return basic((R/'theme/sections'/f'{n}.liquid').read_text())
def card(p):
 title=html.escape(p['title']);price=float(p['variants'][0]['price']);compare=float(p['variants'][0]['compare_at_price'] or 0)
 sold=not any(v['available'] for v in p['variants']);badge='Sold out' if sold else 'The good-price edit' if compare>price else ''
 alternate=f'<img class="alternate" src="assets/{p["images"][1]["local"]}" alt="{title}" loading="lazy">' if len(p['images'])>1 else ''
 return f'<article class="product-card"><a class="product-photo" href="#product/{p["handle"]}"><img src="assets/{p["images"][0]["local"]}" alt="{title}" loading="lazy">{alternate}<span class="badge">{badge}</span></a><button class="quick-add" data-product="{p["handle"]}" aria-label="Choose options for {title}">+</button><div class="product-meta"><a href="#product/{p["handle"]}">{title}</a><span>${price:.2f}'+(f'<s>${compare:.2f}</s>' if compare>price else '')+f'</span></div><p class="product-options">'+html.escape(' · '.join(p['options'][0]['values']))+'</p></article>'
header=read('header');icon=(R/'theme/snippets/icon.liquid').read_text();header=header.replace("{% render 'icon', name: 'search' %}",'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>').replace("{% render 'icon', name: 'bag' %}",'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 7h14l1 14H4L5 7Z"/><path d="M8 8V6a4 4 0 0 1 8 0v2"/></svg>')
hero=read('hero').replace('{{ section.settings.heading }}','Everyday.<br>Anything but<br>ordinary.');hero=re.sub(r'{% if section.settings.image != blank %}.*?{% else %}(.*?){% endif %}',r'\1',hero,flags=re.S)
essentials=read('essentials');essentials=re.sub(r'{% assign featured.*?{% endfor %}',''.join(card(P[i]) for i in [3,10,2,6]),essentials,flags=re.S)
bundles=read('bundles');items=''
for i,(title,handle) in enumerate([('The off-duty pair','milano-striped-pants-dropping-next-week'),('The slow-day set','linen-pants-unisex'),('The city uniform','tailored-pants')],1):
 top=by['over-size-t-shirt'];bottom=by[handle]
 items+=f'<article class="bundle-card"><div class="bundle-images"><img src="assets/{top["images"][0]["local"]}" alt="Oversized T-Shirt" loading="lazy"><img src="assets/{bottom["images"][0]["local"]}" alt="{html.escape(bottom["title"])}" loading="lazy"><span class="bundle-number">0{i} / THE OUTFIT EDIT</span></div><div class="bundle-info"><div><h3>{title}</h3><p>Oversized T-Shirt + {html.escape(bottom["title"])}</p></div><button class="text-link" data-bundle="over-size-t-shirt,{handle}" data-title="{title}">Build your set ↗</button></div></article>'
bundles=re.sub(r'{% for block.*?{% endfor %}',items,bundles,flags=re.S)
footer=read('footer');footer=re.sub(r'{% for policy.*?{% endfor %}','<a href="https://essaint.com/policies/shipping-policy" target="_blank" rel="noopener">Shipping policy ↗</a><a href="https://essaint.com/policies/refund-policy" target="_blank" rel="noopener">Exchanges ↗</a>',footer,flags=re.S);footer=re.sub(r"{% form 'customer' %}.*?{% endform %}",'<p style="margin-top:20px">Join the list on our current store.</p><a class="text-link" href="https://essaint.com/#ContactFooter" target="_blank" rel="noopener">Visit Essaint ↗</a>',footer,flags=re.S);footer=footer.replace('href="/pages/contact"','href="https://essaint.com/pages/contact" target="_blank" rel="noopener"')
overlays=basic((R/'theme/snippets/overlays.liquid').read_text())
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Essaint — Everyday, elevated</title><meta name="description" content="Discover Essaint's everyday wardrobe. Relaxed tees, effortless trousers, and curated outfit edits. Crafted in Lebanon."><link rel="stylesheet" href="assets/essaint.css"><script>window.Essaint={{preview:true,root:'/',currency:'USD'}};</script><script src="assets/catalog.js" defer></script><script src="assets/essaint.js" defer></script><script src="assets/preview.js" defer></script></head><body><a class="skip-link" href="#MainContent">Skip to content</a><div class="preview-note">PRIVATE DESIGN PREVIEW · <a href="essaint-shopify-theme.zip" download>Download Shopify theme</a> · Checkout activates on Shopify</div>{header}<main id="MainContent"><div id="home-view">{hero}{essentials}{bundles}{read('story')}</div><div id="route-view" class="preview-view" hidden></div></main>{footer}{overlays}</body></html>'''
assert '{{' not in page and '{%' not in page
(D/'index.html').write_text(page,encoding='utf-8')
catalog=[]
for p in P:
 v=[{**v,'price':round(float(v['price'])*100),'compare_at_price':round(float(v['compare_at_price'] or 0)*100)} for v in p['variants']]
 catalog.append({**p,'description':p['body_html'],'featured_image':'assets/'+p['images'][0]['local'],'images':['assets/'+x['local'] for x in p['images']],'variants':v,'card':card(p)})
(D/'assets/catalog.js').write_text('window.EssaintCatalog='+json.dumps(catalog)+';',encoding='utf-8')
shutil.copy(R/'preview/preview.js',D/'assets/preview.js')
print('Preview built using actual theme styles and shared commerce UI.')
