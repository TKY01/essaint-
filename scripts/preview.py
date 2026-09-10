import json,pathlib,re,shutil,html
R=pathlib.Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
P=json.loads((R/'data/catalog.json').read_text());by={p['handle']:p for p in P}
shutil.copytree(R/'theme/assets',D/'assets',dirs_exist_ok=True)
def basic(s):
 s=re.sub(r'{% schema %}.*?{% endschema %}','',s,flags=re.S)
 for a,b in {'{{ routes.root_url }}':'/','{{ routes.all_products_collection_url }}':'#shop','{{ routes.search_url }}':'#shop','{{ cart.item_count }}':'0','{{ cart.currency.iso_code }}':'USD','{{ section.id }}':'preview',"{{ 'now' | date: '%Y' }}":'2026'}.items():s=s.replace(a,b)
 s=re.sub(r"{{ '([^']+)' \| asset_url }}",r'assets/\1',s)
 return s
def read(n):return basic((R/'theme/sections'/f'{n}.liquid').read_text(encoding='utf-8'))
def card(p):
 title=html.escape(p['title']);price=float(p['variants'][0]['price']);compare=float(p['variants'][0]['compare_at_price'] or 0)
 sold=not any(v['available'] for v in p['variants']);badge='SOLD OUT' if sold else 'PRICE DROP' if compare>price else ''
 alternate=f'<img class="alternate" src="assets/{p["images"][1]["local"]}" alt="{title}" loading="lazy">' if len(p['images'])>1 else ''
 kind='tees' if 't-shirt' in p['title'].lower() else 'bottoms'
 return f'<article class="product-card" data-kind="{kind}"><div class="product-media"><a class="product-photo" href="#product/{p["handle"]}"><img src="assets/{p["images"][0]["local"]}" alt="{title}" loading="lazy">{alternate}<span class="badge">{badge}</span></a><button class="quick-add" data-product="{p["handle"]}" aria-label="Choose options for {title}"><span>QUICK ADD</span><b>+</b></button></div><div class="product-meta"><a href="#product/{p["handle"]}">{title}</a><span>${price:.2f}'+(f'<s>${compare:.2f}</s>' if compare>price else '')+f'</span></div><p class="product-options">'+html.escape(' / '.join(p['options'][0]['values']))+'</p></article>'
header=read('header').replace("{% render 'icon', name: 'search' %}",'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>')
hero=read('hero').replace('{{ section.settings.heading }}','OFF DUTY.').replace('{{ section.settings.subheading }}','On purpose.');hero=re.sub(r'{% if section.settings.image != blank %}.*?{% else %}(.*?){% endif %}',r'\1',hero,flags=re.S)
essentials=read('essentials');order=[3,4,10,6]+[i for i in range(len(P)) if i not in [3,4,10,6]]
essentials=re.sub(r'{% assign featured.*?{% endfor %}',''.join(card(P[i]) for i in order),essentials,flags=re.S)
bundles=read('bundles')
for part,match,default in [('top',True,'over-size-t-shirt'),('bottom',False,'milano-striped-pants-dropping-next-week')]:
 options=''.join(f'<option value="{p["handle"]}" '+('selected' if p['handle']==default else '')+'>'+html.escape(p['title'])+'</option>' for p in P if ('t-shirt' in p['title'].lower())==match)
 bundles=re.sub(r'(<select[^>]*data-studio-product="'+part+r'"[^>]*>).*?(</select>)',lambda m:m[1]+options+m[2],bundles,flags=re.S)
presets=''.join(f'<button data-studio-preset="over-size-t-shirt,{handle}">{title} ↗</button>' for title,handle in [('The striped set','milano-striped-pants-dropping-next-week'),('The linen set','linen-pants-unisex'),('The city set','tailored-pants')])
bundles=re.sub(r'{% for block.*?{% endfor %}',presets,bundles,flags=re.S)
footer=read('footer');footer=re.sub(r'{% for policy.*?{% endfor %}','<a href="https://essaint.com/policies/shipping-policy" target="_blank" rel="noopener">Shipping policy ↗</a><a href="https://essaint.com/policies/refund-policy" target="_blank" rel="noopener">Exchanges ↗</a><a href="https://essaint.com/policies/privacy-policy" target="_blank" rel="noopener">Privacy policy ↗</a>',footer,flags=re.S)
footer=re.sub(r"{% form 'customer' %}.*?{% endform %}",'<a class="text-link" style="margin-top:22px" href="https://essaint.com/#ContactFooter" target="_blank" rel="noopener">JOIN THE LIST AT ESSAINT.COM ↗</a>',footer,flags=re.S)
footer=footer.replace('href="/pages/contact"','href="https://essaint.com/pages/contact" target="_blank" rel="noopener"')
overlays=basic((R/'theme/snippets/overlays.liquid').read_text(encoding='utf-8'))
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ESSAINT — Off duty. On purpose.</title><meta name="description" content="Essaint. Easy silhouettes, a different kind of presence. Shop tees, trousers and build your own everyday uniform."><link rel="stylesheet" href="assets/essaint.css"><script>window.Essaint={{preview:true,root:'/',currency:'USD'}};</script><script src="assets/catalog.js" defer></script><script src="assets/essaint.js" defer></script><script src="assets/studio.js" defer></script><script src="assets/preview.js" defer></script></head><body><a class="skip-link" href="#MainContent">Skip to content</a>{header}<main id="MainContent"><div id="home-view">{hero}{essentials}{bundles}{read('story')}</div><div id="route-view" class="preview-view" hidden></div></main>{footer}<aside class="preview-note">PRIVATE DESIGN PREVIEW · <a href="essaint-shopify-theme.zip" download>DOWNLOAD SHOPIFY THEME</a> · Checkout activates on Shopify</aside>{overlays}</body></html>'''
assert '{{' not in page and '{%' not in page
(D/'index.html').write_text(page,encoding='utf-8')
catalog=[]
for p in P:
 v=[{**v,'price':round(float(v['price'])*100),'compare_at_price':round(float(v['compare_at_price'] or 0)*100)} for v in p['variants']]
 catalog.append({**p,'description':p['body_html'],'featured_image':'assets/'+p['images'][0]['local'],'images':['assets/'+x['local'] for x in p['images']],'variants':v,'card':card(p)})
(D/'assets/catalog.js').write_text('window.EssaintCatalog='+json.dumps(catalog)+';',encoding='utf-8')
shutil.copy(R/'preview/preview.js',D/'assets/preview.js')
print('Built redesigned preview, shared Shopify styles, and outfit studio.')
