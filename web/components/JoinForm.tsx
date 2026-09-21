"use client";

import { useState, type FormEvent } from "react";
import { ArrowUpRight } from "@phosphor-icons/react/dist/csr/ArrowUpRight";
import { CheckCircle } from "@phosphor-icons/react/dist/csr/CheckCircle";

const telegramUrl =
  process.env.NEXT_PUBLIC_TELEGRAM_URL || "https://t.me/trade_bookbot";

const empty = {
  name: "",
  shopName: "",
  phone: "",
  telegram: "",
  email: "",
  market: "",
  goods: "",
};

const fields = [
  { key: "name", label: "Your name", auto: "name", required: true },
  { key: "shopName", label: "Stall or shop name", auto: "organization", required: true },
  { key: "phone", label: "Phone", auto: "tel", type: "tel", required: true },
  { key: "telegram", label: "Telegram username", auto: "username", required: false },
  { key: "email", label: "Email", auto: "email", type: "email", required: false },
  { key: "market", label: "Market or area", auto: "address-level2", required: false },
  { key: "goods", label: "What you sell", auto: "off", required: false },
] as const;

export function JoinForm() {
  const [values, setValues] = useState(empty);
  const [status, setStatus] = useState<"idle" | "saving" | "saved" | "error">(
    "idle",
  );
  const [message, setMessage] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (status === "saving") return;

    setStatus("saving");
    setMessage("");
    try {
      const res = await fetch("/api/details", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      const data = (await res.json()) as { ok?: boolean; error?: string };
      if (!res.ok || !data.ok) {
        throw new Error(data.error || "Could not send. Try again.");
      }
      setStatus("saved");
    } catch (err) {
      setStatus("error");
      setMessage(
        err instanceof Error
          ? err.message
          : "Could not send. Try again in a moment.",
      );
    }
  }

  if (status === "saved") {
    return (
      <div className="rounded-[1.6rem] border border-gold/20 bg-ink-2 p-8 md:p-10">
        <CheckCircle size={36} weight="fill" className="text-gold" />
        <h3 className="mt-4 font-display text-3xl font-semibold text-gold">
          Sent.
        </h3>
        <p className="mt-3 max-w-[36ch] text-[15px] leading-relaxed text-mute">
          Your stall details went to TradeBook. Open Telegram and start with
          sold 3 rice 15000.
        </p>
        <a
          href={telegramUrl}
          className="mt-7 inline-flex items-center gap-3 rounded-full bg-gold px-5 py-3 text-[15px] font-medium text-ink transition duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-gold-2 active:scale-[0.98]"
        >
          Open Telegram
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-ink/10">
            <ArrowUpRight size={14} weight="bold" />
          </span>
        </a>
      </div>
    );
  }

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-[1.6rem] border border-gold/20 bg-ink-2 p-6 md:p-8"
      noValidate
    >
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        {fields.map((field) => (
          <label
            key={field.key}
            className={
              field.key === "goods" || field.key === "market"
                ? "flex flex-col gap-2 md:col-span-2"
                : "flex flex-col gap-2"
            }
          >
            <span className="text-[13px] font-medium text-cream">
              {field.label}
              {field.required ? null : (
                <span className="ml-1 font-normal text-mute">optional</span>
              )}
            </span>
            <input
              name={field.key}
              type={"type" in field ? field.type : "text"}
              autoComplete={field.auto}
              required={field.required}
              value={values[field.key]}
              onChange={(e) =>
                setValues((current) => ({
                  ...current,
                  [field.key]: e.target.value,
                }))
              }
              className="rounded-xl border border-gold/15 bg-ink px-3.5 py-3 text-[15px] text-cream outline-none transition duration-300 placeholder:text-mute/60 focus:border-gold"
            />
          </label>
        ))}
      </div>

      {status === "error" ? (
        <p className="mt-4 text-[14px] text-[#e3b4a0]" role="alert">
          {message}
        </p>
      ) : null}

      <button
        type="submit"
        disabled={status === "saving"}
        className="mt-7 inline-flex w-full items-center justify-center gap-3 rounded-full bg-gold px-5 py-3.5 text-[15px] font-medium text-ink transition duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-gold-2 active:scale-[0.98] disabled:opacity-60 md:w-auto"
      >
        {status === "saving" ? "Sending" : "Send my details"}
        {status === "saving" ? null : (
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-ink/10">
            <ArrowUpRight size={14} weight="bold" />
          </span>
        )}
      </button>
    </form>
  );
}
