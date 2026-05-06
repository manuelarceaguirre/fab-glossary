# Foundry Stack

This repository contains the source content and static-site generator for Foundry Stack, a glossary for understanding semiconductor foundries as businesses and manufacturing systems.

The project is intentionally inspired by Modal's excellent [GPU Glossary](https://github.com/modal-labs/gpu-glossary). The goal is to build a similar hyperlinked glossary format, but focused on the semiconductor manufacturing value chain: industry map, materials and wafers, front-end wafer fabrication, mid-end/advanced packaging, back-end/OSAT, fab operations, and economics/models.

Live site: https://manuelarceaguirre.github.io/fab-glossary/

## Licenses

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CC BY 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](fab-glossary/LICENSE)

All files in the `fab-glossary` folder of this repository are licensed under the 
[Creative Commons Attribution 4.0 International (CC BY 4.0) License](https://creativecommons.org/licenses/by/4.0/).
See [`fab-glossary/LICENSE`](fab-glossary/LICENSE) for details.

The remainder of the files in this repository are licensed under the
[MIT License](https://opensource.org/license/mit).
See [`LICENSE`](LICENSE) for details.

## Editing the Glossary

The site is designed so contributors can focus on Markdown.

- Edit homepage copy in `fab-glossary/readme.md`.
- Edit a section landing page, e.g. `fab-glossary/front-end.md`.
- Add a new term by creating a Markdown file inside a section, e.g. `fab-glossary/front-end/euv-scanner.md`.
- Add a new section by creating both a top-level file and directory, e.g. `fab-glossary/advanced-packaging.md` and `fab-glossary/advanced-packaging/hybrid-bonding.md`.

Each Markdown file should start with frontmatter:

```md
---
title: EUV Scanner
---

Your glossary entry here.
```

When changes are pushed to `main`, GitHub Actions rebuilds and publishes the site to GitHub Pages automatically.

For local preview:

```bash
pip install -r requirements.txt
python scripts/build_site.py
python -m http.server 8000 -d docs
```

Then open `http://localhost:8000/fab-glossary/`.
