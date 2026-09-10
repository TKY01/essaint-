import pathlib,zipfile,shutil,json
R=pathlib.Path(__file__).resolve().parents[1]
with zipfile.ZipFile(R/'essaint-shopify-theme.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((R/'theme').rglob('*')):
  if p.is_file() and not p.name.startswith('.'):z.write(p,p.relative_to(R/'theme'))
# The Shopify package is delivered separately; Sites has a 25 MiB per-file limit.
preview_zip=R/'dist/essaint-shopify-theme.zip'
if preview_zip.is_file():preview_zip.unlink()
shutil.copy(R/'README.md',R/'dist/INSTALL.md')
with zipfile.ZipFile(R/'essaint-catalog-export.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in ['products.json','catalog.json','products.csv','provenance.json']:z.write(R/'data'/f,f)
print('Packaged Shopify theme and catalog export.')
campaign_files=[R/'theme/assets'/f'campaign-0{i}.png' for i in range(1,4)]+[R/'theme/assets/essaint-hero-desktop.mp4',R/'theme/assets/essaint-hero-mobile.mp4',R/'deliverables/video-specification.json']
if all(p.exists() for p in campaign_files):
 with zipfile.ZipFile(R/'essaint-campaign-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in campaign_files:z.write(p,p.name)
 print('Packaged three campaign images and both hero video versions.')
