# Selection Guide 2026 Europe — Website

Transformation of the **"Selection Guide - 2026 Europe - English.pdf"** (814 pages,
Mersen electrical protection catalog) into a modern, responsive, browsable
website, inspired by the Microsoft Learn design.

## Features

- Chapter structure automatically generated from the PDF (About Us,
  Product Selector, Markets, Knowledge Centre), with ~760 product
  references organized into families / subfamilies.
- Collapsible, tree-structured side navigation, fully responsive (drawer on mobile).
- Internal search (client-side) over each page's title and extracted text.
- Real text and tables: every product page's spec table and text is
  reconstructed as real, selectable HTML (not a screenshot). Embedded
  product photos and icons are preserved as real images, and the original
  page render is kept as a collapsible fallback.
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

The Python scripts in `extract/` regenerate `data/*.json`, the content images in
`public/assets/`, and the full-page fallback renders in `public/pages/` from the
source PDF (requires `pymupdf` and `pillow`):

```bash
pip install pymupdf pillow
python3 extract/build_data.py     # -> web_data/*.json, web_data/assets/*.webp
python3 extract/render_images.py  # -> web_data/pages_img/*.webp
# then copy web_data/nav.json, web_data/pages.json to data/
# web_data/search-index.json to public/data/, web_data/assets to public/assets/,
# and web_data/pages_img to public/pages/
```

## Deploying to Vercel

The repository is ready to be imported as-is into [Vercel](https://vercel.com):
Next.js is auto-detected, and `npm run build` statically generates every page (SSG).
