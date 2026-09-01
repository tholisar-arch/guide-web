# Selection Guide 2026 Europe — Website

Transformation of the **"Selection Guide - 2026 Europe - English.pdf"** (814 pages,
Mersen electrical protection catalog) into a modern, responsive **Product
Selector** website.

## Features

- Category tree automatically generated from the PDF's Product Selector
  section (the About Us / Markets / Knowledge Centre chapters from the
  source PDF are intentionally excluded — this site is the product
  selector only), pruned down to the ~440 pages that show a genuine
  product reference table (Part Number / Catalog Number rows) — pages
  that were just an intermediate "choose a size/voltage" step or a
  size/voltage-range summary with no purchasable reference are dropped.
- Collapsible, tree-structured side navigation, fully responsive (drawer on mobile).
- Internal search (client-side) over each page's title and extracted text.
- Real tables: every product page's spec table is reconstructed as real,
  selectable HTML (not a screenshot or an image) directly from the PDF's
  positioned text.
- Every screen (category, subcategory, and product page) is wrapped in a
  header that reproduces the original PDF Product Selector chrome (photo
  banner, "PRODUCT SELECTOR" title, Mersen logo, Back button), so browsing
  the site feels the same as flipping through the tool in the PDF.
- Text-only: no product photos/icons, no page-count or reference-count
  badges anywhere (home page, sidebar, category cards) — just the
  navigation tree and the reference tables.
- Light / dark theme, optimized for mobile / tablet / desktop.
- Next.js (App Router) project, fully static, ready for Vercel deployment.

## Development

```bash
npm install
npm run dev
```

## Production build

```bash
npm run build
npm run start
```

## Regenerating data from the PDF

The Python scripts in `extract/` regenerate `data/*.json` from the source PDF
(requires `pymupdf` and `pillow`):

```bash
pip install pymupdf pillow
python3 extract/build_data.py     # -> web_data/*.json
# copy web_data/nav.json, web_data/pages.json to data/
# and web_data/search-index.json to public/data/
python3 extract/filter_selector_only.py         # drop About/Markets/Knowledge
python3 extract/filter_reference_tables_only.py # drop pages with no real reference table
```

The site itself carries no images (product photos/screenshots were
deliberately removed — see Features above), so there is no image step to
run; `build_data.py` still extracts `blocks`/`images`/`screenshot` fields
for archival purposes, but the `data/pages.json` shipped in this repo has
had `images`/`screenshot` stripped and nothing in the app reads them.

## Deploying to Vercel

The repository is ready to be imported as-is into [Vercel](https://vercel.com):
Next.js is auto-detected, and `npm run build` statically generates every page (SSG).
