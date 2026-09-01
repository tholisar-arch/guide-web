export type TableBlock = {
  type: "table";
  headers: string[] | null;
  rows: string[][];
};

export type ParagraphBlock = {
  type: "paragraph";
  text: string;
  size: number;
};

export type ContentBlock = TableBlock | ParagraphBlock;

export type ResourceLink = {
  label: string;
  url: string;
};

export type PageEntry = {
  page: number;
  chapter: "cover" | "about" | "selector" | "markets" | "knowledge";
  category: string | null;
  subcategory: string | null;
  tail: string[];
  title: string;
  text: string;
  blocks: ContentBlock[];
  slug: string;
  resourceLinks?: ResourceLink[];
};

export type NavLeafItem = {
  title: string;
  slug: string;
  page: number;
};

export type SelectorNavNode =
  | { type: "leaves"; items: NavLeafItem[] }
  | {
      type: "group";
      children: {
        title: string;
        slug: string;
        count: number;
        node: SelectorNavNode;
      }[];
    };

export type SelectorCategory = {
  title: string;
  slug: string;
  count: number;
  nav: SelectorNavNode;
};

export type ChapterAbout = {
  slug: "about";
  title: string;
  items: NavLeafItem[];
};

export type ChapterSelector = {
  slug: "selector";
  title: string;
  overview: NavLeafItem[];
  categories: SelectorCategory[];
};

export type ChapterMarkets = {
  slug: "markets";
  title: string;
  overviewSlug: string;
  items: NavLeafItem[];
};

export type ChapterKnowledge = {
  slug: "knowledge";
  title: string;
  items: NavLeafItem[];
};

export type Chapter =
  | ChapterAbout
  | ChapterSelector
  | ChapterMarkets
  | ChapterKnowledge;

export type NavRoot = {
  chapters: Chapter[];
};
