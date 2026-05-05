#!/usr/bin/env python3
"""Build the Foundry Stack static site for GitHub Pages."""
from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "fab-glossary"
OUT = ROOT / "docs"
BASE_PATH = "/fab-glossary/"
REPO_URL = "https://github.com/manuelarceaguirre/fab-glossary"

CATEGORY_ORDER = [
    "market-structure",
    "fab-system",
    "process-stack",
    "operating-model",
    "metrics",
    "models",
]
RESERVED_TOP_LEVEL = {"readme", "contributors", "license"}


@dataclass
class Page:
    title: str
    slug: str
    source: Path
    body_md: str
    children: list["Page"] = field(default_factory=list)

    @property
    def url(self) -> str:
        return BASE_PATH if self.slug == "" else f"{BASE_PATH}{self.slug}/"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("---\n"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body.lstrip("\n")
    return {}, text


def read_page(path: Path, slug: str) -> Page:
    meta, body = split_frontmatter(path.read_text())
    title = meta.get("title") or slug.replace("-", " ").title() or "Foundry Stack"
    return Page(title=title, slug=slug, source=path, body_md=body)


def discover_category_stems() -> list[str]:
    stems = {
        path.stem
        for path in CONTENT.glob("*.md")
        if path.stem.lower() not in RESERVED_TOP_LEVEL
    }
    ordered = [stem for stem in CATEGORY_ORDER if stem in stems]
    ordered.extend(sorted(stems - set(ordered)))
    return ordered


def build_tree() -> Page:
    home = read_page(CONTENT / "readme.md", "")

    categories: list[Page] = []
    for stem in discover_category_stems():
        path = CONTENT / f"{stem}.md"
        category = read_page(path, stem)
        child_dir = CONTENT / stem
        if child_dir.exists():
            category.children = [
                read_page(child, f"{stem}/{child.stem}")
                for child in sorted(child_dir.glob("*.md"))
            ]
        categories.append(category)

    contributors = CONTENT / "contributors.md"
    home.children = categories
    if contributors.exists():
        home.children.append(read_page(contributors, "contributors"))
    return home


def flatten(page: Page) -> list[Page]:
    pages = [page]
    for child in page.children:
        pages.extend(flatten(child))
    return pages


def categories(tree: Page) -> list[Page]:
    return [child for child in tree.children if child.children]


def side_toc_html(page: Page, active_slug: str, depth: int = 0) -> str:
    active = active_slug == page.slug
    label = "Home" if page.slug == "" else html.escape(page.title)
    out = [
        f'<div class="toc-row depth-{depth} {active and "active" or ""}">'
        f'<a href="{page.url}">{label}</a>'
        f"</div>"
    ]
    for child in page.children:
        out.append(side_toc_html(child, active_slug, depth + 1))
    return "\n".join(out)


def section_index_html(page: Page) -> str:
    if not page.children:
        return ""
    links = "\n".join(
        f'<li><a href="{child.url}">{html.escape(child.title)}</a></li>'
        for child in page.children
    )
    return f'<h2>Terms</h2>\n<ul class="term-list">\n{links}\n</ul>'


def home_index_html(tree: Page) -> str:
    cards = []
    for category in categories(tree):
        child_links = "".join(
            f'<li><a href="{child.url}">{html.escape(child.title)}</a></li>'
            for child in category.children[:6]
        )
        cards.append(
            f'<section class="section-card"><h2><a href="{category.url}">{html.escape(category.title)}</a></h2>'
            f'<ul>{child_links}</ul></section>'
        )
    return '<div class="section-grid">' + "\n".join(cards) + "</div>"


def rewrite_links(rendered: str) -> str:
    rendered = rendered.replace('href="/fab-glossary"', f'href="{BASE_PATH}"')
    rendered = re.sub(r'href="/fab-glossary/([^"]+)"', lambda m: f'href="{BASE_PATH}{m.group(1).strip("/")}/"', rendered)
    rendered = re.sub(r'href="([^":#]+)\.md"', lambda m: f'href="{BASE_PATH}{m.group(1).strip("/")}/"', rendered)
    return rendered


def render_markdown(text: str) -> str:
    rendered = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "toc", "sane_lists"],
        output_format="html5",
    )
    return rewrite_links(rendered)


def page_template(page: Page, tree: Page, pages: list[Page], body: str) -> str:
    idx = pages.index(page)
    prev_page = pages[idx - 1] if idx > 0 else None
    next_page = pages[idx + 1] if idx < len(pages) - 1 else None
    path_label = "Introduction" if page.slug == "" else page.slug.replace("-", " /")
    prev_html = f'<a href="{prev_page.url}">← {html.escape(prev_page.title)}</a>' if prev_page else '<span></span>'
    next_html = f'<a href="{next_page.url}">{html.escape(next_page.title)} →</a>' if next_page else '<span></span>'

    if page.slug == "":
        body += home_index_html(tree)
    else:
        body += section_index_html(page)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(page.title)} | Foundry Stack</title>
  <meta name="description" content="A glossary for understanding semiconductor foundries as businesses and manufacturing systems." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Benne&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{BASE_PATH}assets/site.css" />
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <main class="glossary-shell">
    <aside class="side-toc" aria-label="Table of contents">
      <a class="site-title" href="{BASE_PATH}">Foundry Stack</a>
      <div class="site-description">The Foundry Business and Fab Operations Glossary</div>
      <input id="search" class="search" type="search" placeholder="Search glossary" />
      <div class="toc-heading">Table of Contents</div>
      <nav id="toc-nav">
        {side_toc_html(tree, page.slug)}
      </nav>
    </aside>

    <section id="content" class="content-panel">
      <article class="entry">
        <header class="entry-header">
          <div class="topline">
            <div class="path-label">{html.escape(path_label)}</div>
            <a class="suggest-edit" href="{REPO_URL}/issues/new" target="_blank" rel="noreferrer">Suggest edit</a>
          </div>
          <h1 class="entry-title">{html.escape(page.title)}</h1>
        </header>
        <div class="entry-content">
          {body}
        </div>
        <footer class="entry-footer">
          <nav class="pager" aria-label="Previous and next pages">
            {prev_html}
            {next_html}
          </nav>
        </footer>
      </article>
    </section>
  </main>
  <script src="{BASE_PATH}assets/site.js"></script>
</body>
</html>
"""


def write_page(page: Page, tree: Page, pages: list[Page]) -> None:
    target_dir = OUT if page.slug == "" else OUT / page.slug
    target_dir.mkdir(parents=True, exist_ok=True)
    body = render_markdown(page.body_md)
    (target_dir / "index.html").write_text(page_template(page, tree, pages, body))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)

    tree = build_tree()
    pages = flatten(tree)
    for page in pages:
        write_page(page, tree, pages)

    (OUT / "assets" / "site.css").write_text(CSS)
    (OUT / "assets" / "site.js").write_text(JS)
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(pages)} pages into {OUT}")


CSS = r'''
:root {
  --text: #f2f5ef;
  --heading: #ffffff;
  --muted: #a9b6a3;
  --border: #31402d;
  --paper: #0d180a;
  --panel: #111f0d;
  --panel-2: #0a1208;
  --link: #7fee64;
  --link-hover: #ffffff;
  --accent-bg: #7fee6424;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; background: var(--paper); color: var(--text); }
body { font-family: Benne, Georgia, 'Times New Roman', serif; font-size: 22px; line-height: 1.5; -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
a { color: var(--link); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.12em; }
a:hover { color: var(--link-hover); }
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 1rem; top: 1rem; background: white; color: #111; padding: .5rem; z-index: 10; }
.glossary-shell { height: 100vh; width: 100vw; display: grid; grid-template-columns: 360px minmax(0, 1fr); padding: 1rem; overflow: hidden; background: radial-gradient(circle at top left, #172912 0, var(--paper) 38rem); }
.side-toc { min-height: 0; overflow-y: auto; border: 1px solid var(--border); border-right: 0; background: color-mix(in srgb, var(--panel-2) 92%, transparent); padding: 1.25rem 1rem; }
.site-title { display: block; color: var(--heading); font-size: 2.4rem; line-height: .88; letter-spacing: -0.04em; text-decoration: none; margin-bottom: .35rem; }
.site-title:hover { color: var(--heading); text-decoration: none; }
.site-description { color: var(--muted); font-size: 1.05rem; line-height: 1.05; margin-bottom: 1rem; }
.search { width: 100%; background: transparent; color: var(--text); border: 1px solid var(--border); padding: .55rem .65rem; margin: .3rem 0 1rem; font: 0.95rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; outline: none; }
.search:focus { border-color: var(--link); box-shadow: 0 0 0 2px var(--accent-bg); }
.toc-heading { color: var(--link); font: .82rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; text-transform: uppercase; letter-spacing: .04em; margin: .25rem 0 .7rem; }
.toc-row { margin: .06rem 0; }
.toc-row a { display: block; color: var(--muted); text-decoration: none; padding: .22rem .35rem; border-left: 2px solid transparent; font: .92rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; line-height: 1.25; }
.toc-row a:hover, .toc-row.active a { color: var(--link); background: var(--accent-bg); text-decoration: none; }
.toc-row.active a { border-left-color: var(--link); }
.toc-row.depth-0 a { color: var(--text); }
.toc-row.depth-1 { padding-left: .55rem; margin-top: .45rem; }
.toc-row.depth-1 a { color: var(--text); }
.toc-row.depth-2 { padding-left: 1.25rem; }
.toc-row.depth-2 a { font-size: .86rem; }
.content-panel { min-width: 0; min-height: 0; overflow-y: auto; border: 1px solid var(--border); background: var(--panel); padding: clamp(1.5rem, 4vw, 3.5rem) clamp(1.25rem, 6vw, 5rem); }
.entry { max-width: 820px; }
.entry-header { margin-bottom: 1.2rem; }
.topline { display: flex; justify-content: space-between; gap: 1rem; align-items: center; margin-bottom: .7rem; }
.path-label { color: var(--muted); font: .92rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.suggest-edit { color: var(--muted); border: 1px solid var(--border); border-radius: 999px; padding: .25rem .55rem; font: .82rem ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; text-decoration: none; white-space: nowrap; }
.suggest-edit:hover { color: var(--link); border-color: var(--link); text-decoration: none; }
.entry-title { color: var(--heading); font-size: clamp(3rem, 7vw, 5.8rem); line-height: .9; letter-spacing: -0.04em; font-weight: 400; margin: 0 0 1.8rem; }
.entry-content p { margin: 0 0 1.1em; }
.entry-content h2, .entry-content h3, .entry-content h4 { color: var(--heading); font-weight: 400; line-height: 1.05; margin: 1.6em 0 .55em; padding-top: .4em; }
.entry-content h2 { font-size: 2.15rem; }
.entry-content h3 { font-size: 1.65rem; }
.entry-content ul, .entry-content ol { padding-left: 1.3em; }
.entry-content li { margin: .15em 0; }
.entry-content hr { border: 0; border-top: 1px solid var(--border); margin: 2.5rem 0; }
.entry-content blockquote { border-left: 3px solid var(--link); margin: 1.5rem 0; padding-left: 1rem; color: var(--muted); }
.entry-content code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .8em; background: var(--accent-bg); padding: .1em .25em; color: var(--link); }
.entry-content pre { overflow-x: auto; background: #071004; border: 1px solid var(--border); padding: 1rem; font-size: .8em; }
.entry-content table { border-collapse: collapse; width: 100%; font-size: .9em; margin: 1.2rem 0; }
.entry-content th, .entry-content td { border: 1px solid var(--border); padding: .35em .5em; vertical-align: top; }
.section-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem 1.5rem; margin-top: 2.4rem; }
.section-card { border-top: 1px solid var(--border); padding-top: .8rem; }
.section-card h2 { margin-top: 0; padding-top: 0; font-size: 1.55rem; }
.section-card ul, .term-list { columns: 2; column-gap: 2rem; font-size: 1.05rem; }
.term-list { margin-top: .5rem; }
.entry-footer { border-top: 1px solid var(--border); margin-top: 3rem; padding-top: 1rem; font-size: 1rem; }
.pager { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 1rem; }
@media (max-width: 860px) {
  body { font-size: 20px; }
  .glossary-shell { display: block; height: auto; min-height: 100vh; overflow: visible; padding: 0; }
  .side-toc { max-height: 46vh; border: 0; border-bottom: 1px solid var(--border); }
  .content-panel { overflow: visible; border: 0; padding: 1.5rem 1rem 3rem; }
  .section-grid { grid-template-columns: 1fr; }
  .section-card ul, .term-list { columns: 1; }
  .pager { display: block; }
  .pager a { display: block; margin-bottom: .5rem; }
}
'''


JS = r'''
const pagerLinks = [...document.querySelectorAll('.pager a')];
const search = document.getElementById('search');
const tocRows = [...document.querySelectorAll('.toc-row')];
if (search) {
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    tocRows.forEach((row) => {
      row.style.display = !q || row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}
document.addEventListener('keydown', (event) => {
  if (event.target && ['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
  if (event.key === 'ArrowLeft' && pagerLinks[0]) location.href = pagerLinks[0].href;
  if (event.key === 'ArrowRight' && pagerLinks[1]) location.href = pagerLinks[1].href;
  if (event.key === '/') { event.preventDefault(); search?.focus(); }
});
'''


if __name__ == "__main__":
    main()
