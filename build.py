from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
FIELDS = ("category", "title", "summary", "concept", "example", "pitfall")


def read_notes():
    notes, used_orders = [], set()
    for path in sorted((ROOT / "notes").glob("*.json")):
        note = json.loads(path.read_text(encoding="utf-8-sig"))
        slug = path.stem
        if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", slug) or slug == "index":
            raise ValueError(f"Invalid filename: {path.name}")
        order = note.get("order")
        if type(order) is not int or order < 1 or order in used_orders:
            raise ValueError(f"Invalid or duplicate order: {path.name}")
        if any(not isinstance(note.get(k), str) or not note[k].strip() for k in FIELDS):
            raise ValueError(f"Missing text field: {path.name}")
        refs = note.get("references")
        if not isinstance(refs, list) or not refs or any(
            not isinstance(r, dict) or not str(r.get("title", "")).strip()
            or not re.fullmatch(r"https://[^/\s]+(?:/\S*)?", str(r.get("url", "")))
            for r in refs
        ):
            raise ValueError(f"Invalid references: {path.name}")
        used_orders.add(order)
        notes.append((slug, note))
    return sorted(notes, key=lambda pair: pair[1]["order"])


def page(title, body):
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}｜醫電訊號筆記</title>
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header><div class="wrap"><a href="index.html">醫電訊號筆記</a></div></header>
<main class="wrap">{body}</main>
<footer class="wrap">醫電所學習筆記 · 李宥辰</footer>
</body>
</html>
"""


def article(note):
    sections = "".join(
        f"<section><h2>{heading}</h2><p>{escape(note[key])}</p></section>"
        for heading, key in (("核心觀念", "concept"), ("手算例子", "example"), ("容易混淆的地方", "pitfall"))
    )
    links = "".join(
        f'<li><a href="{escape(ref["url"])}">{escape(ref["title"])}</a></li>'
        for ref in note["references"]
    )
    return (f'<article><p class="tag">{escape(note["category"])}</p>'
            f'<h1>{escape(note["title"])}</h1><p class="lead">{escape(note["summary"])}</p>'
            f'{sections}<section><h2>延伸閱讀</h2><ul>{links}</ul></section></article>'
            '<p><a href="index.html">← 返回筆記索引</a></p>')


def main():
    notes = read_notes()
    cards = "".join(
        f'<li><span class="tag">{escape(n["category"])}</span>'
        f'<h2><a href="{slug}.html">{escape(n["title"])}</a></h2>'
        f'<p>{escape(n["summary"])}</p></li>'
        for slug, n in notes
    )
    DOCS.joinpath("index.html").write_text(page("首頁",
        '<h1>醫電訊號筆記</h1><p class="lead">從取樣、振幅到頻域，每篇用一道手算例題拆解一個觀念。</p>'
        f'<ul class="cards">{cards}</ul>'), encoding="utf-8")
    for slug, note in notes:
        DOCS.joinpath(f"{slug}.html").write_text(page(note["title"], article(note)), encoding="utf-8")
    print(f"Built index and {len(notes)} notes")


if __name__ == "__main__":
    main()
