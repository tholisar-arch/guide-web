import pagesDataEn from "@/data/pages.json";
import navDataEn from "@/data/nav.json";
import pagesDataFr from "@/data/pages.fr.json";
import navDataFr from "@/data/nav.fr.json";
import pagesDataIt from "@/data/pages.it.json";
import navDataIt from "@/data/nav.it.json";
import pagesDataDe from "@/data/pages.de.json";
import navDataDe from "@/data/nav.de.json";
import pagesDataNl from "@/data/pages.nl.json";
import navDataNl from "@/data/nav.nl.json";
import type {
  PageEntry,
  NavRoot,
  Chapter,
  ChapterSelector,
  SelectorNavNode,
  NavLeafItem,
} from "@/lib/types";

export type Locale = "en" | "fr" | "it" | "de" | "nl";
export const LOCALES: Locale[] = ["en", "fr", "it", "de", "nl"];

export type ListingResult =
  | { kind: "chapter"; chapter: Chapter }
  | {
      kind: "category";
      chapter: ChapterSelector;
      category: ChapterSelector["categories"][number];
      node: SelectorNavNode;
      pathTitles: string[];
    }
  | {
      kind: "subgroup";
      chapter: ChapterSelector;
      category: ChapterSelector["categories"][number];
      node: SelectorNavNode;
      pathTitles: string[];
    };

function createDataApi(pagesData: unknown, navData: unknown) {
  const pages = pagesData as PageEntry[];
  const nav = navData as NavRoot;

  const pagesBySlug = new Map<string, PageEntry>();
  const pagesByNumber = new Map<number, PageEntry>();
  for (const p of pages) {
    pagesBySlug.set(p.slug, p);
    pagesByNumber.set(p.page, p);
  }

  function getPageBySlug(slug: string): PageEntry | undefined {
    return pagesBySlug.get(slug);
  }

  function getPageByNumber(n: number): PageEntry | undefined {
    return pagesByNumber.get(n);
  }

  function getAdjacentPages(pageNumber: number) {
    const entry = pagesByNumber.get(pageNumber);
    const index = entry ? pages.indexOf(entry) : -1;
    return {
      prev: index > 0 ? pages[index - 1] : null,
      next: index >= 0 && index < pages.length - 1 ? pages[index + 1] : null,
    };
  }

  function getChapter(slug: string): Chapter | undefined {
    return nav.chapters.find((c) => c.slug === slug);
  }

  function resolveListing(segments: string[]): ListingResult | null {
    if (segments.length === 0) return null;
    const chapter = getChapter(segments[0]);
    if (!chapter) return null;
    if (segments.length === 1) return { kind: "chapter", chapter };
    if (chapter.slug !== "selector") return null;

    const sel = chapter as ChapterSelector;
    const category = sel.categories.find((c) => c.slug === segments[1]);
    if (!category) return null;
    if (segments.length === 2) {
      return {
        kind: "category",
        chapter: sel,
        category,
        node: category.nav,
        pathTitles: [],
      };
    }

    let node = category.nav;
    const pathTitles: string[] = [];
    for (const seg of segments.slice(2)) {
      if (node.type !== "group") return null;
      const child = node.children.find((c) => c.slug === seg);
      if (!child) return null;
      pathTitles.push(child.title);
      node = child.node;
    }
    return { kind: "subgroup", chapter: sel, category, node, pathTitles };
  }

  function walkSelectorGroupPaths(
    node: SelectorNavNode,
    prefix: string[]
  ): string[][] {
    if (node.type === "leaves") return [];
    let out: string[][] = [];
    for (const child of node.children) {
      const path = [...prefix, child.slug];
      out.push(path);
      out = out.concat(walkSelectorGroupPaths(child.node, path));
    }
    return out;
  }

  function getAllListingParams(): string[][] {
    const out: string[][] = [];
    for (const chapter of nav.chapters) {
      out.push([chapter.slug]);
      if (chapter.slug === "selector") {
        const sel = chapter as ChapterSelector;
        for (const category of sel.categories) {
          out.push([chapter.slug, category.slug]);
          for (const p of walkSelectorGroupPaths(category.nav, [
            chapter.slug,
            category.slug,
          ])) {
            out.push(p);
          }
        }
      }
    }
    return out;
  }

  function getAllParams(): { slug: string[] }[] {
    const leafParams = pages.map((p) => ({ slug: p.slug.split("/") }));
    const listingParams = getAllListingParams().map((s) => ({ slug: s }));
    return [...leafParams, ...listingParams];
  }

  function flattenLeaves(node: SelectorNavNode): NavLeafItem[] {
    if (node.type === "leaves") return node.items;
    return node.children.flatMap((c) => flattenLeaves(c.node));
  }

  function getListingChain(
    segments: string[]
  ): { title: string; href: string }[] {
    const chain: { title: string; href: string }[] = [];
    for (let i = 1; i <= segments.length; i++) {
      const prefix = segments.slice(0, i);
      const result = resolveListing(prefix);
      if (!result) break;
      let title: string;
      if (result.kind === "chapter") title = result.chapter.title;
      else if (result.kind === "category") title = result.category.title;
      else title = result.pathTitles[result.pathTitles.length - 1];
      chain.push({ title, href: "/guide/" + prefix.join("/") });
    }
    return chain;
  }

  return {
    pages,
    nav,
    getPageBySlug,
    getPageByNumber,
    getAdjacentPages,
    getChapter,
    resolveListing,
    getAllListingParams,
    getAllParams,
    flattenLeaves,
    getListingChain,
  };
}

export type DataApi = ReturnType<typeof createDataApi>;

const apis: Record<Locale, DataApi> = {
  en: createDataApi(pagesDataEn, navDataEn),
  fr: createDataApi(pagesDataFr, navDataFr),
  it: createDataApi(pagesDataIt, navDataIt),
  de: createDataApi(pagesDataDe, navDataDe),
  nl: createDataApi(pagesDataNl, navDataNl),
};

export function getData(locale: Locale): DataApi {
  return apis[locale];
}

// Back-compat default (English) exports for any call site that hasn't
// been made locale-aware yet.
export const pages = apis.en.pages;
export const nav = apis.en.nav;
export const getPageBySlug = apis.en.getPageBySlug;
export const getPageByNumber = apis.en.getPageByNumber;
export const getAdjacentPages = apis.en.getAdjacentPages;
export const getChapter = apis.en.getChapter;
export const resolveListing = apis.en.resolveListing;
export const getAllListingParams = apis.en.getAllListingParams;
export const getAllParams = apis.en.getAllParams;
export const flattenLeaves = apis.en.flattenLeaves;
export const getListingChain = apis.en.getListingChain;
