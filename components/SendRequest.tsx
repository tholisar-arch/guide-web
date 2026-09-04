"use client";

import { useMemo, useState } from "react";
import { Mail, Send, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { t, type Locale } from "@/lib/i18n";
import { getContactCountries } from "@/lib/contact-countries";

type Status = "idle" | "sending" | "sent" | "error";

export default function SendRequest({ locale }: { locale: Locale }) {
  const dict = t(locale);
  const countries = useMemo(() => getContactCountries(locale), [locale]);

  const [countryKey, setCountryKey] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [company, setCompany] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<Status>("idle");

  const selectedCountry = countries.find((c) => c.key === countryKey) ?? null;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedCountry || status === "sending") return;
    setStatus("sending");
    try {
      const res = await fetch("/api/send-request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          countryKey,
          firstName,
          lastName,
          company,
          email,
          message,
          locale,
        }),
      });
      if (!res.ok) throw new Error("send failed");
      setStatus("sent");
      setFirstName("");
      setLastName("");
      setCompany("");
      setEmail("");
      setMessage("");
      setCountryKey("");
    } catch {
      setStatus("error");
    }
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

      {status === "sent" ? (
        <div className="flex items-start gap-3 rounded-lg border border-emerald-200 bg-emerald-50 p-5 text-sm text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950 dark:text-emerald-300">
          <CheckCircle2 size={18} className="mt-0.5 shrink-0" />
          <p>{dict.sendRequestSuccess}</p>
        </div>
      ) : (
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

          {status === "error" && (
            <div className="flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-xs text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
              <AlertCircle size={15} className="mt-0.5 shrink-0" />
              <p>{dict.sendRequestError}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={status === "sending"}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {status === "sending" ? (
              <>
                <Loader2 size={15} className="animate-spin" />
                {dict.sendRequestSending}
              </>
            ) : (
              <>
                <Send size={15} />
                {dict.sendRequestButton}
              </>
            )}
          </button>
          <p className="text-center text-xs text-ink-400 dark:text-ink-500">
            {dict.sendRequestHint}
          </p>
        </form>
      )}
    </div>
  );
}
