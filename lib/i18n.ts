export type Locale = "en" | "fr" | "it";

export const LOCALES: Locale[] = ["en", "fr", "it"];

export const LOCALE_LABELS: Record<Locale, string> = {
  en: "English",
  fr: "Français",
  it: "Italiano",
};

// Every non-English locale is prefixed with its own segment ("/fr", "/it").
const PREFIXED_LOCALES = LOCALES.filter((l) => l !== "en");

/** Prefix an internal path ("/guide/...", "/xref", "/spd-configurator",
 * "/search", "/") with the locale segment. English has no prefix. */
export function localeHref(locale: Locale, path: string): string {
  if (locale === "en") return path;
  return path === "/" ? `/${locale}` : `/${locale}${path}`;
}

/** Given the current pathname, return the equivalent path under the other
 * locale (used by the language switcher). */
export function switchLocalePath(pathname: string, target: Locale): string {
  const prefix = PREFIXED_LOCALES.find(
    (l) => pathname === `/${l}` || pathname.startsWith(`/${l}/`)
  );
  const stripped = prefix ? pathname.slice(1 + prefix.length) || "/" : pathname;
  return localeHref(target, stripped);
}

export function localeFromPathname(pathname: string): Locale {
  return (
    PREFIXED_LOCALES.find(
      (l) => pathname === `/${l}` || pathname.startsWith(`/${l}/`)
    ) ?? "en"
  );
}

type Dict = {
  guideHome: string;
  crossReferenceSearch: string;
  spdConfigurator: string;
  searchPlaceholderHeader: string;
  searchPlaceholderHero: string;
  home: string;
  back: string;
  documentation: string;
  filterReferences: string;
  noReferencesFound: string;
  noResultsFor: (q: string) => string;
  viewAllResultsFor: (q: string) => string;
  resultsCountFor: (n: number, q: string) => string;
  loading: string;
  productSelectorFallback: string;
  siteSubtitle: string;
  heroBadge: string;
  heroTitle1: string;
  heroTitle2: string;
  heroDescription: string;
  productFamilies: string;
  productFamiliesDesc: string;
  moreTools: string;
  moreToolsDesc: string;
  xrefCardTitle: string;
  xrefCardDesc: string;
  spdCardTitle: string;
  spdCardDesc: string;
  xrefEyebrow: string;
  xrefH1: string;
  xrefDesc: string;
  xrefSearchPlaceholder: string;
  xrefResultsFor: (n: number, q: string) => string;
  xrefNoResults: string;
  xrefMatchedVia: (brand: string) => string;
  spdEyebrow: string;
  spdH1: string;
  spdDesc: string;
  spdStartOver: string;
  searchTitle: string;
  searchNoResults: string;
  matchTitle: string;
  metaSiteTitle: string;
  metaSiteDescription: string;
  mersenWebsiteLabel: string;
  mersenWebsiteUrl: string;
  sendRequestNav: string;
  sendRequestCardTitle: string;
  sendRequestCardDesc: string;
  sendRequestEyebrow: string;
  sendRequestH1: string;
  sendRequestDesc: string;
  sendRequestCountryLabel: string;
  sendRequestCountryPlaceholder: string;
  sendRequestFirstNameLabel: string;
  sendRequestLastNameLabel: string;
  sendRequestCompanyLabel: string;
  sendRequestTypeLabel: string;
  sendRequestTypePlaceholder: string;
  sendRequestTypeFuse: string;
  sendRequestTypeSurge: string;
  sendRequestTypeBoth: string;
  sendRequestEmailLabel: string;
  sendRequestEmailPlaceholder: string;
  sendRequestMessageLabel: string;
  sendRequestMessagePlaceholder: string;
  sendRequestButton: string;
  sendRequestHint: string;
  sendRequestSentTo: (country: string) => string;
  sendRequestSubjectPrefix: string;
};

const en: Dict = {
  guideHome: "Guide Home",
  crossReferenceSearch: "Cross Reference Search",
  spdConfigurator: "SPD Configurator",
  searchPlaceholderHeader: "Search the guide... (fuses, SPD, voltage...)",
  searchPlaceholderHero: "Search the guide... (fuses, SPD, voltage...)",
  home: "Home",
  back: "Back",
  documentation: "Documentation",
  filterReferences: "Filter references...",
  noReferencesFound: "No references found.",
  noResultsFor: (q) => `No results for "${q}"`,
  viewAllResultsFor: (q) => `View all results for "${q}" →`,
  resultsCountFor: (n, q) => `${n} result${n !== 1 ? "s" : ""} for "${q}"`,
  loading: "Loading...",
  productSelectorFallback: "Product Selector",
  siteSubtitle: "2026 Europe",
  heroBadge: "Interactive Product Selector · 2026 Europe Edition",
  heroTitle1: "Selection Guide",
  heroTitle2: "Electrical Protection",
  heroDescription:
    "The full product selector, transformed into a website: fuses, surge protection devices, and photovoltaic solutions, organized by product family and fully browsable on mobile, tablet, and desktop.",
  productFamilies: "Product Families",
  productFamiliesDesc: "Browse the full Product Selector by category.",
  moreTools: "More Tools",
  moreToolsDesc: "Additional lookups built on the same product data.",
  xrefCardTitle: "Cross Reference Search",
  xrefCardDesc:
    "Find the equivalent Mersen reference for a competitor part number (Citel, Dehn, Eaton, Siemens, and more).",
  spdCardTitle: "SPD Configurator",
  spdCardDesc:
    "Answer a few questions about your installation to find the right Surge Protection Device family.",
  xrefEyebrow: "Cross Reference Search",
  xrefH1: "Find a Mersen reference from a competitor part number",
  xrefDesc:
    "Search by a competitor's reference (Citel, Dehn, Eaton, Siemens, Schneider Electric, and more) to find the equivalent Mersen part.",
  xrefSearchPlaceholder: "Search a competitor reference...",
  xrefResultsFor: (n, q) => `${n} result${n !== 1 ? "s" : ""} for "${q}"`,
  xrefNoResults: "No results. Try a different reference.",
  xrefMatchedVia: (brand) => `matched via ${brand}`,
  spdEyebrow: "SPD Configurator",
  spdH1: "Find the right surge protection device",
  spdDesc:
    "Answer a few questions about your installation to reach the right Surge Protection product family.",
  spdStartOver: "Start over",
  searchTitle: "Search",
  searchNoResults: "No results. Try a different search term.",
  matchTitle: "Search",
  metaSiteTitle: "Selection Guide 2026 Europe | Mersen Electrical Protection",
  metaSiteDescription:
    "Interactive selection guide for electrical protection products: low and medium voltage fuses, high-speed fuses, surge protection devices, and photovoltaic solutions.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/en",
  sendRequestNav: "Send a Request",
  sendRequestCardTitle: "Send a Request",
  sendRequestCardDesc:
    "Get in touch with your local Mersen team about a product or project.",
  sendRequestEyebrow: "Contact Us",
  sendRequestH1: "Send a request",
  sendRequestDesc:
    "Select your country and we'll route your request to the right contact.",
  sendRequestCountryLabel: "Country",
  sendRequestCountryPlaceholder: "Select your country...",
  sendRequestFirstNameLabel: "First name",
  sendRequestLastNameLabel: "Last name",
  sendRequestCompanyLabel: "Company (optional)",
  sendRequestTypeLabel: "Request",
  sendRequestTypePlaceholder: "Select a request type...",
  sendRequestTypeFuse: "Fuse",
  sendRequestTypeSurge: "Surge Protection",
  sendRequestTypeBoth: "Fuse & Surge Protection",
  sendRequestEmailLabel: "Your email",
  sendRequestEmailPlaceholder: "name@example.com",
  sendRequestMessageLabel: "Message",
  sendRequestMessagePlaceholder: "Write your message...",
  sendRequestButton: "Open in Mail App",
  sendRequestSentTo: (country) =>
    `Your request will be sent to our ${country} team.`,
  sendRequestSubjectPrefix: "Website contact request",
  sendRequestHint:
    "This opens your own email app with everything pre-filled — just click Send from there.",
};

const fr: Dict = {
  guideHome: "Accueil du guide",
  crossReferenceSearch: "Recherche par référence concurrente",
  spdConfigurator: "Configurateur SPD",
  searchPlaceholderHeader: "Rechercher dans le guide... (fusibles, SPD, tension...)",
  searchPlaceholderHero: "Rechercher dans le guide... (fusibles, SPD, tension...)",
  home: "Accueil",
  back: "Retour",
  documentation: "Documentation",
  filterReferences: "Filtrer les références...",
  noReferencesFound: "Aucune référence trouvée.",
  noResultsFor: (q) => `Aucun résultat pour « ${q} »`,
  viewAllResultsFor: (q) => `Voir tous les résultats pour « ${q} » →`,
  resultsCountFor: (n, q) => `${n} résultat${n !== 1 ? "s" : ""} pour « ${q} »`,
  loading: "Chargement...",
  productSelectorFallback: "Sélecteur de produits",
  siteSubtitle: "2026 Europe",
  heroBadge: "Sélecteur de produits interactif · Édition Europe 2026",
  heroTitle1: "Guide de sélection",
  heroTitle2: "Protection électrique",
  heroDescription:
    "L'ensemble du sélecteur de produits, transformé en site web : fusibles, dispositifs de protection contre les surtensions et solutions photovoltaïques, organisés par famille de produits et entièrement consultables sur mobile, tablette et ordinateur.",
  productFamilies: "Familles de produits",
  productFamiliesDesc: "Parcourez l'ensemble du sélecteur de produits par catégorie.",
  moreTools: "Autres outils",
  moreToolsDesc: "Recherches complémentaires basées sur les mêmes données produits.",
  xrefCardTitle: "Recherche par référence concurrente",
  xrefCardDesc:
    "Trouvez la référence Mersen équivalente à une référence concurrente (Citel, Dehn, Eaton, Siemens, et plus).",
  spdCardTitle: "Configurateur SPD",
  spdCardDesc:
    "Répondez à quelques questions sur votre installation pour trouver la bonne famille de parafoudres.",
  xrefEyebrow: "Recherche par référence concurrente",
  xrefH1: "Trouvez une référence Mersen à partir d'une référence concurrente",
  xrefDesc:
    "Recherchez par référence concurrente (Citel, Dehn, Eaton, Siemens, Schneider Electric, et plus) pour trouver la pièce Mersen équivalente.",
  xrefSearchPlaceholder: "Rechercher une référence concurrente...",
  xrefResultsFor: (n, q) => `${n} résultat${n !== 1 ? "s" : ""} pour « ${q} »`,
  xrefNoResults: "Aucun résultat. Essayez une autre référence.",
  xrefMatchedVia: (brand) => `trouvé via ${brand}`,
  spdEyebrow: "Configurateur SPD",
  spdH1: "Trouvez le bon parafoudre",
  spdDesc:
    "Répondez à quelques questions sur votre installation pour identifier la bonne famille de produits de protection contre les surtensions.",
  spdStartOver: "Recommencer",
  searchTitle: "Recherche",
  searchNoResults: "Aucun résultat. Essayez un autre terme de recherche.",
  matchTitle: "Recherche",
  metaSiteTitle: "Guide de sélection 2026 Europe | Mersen Protection Électrique",
  metaSiteDescription:
    "Guide de sélection interactif pour les produits de protection électrique : fusibles basse et moyenne tension, fusibles ultra-rapides, parafoudres et solutions photovoltaïques.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/fr",
  sendRequestNav: "Envoyer une demande",
  sendRequestCardTitle: "Envoyer une demande",
  sendRequestCardDesc:
    "Rédigez un e-mail directement depuis le site : destinataire, objet et message.",
  sendRequestEyebrow: "Contactez-nous",
  sendRequestH1: "Envoyer une demande",
  sendRequestDesc:
    "Sélectionnez votre pays : votre demande sera transmise au bon interlocuteur.",
  sendRequestCountryLabel: "Pays",
  sendRequestCountryPlaceholder: "Sélectionnez votre pays...",
  sendRequestFirstNameLabel: "Prénom",
  sendRequestLastNameLabel: "Nom",
  sendRequestCompanyLabel: "Société (facultatif)",
  sendRequestTypeLabel: "Demande",
  sendRequestTypePlaceholder: "Sélectionnez un type de demande...",
  sendRequestTypeFuse: "Fusible",
  sendRequestTypeSurge: "Protection contre les surtensions",
  sendRequestTypeBoth: "Fusible et protection contre les surtensions",
  sendRequestEmailLabel: "Votre e-mail",
  sendRequestEmailPlaceholder: "nom@exemple.com",
  sendRequestMessageLabel: "Message",
  sendRequestMessagePlaceholder: "Rédigez votre message...",
  sendRequestButton: "Ouvrir dans l'application mail",
  sendRequestSentTo: (country) =>
    `Votre demande sera envoyée à notre équipe pour ${country}.`,
  sendRequestSubjectPrefix: "Demande de contact depuis le site",
  sendRequestHint:
    "Cela ouvre votre messagerie habituelle avec ces informations pré-remplies ; il ne vous reste qu'à cliquer sur Envoyer.",
};

const it: Dict = {
  guideHome: "Home del catalogo",
  crossReferenceSearch: "Ricerca per riferimento concorrente",
  spdConfigurator: "Configuratore SPD",
  searchPlaceholderHeader: "Cerca nel catalogo... (fusibili, SPD, tensione...)",
  searchPlaceholderHero: "Cerca nel catalogo... (fusibili, SPD, tensione...)",
  home: "Home",
  back: "Indietro",
  documentation: "Documentazione",
  filterReferences: "Filtra i riferimenti...",
  noReferencesFound: "Nessun riferimento trovato.",
  noResultsFor: (q) => `Nessun risultato per "${q}"`,
  viewAllResultsFor: (q) => `Vedi tutti i risultati per "${q}" →`,
  resultsCountFor: (n, q) => `${n} risultat${n !== 1 ? "i" : "o"} per "${q}"`,
  loading: "Caricamento...",
  productSelectorFallback: "Selettore di prodotti",
  siteSubtitle: "2026 Europa",
  heroBadge: "Selettore di prodotti interattivo · Edizione Europa 2026",
  heroTitle1: "Guida alla selezione",
  heroTitle2: "Protezione elettrica",
  heroDescription:
    "L'intero selettore di prodotti, trasformato in un sito web: fusibili, dispositivi di protezione contro le sovratensioni e soluzioni fotovoltaiche, organizzati per famiglia di prodotto e completamente consultabili da mobile, tablet e desktop.",
  productFamilies: "Famiglie di prodotti",
  productFamiliesDesc: "Sfoglia l'intero selettore di prodotti per categoria.",
  moreTools: "Altri strumenti",
  moreToolsDesc: "Ricerche aggiuntive basate sugli stessi dati di prodotto.",
  xrefCardTitle: "Ricerca per riferimento concorrente",
  xrefCardDesc:
    "Trova il riferimento Mersen equivalente a un codice di un concorrente (Citel, Dehn, Eaton, Siemens e altri).",
  spdCardTitle: "Configuratore SPD",
  spdCardDesc:
    "Rispondi ad alcune domande sul tuo impianto per trovare la famiglia di scaricatori di sovratensione più adatta.",
  xrefEyebrow: "Ricerca per riferimento concorrente",
  xrefH1: "Trova un riferimento Mersen a partire da un codice concorrente",
  xrefDesc:
    "Cerca per riferimento di un concorrente (Citel, Dehn, Eaton, Siemens, Schneider Electric e altri) per trovare l'articolo Mersen equivalente.",
  xrefSearchPlaceholder: "Cerca un riferimento concorrente...",
  xrefResultsFor: (n, q) => `${n} risultat${n !== 1 ? "i" : "o"} per "${q}"`,
  xrefNoResults: "Nessun risultato. Prova un altro riferimento.",
  xrefMatchedVia: (brand) => `trovato tramite ${brand}`,
  spdEyebrow: "Configuratore SPD",
  spdH1: "Trova il dispositivo di protezione da sovratensione giusto",
  spdDesc:
    "Rispondi ad alcune domande sul tuo impianto per individuare la famiglia di prodotti di protezione da sovratensione più adatta.",
  spdStartOver: "Ricomincia",
  searchTitle: "Ricerca",
  searchNoResults: "Nessun risultato. Prova un altro termine di ricerca.",
  matchTitle: "Ricerca",
  metaSiteTitle: "Guida alla selezione 2026 Europa | Mersen Protezione Elettrica",
  metaSiteDescription:
    "Guida interattiva alla selezione dei prodotti di protezione elettrica: fusibili bassa e media tensione, fusibili ultrarapidi, dispositivi di protezione da sovratensione e soluzioni fotovoltaiche.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/it",
  sendRequestNav: "Invia una richiesta",
  sendRequestCardTitle: "Invia una richiesta",
  sendRequestCardDesc:
    "Contatta il team Mersen del tuo paese per un prodotto o un progetto.",
  sendRequestEyebrow: "Contattaci",
  sendRequestH1: "Invia una richiesta",
  sendRequestDesc:
    "Seleziona il tuo paese: la tua richiesta sarà inoltrata al contatto giusto.",
  sendRequestCountryLabel: "Paese",
  sendRequestCountryPlaceholder: "Seleziona il tuo paese...",
  sendRequestFirstNameLabel: "Nome",
  sendRequestLastNameLabel: "Cognome",
  sendRequestCompanyLabel: "Azienda (facoltativo)",
  sendRequestTypeLabel: "Richiesta",
  sendRequestTypePlaceholder: "Seleziona un tipo di richiesta...",
  sendRequestTypeFuse: "Fusibile",
  sendRequestTypeSurge: "Protezione da sovratensione",
  sendRequestTypeBoth: "Fusibile e protezione da sovratensione",
  sendRequestEmailLabel: "La tua email",
  sendRequestEmailPlaceholder: "nome@esempio.com",
  sendRequestMessageLabel: "Messaggio",
  sendRequestMessagePlaceholder: "Scrivi il tuo messaggio...",
  sendRequestButton: "Apri nell'app di posta",
  sendRequestSentTo: (country) =>
    `La tua richiesta sarà inviata al nostro team per ${country}.`,
  sendRequestSubjectPrefix: "Richiesta di contatto dal sito",
  sendRequestHint:
    "Si aprirà la tua app di posta con tutto già compilato: ti basterà cliccare su Invia.",
};

const dicts: Record<Locale, Dict> = { en, fr, it };

export function t(locale: Locale): Dict {
  return dicts[locale];
}
