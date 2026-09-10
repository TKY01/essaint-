import pathlib
R = pathlib.Path(__file__).resolve().parents[1]
p = R / 'theme/layout/theme.liquid'
s = p.read_text(encoding='utf-8')
if 'mobile.css' not in s:
    s = s.replace('</head>', "{{ 'mobile.css' | asset_url | stylesheet_tag }}</head>")
s = s.replace('width=device-width,initial-scale=1"', 'width=device-width,initial-scale=1,viewport-fit=cover"')
p.write_text(s, encoding='utf-8')
