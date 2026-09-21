import { NextResponse } from "next/server";

function clean(value: unknown, max: number): string {
  return String(value ?? "").trim().slice(0, max);
}

function line(label: string, value: string): string {
  return value ? `${label}: ${value}` : "";
}

export async function POST(request: Request) {
  const token = process.env.TELEGRAM_BOT_TOKEN?.trim();
  const owner = process.env.TELEGRAM_OWNER_CHAT_ID?.trim();
  if (!token || !owner) {
    return NextResponse.json(
      { ok: false, error: "Telegram delivery is not configured." },
      { status: 500 },
    );
  }

  let body: Record<string, unknown>;
  try {
    body = (await request.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json(
      { ok: false, error: "Invalid form data." },
      { status: 400 },
    );
  }

  const name = clean(body.name, 80);
  const shopName = clean(body.shopName, 80);
  const phone = clean(body.phone, 32);
  const telegram = clean(String(body.telegram ?? "").replace(/^@/, ""), 40);
  const market = clean(body.market, 80);
  const goods = clean(body.goods, 120);
  const email = clean(body.email, 80);

  if (!name || !shopName || !phone) {
    return NextResponse.json(
      { ok: false, error: "Name, stall name, and phone are required." },
      { status: 400 },
    );
  }

  const text = [
    "New stall details from the TradeBook site",
    line("Name", name),
    line("Stall", shopName),
    line("Phone", phone),
    line("Telegram", telegram ? "@" + telegram : ""),
    line("Email", email),
    line("Market", market),
    line("Sells", goods),
  ]
    .filter(Boolean)
    .join("\n");

  const telegramRes = await fetch(
    `https://api.telegram.org/bot${token}/sendMessage`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: owner, text }),
    },
  );
  const telegramJson = (await telegramRes.json()) as { ok?: boolean };

  if (!telegramRes.ok || !telegramJson.ok) {
    return NextResponse.json(
      { ok: false, error: "Could not send to Telegram." },
      { status: 502 },
    );
  }

  return NextResponse.json({ ok: true });
}
