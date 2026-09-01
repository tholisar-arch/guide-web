# Selection Guide 2026 Europe — site web

Transformation du PDF **"Selection Guide - 2026 Europe - English.pdf"** (814 pages,
catalogue de protection électrique Mersen) en un site web moderne, responsive et
consultable, inspiré du design de Microsoft Learn.

## Fonctionnalités

- Structure de chapitres générée automatiquement à partir du PDF (À propos,
  Sélecteur de produits, Marchés, Centre de connaissances), avec ~760 références
  produits organisées en familles / sous-familles.
- Navigation latérale arborescente, repliable, responsive (drawer sur mobile).
- Recherche interne (client-side) sur les titres et le texte extrait de chaque page.
- Toutes les visuels du guide sont conservés : chaque page est rendue en image
  haute qualité (WebP) en plus du texte extrait pour l'accessibilité et la recherche.
- Thème clair / sombre, optimisé mobile / tablette / desktop.
- Projet Next.js (App Router) 100% statique, prêt pour un déploiement Vercel.

## Développement

```bash
npm install
npm run dev
```

## Build de production

```bash
npm run build
npm run start
```

## Régénérer les données depuis le PDF

Les scripts Python dans `extract/` régénèrent `data/*.json` et les images de
`public/pages/` à partir du PDF source (nécessite `pymupdf` et `pillow`) :

```bash
pip install pymupdf pillow
python3 extract/build_data.py     # -> web_data/*.json
python3 extract/render_images.py  # -> web_data/pages_img/*.webp
# puis copier web_data/nav.json, web_data/pages.json vers data/
# et web_data/search-index.json vers public/data/, web_data/pages_img vers public/pages/
```

## Déploiement sur Vercel

Le dépôt est prêt à être importé tel quel sur [Vercel](https://vercel.com) :
Next.js est détecté automatiquement, `npm run build` génère l'ensemble des pages
en statique (SSG).
