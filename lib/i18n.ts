export type Locale = "en" | "fr" | "it" | "de" | "nl" | "hu" | "pt" | "pl" | "ro" | "cs";

// Kept in alphabetical order by display label (LOCALE_LABELS below) since
// the language switcher renders this list as-is.
export const LOCALES: Locale[] = ["cs", "de", "en", "fr", "it", "hu", "nl", "pl", "pt", "ro"];

export const LOCALE_LABELS: Record<Locale, string> = {
  en: "English",
  fr: "Français",
  it: "Italiano",
  de: "Deutsch",
  nl: "Nederlands",
  hu: "Magyar",
  pt: "Português",
  pl: "Polski",
  ro: "Română",
  cs: "Čeština",
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

const de: Dict = {
  guideHome: "Katalog-Startseite",
  crossReferenceSearch: "Kreuzreferenzsuche",
  spdConfigurator: "SPD-Konfigurator",
  searchPlaceholderHeader: "Katalog durchsuchen... (Sicherungen, SPD, Spannung...)",
  searchPlaceholderHero: "Katalog durchsuchen... (Sicherungen, SPD, Spannung...)",
  home: "Startseite",
  back: "Zurück",
  documentation: "Dokumentation",
  filterReferences: "Referenzen filtern...",
  noReferencesFound: "Keine Referenzen gefunden.",
  noResultsFor: (q) => `Keine Ergebnisse für „${q}"`,
  viewAllResultsFor: (q) => `Alle Ergebnisse für „${q}" anzeigen →`,
  resultsCountFor: (n, q) => `${n} Ergebnis${n !== 1 ? "se" : ""} für „${q}"`,
  loading: "Wird geladen...",
  productSelectorFallback: "Produktselektor",
  siteSubtitle: "2026 Europa",
  heroBadge: "Interaktiver Produktselektor · Ausgabe Europa 2026",
  heroTitle1: "Auswahlhilfe",
  heroTitle2: "Elektrischer Schutz",
  heroDescription:
    "Der gesamte Produktselektor, als Website: Sicherungen, Überspannungsschutzgeräte und Photovoltaik-Lösungen, nach Produktfamilie geordnet und vollständig auf Mobilgerät, Tablet und Desktop nutzbar.",
  productFamilies: "Produktfamilien",
  productFamiliesDesc: "Durchsuchen Sie den gesamten Produktselektor nach Kategorie.",
  moreTools: "Weitere Tools",
  moreToolsDesc: "Zusätzliche Suchfunktionen auf Basis derselben Produktdaten.",
  xrefCardTitle: "Kreuzreferenzsuche",
  xrefCardDesc:
    "Finden Sie die entsprechende Mersen-Referenz zu einer Wettbewerber-Artikelnummer (Citel, Dehn, Eaton, Siemens und mehr).",
  spdCardTitle: "SPD-Konfigurator",
  spdCardDesc:
    "Beantworten Sie einige Fragen zu Ihrer Anlage, um die passende Überspannungsschutz-Produktfamilie zu finden.",
  xrefEyebrow: "Kreuzreferenzsuche",
  xrefH1: "Mersen-Referenz anhand einer Wettbewerber-Artikelnummer finden",
  xrefDesc:
    "Suchen Sie anhand einer Wettbewerber-Referenz (Citel, Dehn, Eaton, Siemens, Schneider Electric und mehr), um das entsprechende Mersen-Produkt zu finden.",
  xrefSearchPlaceholder: "Wettbewerber-Referenz suchen...",
  xrefResultsFor: (n, q) => `${n} Ergebnis${n !== 1 ? "se" : ""} für „${q}"`,
  xrefNoResults: "Keine Ergebnisse. Versuchen Sie eine andere Referenz.",
  xrefMatchedVia: (brand) => `gefunden über ${brand}`,
  spdEyebrow: "SPD-Konfigurator",
  spdH1: "Das richtige Überspannungsschutzgerät finden",
  spdDesc:
    "Beantworten Sie einige Fragen zu Ihrer Anlage, um die passende Überspannungsschutz-Produktfamilie zu finden.",
  spdStartOver: "Neu starten",
  searchTitle: "Suche",
  searchNoResults: "Keine Ergebnisse. Versuchen Sie einen anderen Suchbegriff.",
  matchTitle: "Suche",
  metaSiteTitle: "Auswahlhilfe 2026 Europa | Mersen Elektrischer Schutz",
  metaSiteDescription:
    "Interaktive Auswahlhilfe für elektrische Schutzprodukte: Nieder- und Mittelspannungssicherungen, Hochleistungssicherungen, Überspannungsschutzgeräte und Photovoltaik-Lösungen.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/de",
  sendRequestNav: "Anfrage senden",
  sendRequestCardTitle: "Anfrage senden",
  sendRequestCardDesc:
    "Nehmen Sie Kontakt mit Ihrem lokalen Mersen-Team zu einem Produkt oder Projekt auf.",
  sendRequestEyebrow: "Kontaktieren Sie uns",
  sendRequestH1: "Anfrage senden",
  sendRequestDesc:
    "Wählen Sie Ihr Land aus, damit wir Ihre Anfrage an den richtigen Ansprechpartner weiterleiten.",
  sendRequestCountryLabel: "Land",
  sendRequestCountryPlaceholder: "Land auswählen...",
  sendRequestFirstNameLabel: "Vorname",
  sendRequestLastNameLabel: "Nachname",
  sendRequestCompanyLabel: "Unternehmen (optional)",
  sendRequestTypeLabel: "Anfrage",
  sendRequestTypePlaceholder: "Anfrageart auswählen...",
  sendRequestTypeFuse: "Sicherung",
  sendRequestTypeSurge: "Überspannungsschutz",
  sendRequestTypeBoth: "Sicherung & Überspannungsschutz",
  sendRequestEmailLabel: "Ihre E-Mail",
  sendRequestEmailPlaceholder: "name@beispiel.de",
  sendRequestMessageLabel: "Nachricht",
  sendRequestMessagePlaceholder: "Schreiben Sie Ihre Nachricht...",
  sendRequestButton: "In der Mail-App öffnen",
  sendRequestSentTo: (country) =>
    `Ihre Anfrage wird an unser Team für ${country} gesendet.`,
  sendRequestSubjectPrefix: "Kontaktanfrage über die Website",
  sendRequestHint:
    "Dadurch öffnet sich Ihre eigene E-Mail-App mit bereits ausgefüllten Angaben – klicken Sie dort einfach auf Senden.",
};

const nl: Dict = {
  guideHome: "Catalogus home",
  crossReferenceSearch: "Kruisreferentie zoeken",
  spdConfigurator: "SPD-configurator",
  searchPlaceholderHeader: "Doorzoek de catalogus... (zekeringen, SPD, spanning...)",
  searchPlaceholderHero: "Doorzoek de catalogus... (zekeringen, SPD, spanning...)",
  home: "Home",
  back: "Terug",
  documentation: "Documentatie",
  filterReferences: "Referenties filteren...",
  noReferencesFound: "Geen referenties gevonden.",
  noResultsFor: (q) => `Geen resultaten voor "${q}"`,
  viewAllResultsFor: (q) => `Alle resultaten voor "${q}" bekijken →`,
  resultsCountFor: (n, q) => `${n} resulta${n !== 1 ? "ten" : "at"} voor "${q}"`,
  loading: "Laden...",
  productSelectorFallback: "Productselector",
  siteSubtitle: "2026 Europa",
  heroBadge: "Interactieve productselector · Editie Europa 2026",
  heroTitle1: "Selectiegids",
  heroTitle2: "Elektrische beveiliging",
  heroDescription:
    "De volledige productselector, omgezet naar een website: zekeringen, overspanningsbeveiligingen en fotovoltaïsche oplossingen, geordend per productfamilie en volledig te doorbladeren op mobiel, tablet en desktop.",
  productFamilies: "Productfamilies",
  productFamiliesDesc: "Blader door de volledige productselector per categorie.",
  moreTools: "Meer tools",
  moreToolsDesc: "Aanvullende zoekfuncties op basis van dezelfde productgegevens.",
  xrefCardTitle: "Kruisreferentie zoeken",
  xrefCardDesc:
    "Vind de bijbehorende Mersen-referentie voor een concurrerend artikelnummer (Citel, Dehn, Eaton, Siemens en meer).",
  spdCardTitle: "SPD-configurator",
  spdCardDesc:
    "Beantwoord enkele vragen over uw installatie om de juiste overspanningsbeveiligingsfamilie te vinden.",
  xrefEyebrow: "Kruisreferentie zoeken",
  xrefH1: "Vind een Mersen-referentie op basis van een concurrerend artikelnummer",
  xrefDesc:
    "Zoek op een referentie van een concurrent (Citel, Dehn, Eaton, Siemens, Schneider Electric en meer) om het bijbehorende Mersen-artikel te vinden.",
  xrefSearchPlaceholder: "Zoek een concurrerende referentie...",
  xrefResultsFor: (n, q) => `${n} resulta${n !== 1 ? "ten" : "at"} voor "${q}"`,
  xrefNoResults: "Geen resultaten. Probeer een andere referentie.",
  xrefMatchedVia: (brand) => `gevonden via ${brand}`,
  spdEyebrow: "SPD-configurator",
  spdH1: "Vind het juiste overspanningsbeveiligingstoestel",
  spdDesc:
    "Beantwoord enkele vragen over uw installatie om de juiste overspanningsbeveiligingsfamilie te vinden.",
  spdStartOver: "Opnieuw beginnen",
  searchTitle: "Zoeken",
  searchNoResults: "Geen resultaten. Probeer een andere zoekterm.",
  matchTitle: "Zoeken",
  metaSiteTitle: "Selectiegids 2026 Europa | Mersen Elektrische Beveiliging",
  metaSiteDescription:
    "Interactieve selectiegids voor elektrische beveiligingsproducten: laag- en middenspanningszekeringen, snelle zekeringen, overspanningsbeveiligingen en fotovoltaïsche oplossingen.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/nl",
  sendRequestNav: "Aanvraag versturen",
  sendRequestCardTitle: "Aanvraag versturen",
  sendRequestCardDesc:
    "Neem contact op met uw lokale Mersen-team over een product of project.",
  sendRequestEyebrow: "Neem contact op",
  sendRequestH1: "Een aanvraag versturen",
  sendRequestDesc:
    "Selecteer uw land en wij sturen uw aanvraag door naar de juiste contactpersoon.",
  sendRequestCountryLabel: "Land",
  sendRequestCountryPlaceholder: "Selecteer uw land...",
  sendRequestFirstNameLabel: "Voornaam",
  sendRequestLastNameLabel: "Achternaam",
  sendRequestCompanyLabel: "Bedrijf (optioneel)",
  sendRequestTypeLabel: "Aanvraag",
  sendRequestTypePlaceholder: "Selecteer een type aanvraag...",
  sendRequestTypeFuse: "Zekering",
  sendRequestTypeSurge: "Overspanningsbeveiliging",
  sendRequestTypeBoth: "Zekering & overspanningsbeveiliging",
  sendRequestEmailLabel: "Uw e-mail",
  sendRequestEmailPlaceholder: "naam@voorbeeld.nl",
  sendRequestMessageLabel: "Bericht",
  sendRequestMessagePlaceholder: "Schrijf uw bericht...",
  sendRequestButton: "Openen in e-mailapp",
  sendRequestSentTo: (country) =>
    `Uw aanvraag wordt verzonden naar ons team voor ${country}.`,
  sendRequestSubjectPrefix: "Contactaanvraag via de website",
  sendRequestHint:
    "Hierdoor opent uw eigen e-mailapp met alles al ingevuld — klik daar gewoon op Verzenden.",
};

const hu: Dict = {
  guideHome: "Katalógus kezdőlap",
  crossReferenceSearch: "Kereszthivatkozás-kereső",
  spdConfigurator: "SPD-konfigurátor",
  searchPlaceholderHeader: "Keresés a katalógusban... (biztosítékok, SPD, feszültség...)",
  searchPlaceholderHero: "Keresés a katalógusban... (biztosítékok, SPD, feszültség...)",
  home: "Kezdőlap",
  back: "Vissza",
  documentation: "Dokumentáció",
  filterReferences: "Referenciák szűrése...",
  noReferencesFound: "Nem található referencia.",
  noResultsFor: (q) => `Nincs találat erre: "${q}"`,
  viewAllResultsFor: (q) => `Összes találat megtekintése erre: "${q}" →`,
  resultsCountFor: (n, q) => `${n} találat erre: "${q}"`,
  loading: "Betöltés...",
  productSelectorFallback: "Termékválasztó",
  siteSubtitle: "2026 Európa",
  heroBadge: "Interaktív termékválasztó · 2026-os európai kiadás",
  heroTitle1: "Kiválasztási útmutató",
  heroTitle2: "Elektromos védelem",
  heroDescription:
    "A teljes termékválasztó weboldallá alakítva: biztosítékok, túlfeszültség-védelmi eszközök és fotovoltaikus megoldások, termékcsalád szerint rendezve, teljes mértékben böngészhető mobilon, tableten és asztali gépen.",
  productFamilies: "Termékcsaládok",
  productFamiliesDesc: "Böngéssze a teljes termékválasztót kategória szerint.",
  moreTools: "További eszközök",
  moreToolsDesc: "Kiegészítő keresések ugyanazon terméklista alapján.",
  xrefCardTitle: "Kereszthivatkozás-kereső",
  xrefCardDesc:
    "Keresse meg a megfelelő Mersen referenciát egy versenytárs cikkszámához (Citel, Dehn, Eaton, Siemens és mások).",
  spdCardTitle: "SPD-konfigurátor",
  spdCardDesc:
    "Válaszoljon néhány kérdésre az Ön rendszeréről, hogy megtalálja a megfelelő túlfeszültségvédelmi termékcsaládot.",
  xrefEyebrow: "Kereszthivatkozás-kereső",
  xrefH1: "Mersen referencia keresése versenytárs cikkszám alapján",
  xrefDesc:
    "Keressen egy versenytárs referenciája alapján (Citel, Dehn, Eaton, Siemens, Schneider Electric és mások), hogy megtalálja a megfelelő Mersen terméket.",
  xrefSearchPlaceholder: "Versenytárs referencia keresése...",
  xrefResultsFor: (n, q) => `${n} találat erre: "${q}"`,
  xrefNoResults: "Nincs találat. Próbáljon másik referenciát.",
  xrefMatchedVia: (brand) => `találat itt: ${brand}`,
  spdEyebrow: "SPD-konfigurátor",
  spdH1: "Találja meg a megfelelő túlfeszültségvédelmi eszközt",
  spdDesc:
    "Válaszoljon néhány kérdésre az Ön rendszeréről, hogy megtalálja a megfelelő túlfeszültségvédelmi termékcsaládot.",
  spdStartOver: "Újrakezdés",
  searchTitle: "Keresés",
  searchNoResults: "Nincs találat. Próbáljon másik keresési kifejezést.",
  matchTitle: "Keresés",
  metaSiteTitle: "Kiválasztási útmutató 2026 Európa | Mersen Elektromos Védelem",
  metaSiteDescription:
    "Interaktív kiválasztási útmutató elektromos védelmi termékekhez: kis- és középfeszültségű biztosítékok, gyorsbiztosítékok, túlfeszültség-védelmi eszközök és fotovoltaikus megoldások.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/hu",
  sendRequestNav: "Kérés küldése",
  sendRequestCardTitle: "Kérés küldése",
  sendRequestCardDesc:
    "Vegye fel a kapcsolatot a helyi Mersen csapattal egy termékkel vagy projekttel kapcsolatban.",
  sendRequestEyebrow: "Kapcsolat",
  sendRequestH1: "Kérés küldése",
  sendRequestDesc:
    "Válassza ki az országát, és a kérését továbbítjuk a megfelelő kapcsolattartóhoz.",
  sendRequestCountryLabel: "Ország",
  sendRequestCountryPlaceholder: "Válasszon országot...",
  sendRequestFirstNameLabel: "Keresztnév",
  sendRequestLastNameLabel: "Vezetéknév",
  sendRequestCompanyLabel: "Cég (opcionális)",
  sendRequestTypeLabel: "Kérés típusa",
  sendRequestTypePlaceholder: "Válasszon kéréstípust...",
  sendRequestTypeFuse: "Biztosíték",
  sendRequestTypeSurge: "Túlfeszültség-védelem",
  sendRequestTypeBoth: "Biztosíték és túlfeszültség-védelem",
  sendRequestEmailLabel: "Az Ön e-mail címe",
  sendRequestEmailPlaceholder: "nev@pelda.hu",
  sendRequestMessageLabel: "Üzenet",
  sendRequestMessagePlaceholder: "Írja meg üzenetét...",
  sendRequestButton: "Megnyitás a levelezőprogramban",
  sendRequestSentTo: (country) =>
    `A kérését elküldjük a(z) ${country} csapatunknak.`,
  sendRequestSubjectPrefix: "Kapcsolatfelvételi kérés a weboldalról",
  sendRequestHint:
    "Ez megnyitja saját levelezőprogramját mindennel előre kitöltve — csak kattintson a Küldésre.",
};

const pt: Dict = {
  guideHome: "Início do catálogo",
  crossReferenceSearch: "Pesquisa por referência concorrente",
  spdConfigurator: "Configurador SPD",
  searchPlaceholderHeader: "Pesquisar no catálogo... (fusíveis, SPD, tensão...)",
  searchPlaceholderHero: "Pesquisar no catálogo... (fusíveis, SPD, tensão...)",
  home: "Início",
  back: "Voltar",
  documentation: "Documentação",
  filterReferences: "Filtrar referências...",
  noReferencesFound: "Nenhuma referência encontrada.",
  noResultsFor: (q) => `Nenhum resultado para "${q}"`,
  viewAllResultsFor: (q) => `Ver todos os resultados para "${q}" →`,
  resultsCountFor: (n, q) => `${n} resultado${n !== 1 ? "s" : ""} para "${q}"`,
  loading: "A carregar...",
  productSelectorFallback: "Seletor de produtos",
  siteSubtitle: "2026 Europa",
  heroBadge: "Seletor de produtos interativo · Edição Europa 2026",
  heroTitle1: "Guia de seleção",
  heroTitle2: "Proteção elétrica",
  heroDescription:
    "Todo o seletor de produtos, transformado num website: fusíveis, dispositivos de proteção contra sobretensões e soluções fotovoltaicas, organizados por família de produtos e totalmente navegáveis em telemóvel, tablet e computador.",
  productFamilies: "Famílias de produtos",
  productFamiliesDesc: "Explore todo o seletor de produtos por categoria.",
  moreTools: "Mais ferramentas",
  moreToolsDesc: "Pesquisas adicionais baseadas nos mesmos dados de produto.",
  xrefCardTitle: "Pesquisa por referência concorrente",
  xrefCardDesc:
    "Encontre a referência Mersen equivalente a uma referência da concorrência (Citel, Dehn, Eaton, Siemens, entre outras).",
  spdCardTitle: "Configurador SPD",
  spdCardDesc:
    "Responda a algumas perguntas sobre a sua instalação para encontrar a família de proteção contra sobretensões adequada.",
  xrefEyebrow: "Pesquisa por referência concorrente",
  xrefH1: "Encontre uma referência Mersen a partir de uma referência concorrente",
  xrefDesc:
    "Pesquise por uma referência da concorrência (Citel, Dehn, Eaton, Siemens, Schneider Electric, entre outras) para encontrar a peça Mersen equivalente.",
  xrefSearchPlaceholder: "Pesquisar uma referência concorrente...",
  xrefResultsFor: (n, q) => `${n} resultado${n !== 1 ? "s" : ""} para "${q}"`,
  xrefNoResults: "Nenhum resultado. Tente outra referência.",
  xrefMatchedVia: (brand) => `correspondência via ${brand}`,
  spdEyebrow: "Configurador SPD",
  spdH1: "Encontre o dispositivo de proteção contra sobretensões adequado",
  spdDesc:
    "Responda a algumas perguntas sobre a sua instalação para chegar à família de produtos de proteção contra sobretensões adequada.",
  spdStartOver: "Recomeçar",
  searchTitle: "Pesquisa",
  searchNoResults: "Nenhum resultado. Tente outro termo de pesquisa.",
  matchTitle: "Pesquisa",
  metaSiteTitle: "Guia de seleção 2026 Europa | Mersen Proteção Elétrica",
  metaSiteDescription:
    "Guia de seleção interativo para produtos de proteção elétrica: fusíveis de baixa e média tensão, fusíveis ultrarrápidos, dispositivos de proteção contra sobretensões e soluções fotovoltaicas.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/pt",
  sendRequestNav: "Enviar um pedido",
  sendRequestCardTitle: "Enviar um pedido",
  sendRequestCardDesc:
    "Entre em contacto com a sua equipa Mersen local sobre um produto ou projeto.",
  sendRequestEyebrow: "Contacte-nos",
  sendRequestH1: "Enviar um pedido",
  sendRequestDesc:
    "Selecione o seu país e encaminharemos o seu pedido para o contacto certo.",
  sendRequestCountryLabel: "País",
  sendRequestCountryPlaceholder: "Selecione o seu país...",
  sendRequestFirstNameLabel: "Nome próprio",
  sendRequestLastNameLabel: "Apelido",
  sendRequestCompanyLabel: "Empresa (opcional)",
  sendRequestTypeLabel: "Pedido",
  sendRequestTypePlaceholder: "Selecione um tipo de pedido...",
  sendRequestTypeFuse: "Fusível",
  sendRequestTypeSurge: "Proteção contra sobretensões",
  sendRequestTypeBoth: "Fusível e proteção contra sobretensões",
  sendRequestEmailLabel: "O seu e-mail",
  sendRequestEmailPlaceholder: "nome@exemplo.pt",
  sendRequestMessageLabel: "Mensagem",
  sendRequestMessagePlaceholder: "Escreva a sua mensagem...",
  sendRequestButton: "Abrir na aplicação de e-mail",
  sendRequestSentTo: (country) =>
    `O seu pedido será enviado para a nossa equipa de ${country}.`,
  sendRequestSubjectPrefix: "Pedido de contacto através do site",
  sendRequestHint:
    "Isto abre a sua própria aplicação de e-mail com tudo já preenchido — basta clicar em Enviar.",
};

const pl: Dict = {
  guideHome: "Strona główna katalogu",
  crossReferenceSearch: "Wyszukiwarka zamienników",
  spdConfigurator: "Konfigurator SPD",
  searchPlaceholderHeader: "Szukaj w katalogu... (bezpieczniki, SPD, napięcie...)",
  searchPlaceholderHero: "Szukaj w katalogu... (bezpieczniki, SPD, napięcie...)",
  home: "Strona główna",
  back: "Wstecz",
  documentation: "Dokumentacja",
  filterReferences: "Filtruj referencje...",
  noReferencesFound: "Nie znaleziono żadnych referencji.",
  noResultsFor: (q) => `Brak wyników dla „${q}"`,
  viewAllResultsFor: (q) => `Zobacz wszystkie wyniki dla „${q}" →`,
  resultsCountFor: (n, q) => `${n} wynik${n !== 1 ? "i" : ""} dla „${q}"`,
  loading: "Ładowanie...",
  productSelectorFallback: "Selektor produktów",
  siteSubtitle: "2026 Europa",
  heroBadge: "Interaktywny selektor produktów · Edycja Europa 2026",
  heroTitle1: "Przewodnik wyboru",
  heroTitle2: "Ochrona elektryczna",
  heroDescription:
    "Cały selektor produktów przekształcony w stronę internetową: bezpieczniki, urządzenia ochrony przeciwprzepięciowej i rozwiązania fotowoltaiczne, uporządkowane według rodziny produktów i w pełni dostępne na telefonie, tablecie i komputerze.",
  productFamilies: "Rodziny produktów",
  productFamiliesDesc: "Przeglądaj cały selektor produktów według kategorii.",
  moreTools: "Więcej narzędzi",
  moreToolsDesc: "Dodatkowe wyszukiwarki oparte na tych samych danych produktowych.",
  xrefCardTitle: "Wyszukiwarka zamienników",
  xrefCardDesc:
    "Znajdź odpowiednik Mersen dla numeru katalogowego konkurencji (Citel, Dehn, Eaton, Siemens i inne).",
  spdCardTitle: "Konfigurator SPD",
  spdCardDesc:
    "Odpowiedz na kilka pytań dotyczących instalacji, aby znaleźć odpowiednią rodzinę ochrony przeciwprzepięciowej.",
  xrefEyebrow: "Wyszukiwarka zamienników",
  xrefH1: "Znajdź referencję Mersen na podstawie numeru katalogowego konkurencji",
  xrefDesc:
    "Wyszukaj według numeru katalogowego konkurencji (Citel, Dehn, Eaton, Siemens, Schneider Electric i inne), aby znaleźć odpowiedni produkt Mersen.",
  xrefSearchPlaceholder: "Szukaj numeru katalogowego konkurencji...",
  xrefResultsFor: (n, q) => `${n} wynik${n !== 1 ? "i" : ""} dla „${q}"`,
  xrefNoResults: "Brak wyników. Spróbuj innej referencji.",
  xrefMatchedVia: (brand) => `dopasowano przez ${brand}`,
  spdEyebrow: "Konfigurator SPD",
  spdH1: "Znajdź odpowiednie urządzenie ochrony przeciwprzepięciowej",
  spdDesc:
    "Odpowiedz na kilka pytań dotyczących instalacji, aby znaleźć odpowiednią rodzinę produktów ochrony przeciwprzepięciowej.",
  spdStartOver: "Zacznij od nowa",
  searchTitle: "Wyszukiwanie",
  searchNoResults: "Brak wyników. Spróbuj innego wyszukiwanego hasła.",
  matchTitle: "Wyszukiwanie",
  metaSiteTitle: "Przewodnik wyboru 2026 Europa | Mersen Ochrona Elektryczna",
  metaSiteDescription:
    "Interaktywny przewodnik wyboru produktów ochrony elektrycznej: bezpieczniki niskiego i średniego napięcia, bezpieczniki szybkie, urządzenia ochrony przeciwprzepięciowej i rozwiązania fotowoltaiczne.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/pl",
  sendRequestNav: "Wyślij zapytanie",
  sendRequestCardTitle: "Wyślij zapytanie",
  sendRequestCardDesc:
    "Skontaktuj się z lokalnym zespołem Mersen w sprawie produktu lub projektu.",
  sendRequestEyebrow: "Skontaktuj się z nami",
  sendRequestH1: "Wyślij zapytanie",
  sendRequestDesc:
    "Wybierz swój kraj, a przekierujemy Twoje zapytanie do właściwej osoby kontaktowej.",
  sendRequestCountryLabel: "Kraj",
  sendRequestCountryPlaceholder: "Wybierz swój kraj...",
  sendRequestFirstNameLabel: "Imię",
  sendRequestLastNameLabel: "Nazwisko",
  sendRequestCompanyLabel: "Firma (opcjonalnie)",
  sendRequestTypeLabel: "Zapytanie",
  sendRequestTypePlaceholder: "Wybierz rodzaj zapytania...",
  sendRequestTypeFuse: "Bezpiecznik",
  sendRequestTypeSurge: "Ochrona przeciwprzepięciowa",
  sendRequestTypeBoth: "Bezpiecznik i ochrona przeciwprzepięciowa",
  sendRequestEmailLabel: "Twój e-mail",
  sendRequestEmailPlaceholder: "imie@przyklad.pl",
  sendRequestMessageLabel: "Wiadomość",
  sendRequestMessagePlaceholder: "Napisz swoją wiadomość...",
  sendRequestButton: "Otwórz w aplikacji pocztowej",
  sendRequestSentTo: (country) =>
    `Twoje zapytanie zostanie wysłane do naszego zespołu dla: ${country}.`,
  sendRequestSubjectPrefix: "Zapytanie kontaktowe ze strony internetowej",
  sendRequestHint:
    "Spowoduje to otwarcie Twojej aplikacji pocztowej z gotowymi danymi — wystarczy kliknąć Wyślij.",
};

const ro: Dict = {
  guideHome: "Pagina principală a catalogului",
  crossReferenceSearch: "Căutare referințe încrucișate",
  spdConfigurator: "Configurator SPD",
  searchPlaceholderHeader: "Căutați în catalog... (siguranțe, SPD, tensiune...)",
  searchPlaceholderHero: "Căutați în catalog... (siguranțe, SPD, tensiune...)",
  home: "Acasă",
  back: "Înapoi",
  documentation: "Documentație",
  filterReferences: "Filtrați referințele...",
  noReferencesFound: "Nu a fost găsită nicio referință.",
  noResultsFor: (q) => `Niciun rezultat pentru „${q}"`,
  viewAllResultsFor: (q) => `Vedeți toate rezultatele pentru „${q}" →`,
  resultsCountFor: (n, q) => `${n} rezultat${n !== 1 ? "e" : ""} pentru „${q}"`,
  loading: "Se încarcă...",
  productSelectorFallback: "Selector de produse",
  siteSubtitle: "2026 Europa",
  heroBadge: "Selector de produse interactiv · Ediția Europa 2026",
  heroTitle1: "Ghid de selecție",
  heroTitle2: "Protecție electrică",
  heroDescription:
    "Întregul selector de produse, transformat într-un site web: siguranțe, dispozitive de protecție la supratensiuni și soluții fotovoltaice, organizate pe familii de produse și complet accesibile pe mobil, tabletă și desktop.",
  productFamilies: "Familii de produse",
  productFamiliesDesc: "Răsfoiți întregul selector de produse pe categorii.",
  moreTools: "Mai multe instrumente",
  moreToolsDesc: "Căutări suplimentare bazate pe aceleași date de produs.",
  xrefCardTitle: "Căutare referințe încrucișate",
  xrefCardDesc:
    "Găsiți referința Mersen echivalentă unui cod de produs al concurenței (Citel, Dehn, Eaton, Siemens și altele).",
  spdCardTitle: "Configurator SPD",
  spdCardDesc:
    "Răspundeți la câteva întrebări despre instalația dumneavoastră pentru a găsi familia potrivită de protecție la supratensiuni.",
  xrefEyebrow: "Căutare referințe încrucișate",
  xrefH1: "Găsiți o referință Mersen pornind de la un cod al concurenței",
  xrefDesc:
    "Căutați după o referință a concurenței (Citel, Dehn, Eaton, Siemens, Schneider Electric și altele) pentru a găsi produsul Mersen echivalent.",
  xrefSearchPlaceholder: "Căutați o referință a concurenței...",
  xrefResultsFor: (n, q) => `${n} rezultat${n !== 1 ? "e" : ""} pentru „${q}"`,
  xrefNoResults: "Niciun rezultat. Încercați o altă referință.",
  xrefMatchedVia: (brand) => `găsit prin ${brand}`,
  spdEyebrow: "Configurator SPD",
  spdH1: "Găsiți dispozitivul potrivit de protecție la supratensiuni",
  spdDesc:
    "Răspundeți la câteva întrebări despre instalația dumneavoastră pentru a ajunge la familia potrivită de produse de protecție la supratensiuni.",
  spdStartOver: "Reîncepeți",
  searchTitle: "Căutare",
  searchNoResults: "Niciun rezultat. Încercați un alt termen de căutare.",
  matchTitle: "Căutare",
  metaSiteTitle: "Ghid de selecție 2026 Europa | Mersen Protecție Electrică",
  metaSiteDescription:
    "Ghid interactiv de selecție pentru produse de protecție electrică: siguranțe de joasă și medie tensiune, siguranțe ultrarapide, dispozitive de protecție la supratensiuni și soluții fotovoltaice.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/ro",
  sendRequestNav: "Trimiteți o solicitare",
  sendRequestCardTitle: "Trimiteți o solicitare",
  sendRequestCardDesc:
    "Contactați echipa Mersen locală în legătură cu un produs sau un proiect.",
  sendRequestEyebrow: "Contactați-ne",
  sendRequestH1: "Trimiteți o solicitare",
  sendRequestDesc:
    "Selectați țara dumneavoastră și vom direcționa solicitarea către persoana de contact potrivită.",
  sendRequestCountryLabel: "Țară",
  sendRequestCountryPlaceholder: "Selectați țara...",
  sendRequestFirstNameLabel: "Prenume",
  sendRequestLastNameLabel: "Nume",
  sendRequestCompanyLabel: "Companie (opțional)",
  sendRequestTypeLabel: "Solicitare",
  sendRequestTypePlaceholder: "Selectați tipul solicitării...",
  sendRequestTypeFuse: "Siguranță",
  sendRequestTypeSurge: "Protecție la supratensiuni",
  sendRequestTypeBoth: "Siguranță și protecție la supratensiuni",
  sendRequestEmailLabel: "E-mailul dumneavoastră",
  sendRequestEmailPlaceholder: "nume@exemplu.ro",
  sendRequestMessageLabel: "Mesaj",
  sendRequestMessagePlaceholder: "Scrieți mesajul dumneavoastră...",
  sendRequestButton: "Deschideți în aplicația de e-mail",
  sendRequestSentTo: (country) =>
    `Solicitarea dumneavoastră va fi trimisă echipei noastre pentru ${country}.`,
  sendRequestSubjectPrefix: "Solicitare de contact de pe site",
  sendRequestHint:
    "Aceasta vă deschide propria aplicație de e-mail cu totul completat în prealabil — trebuie doar să apăsați Trimitere.",
};

const cs: Dict = {
  guideHome: "Domovská stránka katalogu",
  crossReferenceSearch: "Vyhledávání křížových referencí",
  spdConfigurator: "Konfigurátor SPD",
  searchPlaceholderHeader: "Hledat v katalogu... (pojistky, SPD, napětí...)",
  searchPlaceholderHero: "Hledat v katalogu... (pojistky, SPD, napětí...)",
  home: "Domů",
  back: "Zpět",
  documentation: "Dokumentace",
  filterReferences: "Filtrovat reference...",
  noReferencesFound: "Nebyla nalezena žádná reference.",
  noResultsFor: (q) => `Žádné výsledky pro „${q}"`,
  viewAllResultsFor: (q) => `Zobrazit všechny výsledky pro „${q}" →`,
  resultsCountFor: (n, q) => `${n} výsledk${n !== 1 ? "y" : ""} pro „${q}"`,
  loading: "Načítání...",
  productSelectorFallback: "Výběr produktů",
  siteSubtitle: "2026 Evropa",
  heroBadge: "Interaktivní výběr produktů · Vydání Evropa 2026",
  heroTitle1: "Průvodce výběrem",
  heroTitle2: "Elektrická ochrana",
  heroDescription:
    "Celý výběr produktů převedený do podoby webu: pojistky, přepěťové ochrany a fotovoltaická řešení, uspořádané podle produktových řad a plně dostupné na mobilu, tabletu i počítači.",
  productFamilies: "Produktové řady",
  productFamiliesDesc: "Procházejte celý výběr produktů podle kategorií.",
  moreTools: "Další nástroje",
  moreToolsDesc: "Další vyhledávání založená na stejných produktových datech.",
  xrefCardTitle: "Vyhledávání křížových referencí",
  xrefCardDesc:
    "Najděte odpovídající referenci Mersen ke katalogovému číslu konkurence (Citel, Dehn, Eaton, Siemens a další).",
  spdCardTitle: "Konfigurátor SPD",
  spdCardDesc:
    "Odpovězte na několik otázek o vaší instalaci a najděte správnou řadu přepěťových ochran.",
  xrefEyebrow: "Vyhledávání křížových referencí",
  xrefH1: "Najděte referenci Mersen podle katalogového čísla konkurence",
  xrefDesc:
    "Vyhledejte podle reference konkurence (Citel, Dehn, Eaton, Siemens, Schneider Electric a další) a najděte odpovídající produkt Mersen.",
  xrefSearchPlaceholder: "Hledat referenci konkurence...",
  xrefResultsFor: (n, q) => `${n} výsledk${n !== 1 ? "y" : ""} pro „${q}"`,
  xrefNoResults: "Žádné výsledky. Zkuste jinou referenci.",
  xrefMatchedVia: (brand) => `nalezeno přes ${brand}`,
  spdEyebrow: "Konfigurátor SPD",
  spdH1: "Najděte správné přepěťové ochranné zařízení",
  spdDesc:
    "Odpovězte na několik otázek o vaší instalaci a najděte správnou řadu produktů přepěťové ochrany.",
  spdStartOver: "Začít znovu",
  searchTitle: "Vyhledávání",
  searchNoResults: "Žádné výsledky. Zkuste jiný hledaný výraz.",
  matchTitle: "Vyhledávání",
  metaSiteTitle: "Průvodce výběrem 2026 Evropa | Mersen Elektrická Ochrana",
  metaSiteDescription:
    "Interaktivní průvodce výběrem produktů elektrické ochrany: pojistky nízkého a vysokého napětí, rychlé pojistky, přepěťové ochrany a fotovoltaická řešení.",
  mersenWebsiteLabel: "mersen.com",
  mersenWebsiteUrl: "https://www.mersen.com/cs",
  sendRequestNav: "Odeslat poptávku",
  sendRequestCardTitle: "Odeslat poptávku",
  sendRequestCardDesc:
    "Kontaktujte místní tým Mersen ohledně produktu nebo projektu.",
  sendRequestEyebrow: "Kontaktujte nás",
  sendRequestH1: "Odeslat poptávku",
  sendRequestDesc:
    "Vyberte svou zemi a my vaši poptávku přesměrujeme na správný kontakt.",
  sendRequestCountryLabel: "Země",
  sendRequestCountryPlaceholder: "Vyberte svou zemi...",
  sendRequestFirstNameLabel: "Jméno",
  sendRequestLastNameLabel: "Příjmení",
  sendRequestCompanyLabel: "Společnost (nepovinné)",
  sendRequestTypeLabel: "Poptávka",
  sendRequestTypePlaceholder: "Vyberte typ poptávky...",
  sendRequestTypeFuse: "Pojistka",
  sendRequestTypeSurge: "Přepěťová ochrana",
  sendRequestTypeBoth: "Pojistka a přepěťová ochrana",
  sendRequestEmailLabel: "Váš e-mail",
  sendRequestEmailPlaceholder: "jmeno@priklad.cz",
  sendRequestMessageLabel: "Zpráva",
  sendRequestMessagePlaceholder: "Napište svou zprávu...",
  sendRequestButton: "Otevřít v e-mailové aplikaci",
  sendRequestSentTo: (country) =>
    `Vaše poptávka bude odeslána našemu týmu pro: ${country}.`,
  sendRequestSubjectPrefix: "Kontaktní poptávka z webu",
  sendRequestHint:
    "Tímto se otevře vaše e-mailová aplikace se všemi předvyplněnými údaji — stačí kliknout na Odeslat.",
};

const dicts: Record<Locale, Dict> = { en, fr, it, de, nl, hu, pt, pl, ro, cs };

export function t(locale: Locale): Dict {
  return dicts[locale];
}
