"""Generate the two static policy pages; uses only the Python standard library."""
import json
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parent
content = json.loads((root / "content.json").read_text())
style = """+:root { color-scheme: light dark; font-family: system-ui, -apple-system, sans-serif; }
body { margin: 0; background: #f8f8f6; color: #292722; }
main { max-width: 76ch; margin: auto; padding: 32px 24px 64px; }
nav { display: flex; gap: 20px; margin-bottom: 40px; }
a { color: #285f7b; text-underline-offset: .2em; overflow-wrap: anywhere; }
h1 { font-size: clamp(1.8rem, 5vw, 2.6rem); line-height: 1.2; letter-spacing: -.035em; }
h2 { font-size: 1.25rem; margin: 36px 0 12px; }
p { font-size: 1rem; line-height: 1.75; }
.date, footer { color: #625f5b; }
footer { margin-top: 44px; padding-top: 20px; border-top: 1px solid #deded9; }
a:focus-visible { outline: 3px solid currentColor; outline-offset: 4px; }
@media (prefers-color-scheme: dark) {
 body { background: #191a18; color: #eeefea; }
 a { color: #9ecfe5; } .date, footer { color: #c2c2ba; }
 footer { border-color: #4a4c45; }
}
"""
for lang, data in content.items():
    english, russian = ("./", "./ru/") if lang == "en" else ("../", "./")
    sections = "\n".join(
        f'<section aria-labelledby="section-{i}"><h2 id="section-{i}">{escape(title)}</h2><p>{body}</p></section>'
        for i, (title, body) in enumerate(data["sections"], 1)
    )
    output = root / ("index.html" if lang == "en" else "ru/index.html")
    output.parent.mkdir(exist_ok=True)
    output.write_text(f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(data['title'])} — Green Key Universe">
<title>{escape(data['title'])}</title>
<style>{style}</style>
</head>
<body><main>
<nav aria-label="Language"><a href="{english}" lang="en" hreflang="en">English</a><a href="{russian}" lang="ru" hreflang="ru">Русский</a></nav>
<h1>{escape(data['title'])}</h1>
<p class="date">{escape(data['date'])}</p>
<p>{data['intro']}</p>
{sections}
<footer>LifeBalance · Green Key Universe</footer>
</main></body></html>
''', encoding="utf-8")
