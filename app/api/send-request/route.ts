import { NextResponse } from "next/server";
import { Resend } from "resend";
import { getContactCountries } from "@/lib/contact-countries";

export const runtime = "nodejs";

type RequestBody = {
  countryKey?: string;
  firstName?: string;
  lastName?: string;
  company?: string;
  email?: string;
  message?: string;
  locale?: string;
};

export async function POST(request: Request) {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "Email sending is not configured on this server." },
      { status: 500 }
    );
  }

  let body: RequestBody;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 });
  }

  const { countryKey, firstName, lastName, company, email, message, locale } = body;

  if (!countryKey || !firstName?.trim() || !lastName?.trim() || !email?.trim() || !message?.trim()) {
    return NextResponse.json({ error: "Missing required fields." }, { status: 400 });
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email.trim())) {
    return NextResponse.json({ error: "Invalid email address." }, { status: 400 });
  }

  const country = getContactCountries(locale === "fr" ? "fr" : "en").find(
    (c) => c.key === countryKey
  );
  if (!country) {
    return NextResponse.json({ error: "Unknown country." }, { status: 400 });
  }

  const resend = new Resend(apiKey);

  const subject = `Website contact request – ${country.label}`;
  const bodyLines = [
    `Name: ${firstName.trim()} ${lastName.trim()}`,
    company?.trim() && `Company: ${company.trim()}`,
    `Email: ${email.trim()}`,
    `Country: ${country.label}`,
    "",
    message.trim(),
  ].filter((v): v is string => Boolean(v));

  try {
    const { error } = await resend.emails.send({
      from: process.env.SEND_REQUEST_FROM || "Selection Guide <onboarding@resend.dev>",
      to: country.email,
      replyTo: email.trim(),
      subject,
      text: bodyLines.join("\n"),
    });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 502 });
    }
  } catch {
    return NextResponse.json({ error: "Failed to send email." }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
