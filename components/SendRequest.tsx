"use client";

import { useMemo, useState } from "react";
import { Mail, Send } from "lucide-react";
import { t, type Locale } from "@/lib/i18n";

export default function SendRequest({ locale }: { locale: Locale }) {
  const dict = t(locale);
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const mailtoHref = useMemo(() => {
    // encodeURIComponent (not URLSearchParams, which encodes spaces as "+"
    // - fine for form bodies, but many mail clients take a mailto query
    // literally and show "+" instead of a space) so spaces come through as
    // %20 and the mail app shows exactly what was typed.
    const parts = [];
    if (subject.trim()) parts.push(`subject=${encodeURIComponent(subject)}`);
    if (message.trim()) parts.push(`body=${encodeURIComponent(message)}`);
    const query = parts.join("&");
    return `mailto:${to.trim()}${query ? `?${query}` : ""}`;
  }, [to, subject, message]);

  const canSend = to.trim().length > 3 && to.includes("@");

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
        onSubmit={(e) => e.preventDefault()}
        className="space-y-4 rounded-lg border border-ink-200 bg-white p-5 dark:border-ink-800 dark:bg-ink-900"
      >
        <div>
          <label
            htmlFor="send-request-to"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestToLabel}
          </label>
          <input
            id="send-request-to"
            type="email"
            required
            value={to}
            onChange={(e) => setTo(e.target.value)}
            placeholder={dict.sendRequestToPlaceholder}
            className="w-full rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          />
        </div>

        <div>
          <label
            htmlFor="send-request-subject"
            className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-500 dark:text-ink-400"
          >
            {dict.sendRequestSubjectLabel}
          </label>
          <input
            id="send-request-subject"
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder={dict.sendRequestSubjectPlaceholder}
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
            rows={8}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={dict.sendRequestMessagePlaceholder}
            className="w-full resize-y rounded-lg border border-ink-200 px-3 py-2 text-sm text-ink-800 outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-ink-700 dark:bg-ink-950 dark:text-ink-100 dark:focus:ring-brand-950"
          />
        </div>

        <a
          href={canSend ? mailtoHref : undefined}
          aria-disabled={!canSend}
          className={`flex w-full items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition ${
            canSend
              ? "bg-brand-600 text-white hover:bg-brand-700"
              : "cursor-not-allowed bg-ink-100 text-ink-400 dark:bg-ink-800 dark:text-ink-600"
          }`}
        >
          <Send size={15} />
          {dict.sendRequestButton}
        </a>
        <p className="text-center text-xs text-ink-400 dark:text-ink-500">
          {dict.sendRequestHint}
        </p>
      </form>
    </div>
  );
}
