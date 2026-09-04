"use client";

import { useMemo, useState } from "react";
import { Mail, Send } from "lucide-react";
import { t, type Locale } from "@/lib/i18n";
import { getContactCountries } from "@/lib/contact-countries";

export default function SendRequest({ locale }: { locale: Locale }) {
  const dict = t(locale);
  const countries = useMemo(() => getContactCountries(locale), [locale]);

  const [countryKey, setCountryKey] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [company, setCompany] = useState("");
  const [requestType, setRequestType] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const selectedCountry = countries.find((c) => c.key === countryKey) ?? null;

  const requestTypeLabels: Record<string, string> = {
    fuse: dict.sendRequestTypeFuse,
    surge: dict.sendRequestTypeSurge,
    both: dict.sendRequestTypeBoth,
  };

  // Surge protection requests for France/Belgium/Luxembourg also go to
  // Mersen's local surge protection specialist, in copy.
  const SURGE_CC = "florent.ivankovics@mersen.com";
  const SURGE_CC_COUNTRIES = ["france", "belgium", "luxembourg"];
  const needsSurgeCc =
    (requestType === "surge" || requestType === "both") &&
    !!selectedCountry &&
    SURGE_CC_COUNTRIES.includes(selectedCountry.key);

  const mailtoHref = useMemo(() => {
    if (!selectedCountry) return null;

    const subject = `${dict.sendRequestSubjectPrefix} – ${selectedCountry.label}`;

    const nameLine = [firstName, lastName].filter((v) => v.trim()).join(" ");
    const infoLines = [
      nameLine && `${dict.sendRequestFirstNameLabel}/${dict.sendRequestLastNameLabel}: ${nameLine}`,
      company.trim() && `${dict.sendRequestCompanyLabel}: ${company.trim()}`,
      requestType && `${dict.sendRequestTypeLabel}: ${requestTypeLabels[requestType]}`,
      email.trim() && `${dict.sendRequestEmailLabel}: ${email.trim()}`,
    ].filter((v): v is string => Boolean(v));
    const body = [infoLines.join("\n"), message.trim()]
      .filter((v) => v)
      .join("\n\n");

    // encodeURIComponent (not URLSearchParams, which encodes spaces as "+"
    // - fine for form bodies, but many mail clients take a mailto query
    // literally and show "+" instead of a space) so spaces come through as
    // %20 and the mail app shows exactly what was typed.
    const query = [
      `subject=${encodeURIComponent(subject)}`,
      needsSurgeCc && `cc=${encodeURIComponent(SURGE_CC)}`,
      body && `body=${encodeURIComponent(body)}`,
    ]
      .filter(Boolean)
      .join("&");

    return `mailto:${selectedCountry.email}?${query}`;
  }, [selectedCountry, firstName, lastName, company, requestType, email, message, dict, needsSurgeCc]);

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (mailtoHref) window.location.href = mailtoHref;
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-10">
      <div className="mb-2 flex items-center gap-2 text-brand-600 dark:text-brand-400">
        <Mail size={18} />
        <span className="text-xs font-semibold uppercase tracking-wide">
          {dict.sendRequestEyebrow}
        </span>
      </div>
      <h1 className="mb-2 text-2xl font-bold text-ink-900 dark:text-white">
        {dict.sendRequestH1}
      </h1>
      <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
        {dict.sendRequestDesc}
      </p>

      <form
        onSubmit={onSubmit}
        className="space-y-4 rounded-lg border border-ink-200 bg-white p-5 dark:border-ink-800 dark:bg-ink-900"
      >
        <div>
          <label
            htmlFor="send-request-country"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestCountryLabel}
          </label>
          <select
            id="send-request-country"
            required
            value={countryKey}
            onChange={(e) => setCountryKey(e.target.value)}
            className="w-full rounded-lg border border-ink-200 bg-white px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          >
            <option value="" disabled>
              {dict.sendRequestCountryPlaceholder}
            </option>
            {countries.map((c) => (
              <option key={c.key} value={c.key}>
                {c.label}
              </option>
            ))}
          </select>
          {selectedCountry && (
            <p className="mt-1.5 text-xs text-ink-400 dark:text-ink-500">
              {dict.sendRequestSentTo(selectedCountry.label)}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label
              htmlFor="send-request-first-name"
              className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
            >
              {dict.sendRequestFirstNameLabel}
            </label>
            <input
              id="send-request-first-name"
              type="text"
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
            />
          </div>
          <div>
            <label
              htmlFor="send-request-last-name"
              className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
            >
              {dict.sendRequestLastNameLabel}
            </label>
            <input
              id="send-request-last-name"
              type="text"
              required
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="send-request-company"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestCompanyLabel}
          </label>
          <input
            id="send-request-company"
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="w-full rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          />
        </div>

        {locale !== "es" && (
          <div>
            <label
              htmlFor="send-request-type"
              className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
            >
              {dict.sendRequestTypeLabel}
            </label>
            <select
              id="send-request-type"
              required
              value={requestType}
              onChange={(e) => setRequestType(e.target.value)}
              className="w-full rounded-lg border border-ink-200 bg-white px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
            >
              <option value="" disabled>
                {dict.sendRequestTypePlaceholder}
              </option>
              <option value="fuse">{dict.sendRequestTypeFuse}</option>
              <option value="surge">{dict.sendRequestTypeSurge}</option>
              <option value="both">{dict.sendRequestTypeBoth}</option>
            </select>
          </div>
        )}

        <div>
          <label
            htmlFor="send-request-email"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestEmailLabel}
          </label>
          <input
            id="send-request-email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder={dict.sendRequestEmailPlaceholder}
            className="w-full rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          />
        </div>

        <div>
          <label
            htmlFor="send-request-message"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestMessageLabel}
          </label>
          <textarea
            id="send-request-message"
            rows={6}
            required
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={dict.sendRequestMessagePlaceholder}
            className="w-full resize-y rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          />
        </div>

        <button
          type="submit"
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700"
        >
          <Send size={15} />
          {dict.sendRequestButton}
        </button>
        <p className="text-center text-xs text-ink-400 dark:text-ink-500">
          {dict.sendRequestHint}
        </p>
      </form>
    </div>
  );
}
