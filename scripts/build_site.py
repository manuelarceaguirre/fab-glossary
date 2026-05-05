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


def top_nav_html(tree: Page, active_slug: str) -> str:
    items = [f'<li><a class="{active_slug == "" and "active" or ""}" href="{BASE_PATH}">Introduction</a></li>']
    for category in categories(tree):
        active = active_slug == category.slug or active_slug.startswith(f"{category.slug}/")
        items.append(
            f'<li><a class="{active and "active" or ""}" href="{category.url}">{html.escape(category.title)}</a></li>'
        )
    items.append(f'<li><a class="{active_slug == "contributors" and "active" or ""}" href="{BASE_PATH}contributors/">About</a></li>')
    return "\n".join(items)


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
  <header class="site-header">
    <div class="inner">
      <a class="site-title" href="{BASE_PATH}">Foundry Stack</a>
      <div class="site-description">The Foundry Business and Fab Operations Glossary</div>
      <nav class="main-navigation" aria-label="Main navigation">
        <ul>
          {top_nav_html(tree, page.slug)}
        </ul>
      </nav>
    </div>
  </header>

  <main id="content" class="content-wrapper">
    <article class="entry">
      <header class="entry-header">
        <div class="path-label">{html.escape(path_label)}</div>
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
        <a class="suggest-edit" href="{REPO_URL}/issues/new" target="_blank" rel="noreferrer">Suggest an edit on GitHub</a>
      </footer>
    </article>
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
  --text: #383838;
  --heading: #0a0a0a;
  --muted: #6d6d6d;
  --border: #e6e1d8;
  --paper: #fffdf8;
  --link: #0a0a0a;
  --link-hover: blue;
  --accent-bg: #f7f3eb;
}
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; background: var(--paper); color: var(--text); }
body {
  font-family: Benne, Georgia, 'Times New Roman', serif;
  font-size: 22px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
a { color: var(--link); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.12em; }
a:hover { color: var(--link-hover); }
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 1rem; top: 1rem; background: white; padding: .5rem; z-index: 10; }
.site-header { padding: 3.25rem .75rem 1.2rem; }
.inner { max-width: 1100px; margin: 0 auto; }
.site-title {
  display: inline-block;
  color: var(--heading);
  font-size: clamp(3.2rem, 9vw, 7.5rem);
  line-height: .82;
  letter-spacing: -0.045em;
  text-decoration: none;
}
.site-title:hover { color: var(--heading); text-decoration: none; }
.site-description {
  color: var(--muted);
  font-size: clamp(1.5rem, 3vw, 2.1rem);
  line-height: .9;
  margin-top: .3rem;
}
.main-navigation { max-width: 1100px; margin-top: 2.2rem; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.main-navigation ul { list-style: none; margin: 0; padding: .65rem 0; display: flex; flex-wrap: wrap; gap: .2rem 1.1rem; }
.main-navigation li { margin: 0; }
.main-navigation a { color: var(--heading); font-size: 1.05rem; text-decoration: none; display: inline-block; }
.main-navigation a:hover, .main-navigation a.active { color: var(--link-hover); text-decoration: underline; }
.content-wrapper { padding: 2.6rem .75rem 4rem; }
.entry { max-width: 760px; margin: 0 auto; }
.entry-header { margin-bottom: 1.2rem; }
.path-label { color: var(--muted); font-size: 1.05rem; margin-bottom: .3rem; }
.entry-title {
  color: var(--heading);
  font-size: clamp(2.8rem, 7vw, 5.2rem);
  line-height: .95;
  letter-spacing: -0.035em;
  font-weight: 400;
  margin: 0 0 1.8rem;
}
.entry-content p { margin: 0 0 1.1em; }
.entry-content h2, .entry-content h3, .entry-content h4 {
  color: var(--heading);
  font-weight: 400;
  line-height: 1.05;
  margin: 1.6em 0 .55em;
  padding-top: .4em;
}
.entry-content h2 { font-size: 2.15rem; }
.entry-content h3 { font-size: 1.65rem; }
.entry-content ul, .entry-content ol { padding-left: 1.3em; }
.entry-content li { margin: .15em 0; }
.entry-content hr { border: 0; border-top: 1px solid var(--border); margin: 2.5rem 0; }
.entry-content blockquote { border-left: 3px solid var(--heading); margin: 1.5rem 0; padding-left: 1rem; color: var(--muted); }
.entry-content code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .8em; background: var(--accent-bg); padding: .1em .25em; }
.entry-content pre { overflow-x: auto; background: var(--accent-bg); border: 1px solid var(--border); padding: 1rem; font-size: .8em; }
.entry-content table { border-collapse: collapse; width: 100%; font-size: .9em; margin: 1.2rem 0; }
.entry-content th, .entry-content td { border: 1px solid var(--border); padding: .35em .5em; vertical-align: top; }
.section-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem 1.5rem; margin-top: 2.4rem; }
.section-card { border-top: 1px solid var(--border); padding-top: .8rem; }
.section-card h2 { margin-top: 0; padding-top: 0; font-size: 1.55rem; }
.section-card ul, .term-list { columns: 2; column-gap: 2rem; font-size: 1.05rem; }
.term-list { margin-top: .5rem; }
.entry-footer { border-top: 1px solid var(--border); margin-top: 3rem; padding-top: 1rem; font-size: 1.05rem; }
.pager { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 1rem; }
.suggest-edit { color: var(--muted); }
@media (max-width: 760px) {
  body { font-size: 20px; }
  .site-header { padding-top: 2rem; }
  .main-navigation ul { display: block; }
  .main-navigation li { margin: .25rem 0; }
  .section-grid { grid-template-columns: 1fr; }
  .section-card ul, .term-list { columns: 1; }
  .pager { display: block; }
  .pager a { display: block; margin-bottom: .5rem; }
}
'''

JS = r'''
const pagerLinks = [...document.querySelectorAll('.pager a')];
document.addEventListener('keydown', (event) => {
  if (event.target && ['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
  if (event.key === 'ArrowLeft' && pagerLinks[0]) location.href = pagerLinks[0].href;
  if (event.key === 'ArrowRight' && pagerLinks[1]) location.href = pagerLinks[1].href;
});
'''


if __name__ == "__main__":
    main()
