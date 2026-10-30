"""Build a dependency-free page with its catalog embedded for local/offline use."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
catalog=json.loads((root/'src/catalog.json').read_text())
body=(root/'src/table.html').read_text().replace('/*CATALOG*/',json.dumps(catalog,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
(root/'index.html').write_text('<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="referrer" content="no-referrer"><title>אינדקס שאלות בגרות במדעי המחשב</title></head><body>\n'+body+'\n</body></html>\n')
print(f"Built {len(catalog['questions'])} questions")
