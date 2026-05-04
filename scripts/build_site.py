#!/usr/bin/env python3
"""Build the Fab Glossary static site for GitHub Pages."""
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
PRIMARY = "#7fee64"
BG = "#0d180a"

CATEGORY_ORDER = ["process", "equipment", "materials", "metrology", "yield-economics"]


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
    title = meta.get("title") or slug.replace("-", " ").title() or "Fab Glossary"
    return Page(title=title, slug=slug, source=path, body_md=body)


def build_tree() -> Page:
    home = read_page(CONTENT / "readme.md", "")

    categories: list[Page] = []
    for stem in CATEGORY_ORDER:
        path = CONTENT / f"{stem}.md"
        if not path.exists():
            continue
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


def nav_html(page: Page, active_slug: str, depth: int = 0) -> str:
    active = " active" if page.slug == active_slug else ""
    label = "Home" if page.slug == "" else html.escape(page.title)
    out = [
        f'<div class="nav-row depth-{depth}{active}">'
        f'<a href="{page.url}">{label}</a>'
        f"</div>"
    ]
    for child in page.children:
        out.append(nav_html(child, active_slug, depth + 1))
    return "\n".join(out)


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
    path_label = "/" if page.slug == "" else f"/{page.slug}"
    prev_html = f'<a href="{prev_page.url}">← {html.escape(prev_page.title)}</a>' if prev_page else '<span></span>'
    next_html = f'<a href="{next_page.url}">{html.escape(next_page.title)} →</a>' if next_page else '<span></span>'

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(page.title)} | Fab Glossary</title>
  <meta name="description" content="A semiconductor fab glossary inspired by Modal's GPU Glossary." />
  <link rel="stylesheet" href="{BASE_PATH}assets/site.css" />
</head>
<body>
  <main class="shell">
    <aside class="sidebar">
      <a class="brand" href="{BASE_PATH}" aria-label="Fab Glossary home">
        <span class="brand-mark">FAB</span>
        <span>Glossary</span>
      </a>
      <input id="search" class="search" type="search" placeholder="Search terms" />
      <nav id="nav" class="nav" aria-label="Table of contents">
        <div class="toc-title">TABLE OF CONTENTS</div>
        {nav_html(tree, page.slug)}
      </nav>
    </aside>

    <article class="content">
      <div class="topline">
        <div class="path">{html.escape(path_label)}</div>
        <a class="issue" href="{REPO_URL}/issues/new" target="_blank" rel="noreferrer">Suggest edit</a>
      </div>
      <h1>{html.escape(page.title)}</h1>
      <div class="markdown">
        {body}
      </div>
      <footer class="pager">
        {prev_html}
        {next_html}
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
  color-scheme: dark;
  --primary: #7fee64;
  --primary-dim: #7fee6499;
  --primary-faint: #7fee6426;
  --bg: #0d180a;
  --panel: #111f0d;
  --text: #d8ffd0;
  --muted: #a6cfa0;
  --border: #7fee6455;
}
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; background: var(--bg); color: var(--text); }
body { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }
a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }
.shell { display: grid; grid-template-columns: 320px minmax(0, 1fr); height: 100vh; border: 1px solid var(--border); }
.sidebar { overflow-y: auto; border-right: 1px solid var(--border); padding: 18px; background: #0b1608; }
.brand { display: flex; align-items: center; gap: 10px; color: var(--primary); font-size: 20px; font-weight: 700; margin-bottom: 18px; }
.brand-mark { border: 1px solid var(--primary); padding: 4px 6px; background: var(--primary-faint); }
.search { width: 100%; background: transparent; border: 1px solid var(--border); color: var(--text); padding: 10px 12px; margin-bottom: 18px; font: inherit; outline: none; }
.search:focus { border-color: var(--primary); box-shadow: 0 0 0 2px var(--primary-faint); }
.toc-title { color: var(--primary); font-size: 14px; margin: 0 0 10px; }
.nav-row { margin: 2px 0; }
.nav-row a { display: block; color: var(--muted); padding: 6px 8px; border-left: 2px solid transparent; }
.nav-row.depth-1 { padding-left: 14px; }
.nav-row.depth-2 { padding-left: 28px; }
.nav-row.active a, .nav-row a:hover { color: var(--primary); background: var(--primary-faint); border-left-color: var(--primary); text-decoration: none; }
.content { overflow-y: auto; padding: 28px clamp(24px, 6vw, 88px); max-width: 1000px; }
.topline { display: flex; justify-content: space-between; gap: 16px; color: var(--primary-dim); margin-bottom: 16px; }
.path { color: var(--primary-dim); }
.issue { border: 1px solid var(--border); border-radius: 999px; padding: 6px 10px; font-size: 13px; }
h1 { color: var(--text); font-size: clamp(32px, 5vw, 56px); line-height: 1.05; margin: 0 0 24px; font-weight: 600; }
.markdown { color: var(--text); font-size: 17px; line-height: 1.7; }
.markdown p, .markdown ul, .markdown ol { max-width: 78ch; }
.markdown h2, .markdown h3 { color: var(--primary); margin-top: 34px; }
.markdown a { background: var(--primary-faint); padding: 0 3px; }
.markdown pre { overflow-x: auto; border: 1px solid var(--border); padding: 16px; background: #071004; }
.markdown code { color: var(--primary); }
.markdown table { border-collapse: collapse; max-width: 100%; display: block; overflow-x: auto; }
.markdown th, .markdown td { border: 1px solid var(--border); padding: 8px 10px; }
.pager { display: flex; justify-content: space-between; gap: 20px; border-top: 1px solid var(--border); margin-top: 48px; padding-top: 18px; }
@media (max-width: 820px) {
  .shell { display: block; height: auto; border: 0; }
  .sidebar { position: static; max-height: 48vh; border-right: 0; border-bottom: 1px solid var(--border); }
  .content { overflow: visible; padding: 24px 18px 48px; }
}
'''

JS = r'''
const search = document.getElementById('search');
const rows = [...document.querySelectorAll('.nav-row')];
if (search) {
  search.addEventListener('input', () => {
    const q = search.value.trim().toLowerCase();
    rows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      row.style.display = !q || text.includes(q) ? '' : 'none';
    });
  });
}
const links = [...document.querySelectorAll('.pager a')];
document.addEventListener('keydown', (event) => {
  if (event.target && ['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
  if (event.key === 'ArrowLeft' && links[0]) location.href = links[0].href;
  if (event.key === 'ArrowRight' && links[1]) location.href = links[1].href;
  if (event.key === '/') { event.preventDefault(); search?.focus(); }
});
'''


if __name__ == "__main__":
    main()
