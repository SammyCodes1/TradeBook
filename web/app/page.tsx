import Image from "next/image";
import { StallMark } from "@/components/StallMark";
import { PhoneMock } from "@/components/PhoneMock";
import { JoinForm } from "@/components/JoinForm";

const telegramUrl =
  process.env.NEXT_PUBLIC_TELEGRAM_URL || "https://t.me/trade_bookbot";

const commands = [
  {
    say: "sold 3 rice 15000",
    get: "Recorded sale: 3 rice = 15,000",
    note: "Quantity, item, total money in.",
  },
  {
    say: "bought 10 rice 60000",
    get: "Recorded purchase: 10 rice = 60,000",
    note: "Stock in, total money out.",
  },
  {
    say: "expense 2000 transport",
    get: "Recorded expense: 2,000 - transport",
    note: "Anything else you spent.",
  },
  {
    say: "stock  /  summary  /  undo",
    get: "Live leftover stock, last 7 days cash, or remove the last line.",
    note: "Ask the notebook. It answers.",
  },
];

export default function HomePage() {
  return (
    <div className="relative min-h-[100dvh] overflow-x-hidden bg-ink text-cream">
      <div className="grain" />

      <header className="mx-auto flex h-16 max-w-[1120px] items-center justify-between px-5 md:h-[72px] md:px-8">
        <a href="#top" className="flex items-center gap-2.5 text-gold">
          <StallMark className="h-7 w-7" />
          <span className="font-display text-[22px] font-semibold tracking-wide">
            TRADEBOOK
          </span>
        </a>
        <nav className="hidden items-center gap-8 text-[14px] text-mute md:flex">
          <a href="#how" className="transition hover:text-cream">
            How it works
          </a>
          <a href="#traders" className="transition hover:text-cream">
            For traders
          </a>
          <a href={telegramUrl} className="text-gold transition hover:text-gold-2">
            Open Telegram
          </a>
        </nav>
      </header>

      <main id="top">
        <section className="mx-auto grid min-h-[calc(100dvh-72px)] max-w-[1120px] items-center gap-12 px-5 pb-16 pt-10 md:grid-cols-[1.05fr_0.95fr] md:gap-8 md:px-8 md:pt-8 lg:pt-4">
          <div>
            <h1 className="rise flex items-center gap-3 font-display text-[3.4rem] font-semibold leading-[0.9] tracking-tight text-gold sm:text-[5rem] lg:text-[6.2rem]">
              <StallMark className="h-10 w-10 shrink-0 sm:h-14 sm:w-14 lg:h-16 lg:w-16" />
              TRADEBOOK
            </h1>
            <p className="rise-2 mt-6 max-w-[20ch] text-[1.65rem] font-medium leading-[1.15] text-cream md:text-[1.85rem]">
              Your stall. Your numbers. In one chat.
            </p>
            <p className="rise-3 mt-4 max-w-[36ch] text-[15px] leading-relaxed text-mute md:text-base">
              Log sales, stock, and expenses in Telegram. Know what you have
              left and what the week paid you.
            </p>
            <div className="rise-3 mt-8 flex flex-wrap items-center gap-3">
              <a
                href={telegramUrl}
                className="inline-flex items-center rounded-full bg-gold px-6 py-3 text-[15px] font-medium text-ink transition duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-gold-2 active:scale-[0.98]"
              >
                Open Telegram
              </a>
              <a
                href="#how"
                className="inline-flex items-center rounded-full border border-gold/25 px-6 py-3 text-[15px] font-medium text-cream transition duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] hover:border-gold hover:text-gold active:scale-[0.98]"
              >
                See how it works
              </a>
            </div>
          </div>
          <PhoneMock />
        </section>

        <section id="how" className="border-t border-gold/10 bg-ink-2 py-24 md:py-28">
          <div className="mx-auto max-w-[1120px] px-5 md:px-8">
            <h2 className="max-w-[16ch] font-display text-4xl font-semibold leading-[1.1] text-gold md:text-5xl">
              Three texts. That is the whole book.
            </h2>
            <div className="mt-12 grid gap-3">
              {commands.map((row) => (
                <div
                  key={row.say}
                  className="grid items-center gap-3 rounded-2xl bg-ink px-5 py-5 md:grid-cols-[0.9fr_1.1fr] md:gap-8 md:px-7"
                >
                  <p className="font-medium text-gold">{row.say}</p>
                  <div>
                    <p className="text-cream">{row.get}</p>
                    <p className="mt-1 text-[13px] text-mute">{row.note}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="traders" className="py-24 md:py-28">
          <div className="mx-auto max-w-[1120px] px-5 md:px-8">
            <div className="grid gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
              <div>
                <h2 className="font-display text-4xl font-semibold leading-[1.1] text-gold md:text-5xl">
                  Built for the stall, not the office.
                </h2>
                <p className="mt-5 max-w-[42ch] text-[16px] leading-relaxed text-mute">
                  Paper notebooks get wet, torn, or left at home. Accounting
                  apps ask for menus you do not have time for. TradeBook is the
                  chat you already open, used as a ledger.
                </p>
                <p className="mt-4 max-w-[42ch] text-[16px] leading-relaxed text-mute">
                  Type with one hand while you pack goods with the other. Your
                  stock and week stay on record.
                </p>
                <a
                  href="#join"
                  className="mt-8 inline-flex items-center text-[15px] font-medium text-gold transition hover:text-gold-2"
                >
                  Leave your stall details
                </a>
              </div>
              <div className="overflow-hidden rounded-[1.6rem] border border-gold/15">
                <Image
                  src="/hero.png"
                  alt="TradeBook chat on a phone next to the TRADEBOOK wordmark"
                  width={1200}
                  height={800}
                  className="h-full w-full object-cover"
                  priority
                />
              </div>
            </div>
          </div>
        </section>

        <section
          id="join"
          className="border-t border-gold/10 bg-ink-2 py-24 md:py-28"
        >
          <div className="mx-auto grid max-w-[1120px] gap-10 px-5 md:px-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">
            <div>
              <h2 className="font-display text-4xl font-semibold leading-[1.1] text-gold md:text-5xl">
                Put your stall on the book.
              </h2>
              <p className="mt-5 max-w-[36ch] text-[16px] leading-relaxed text-mute">
                Enter your details once. They go to TradeBook on Telegram.
                Then you log every sale in the chat.
              </p>
            </div>
            <JoinForm />
          </div>
        </section>
      </main>

      <footer className="border-t border-gold/10">
        <div className="mx-auto flex max-w-[1120px] items-center justify-between px-5 py-8 md:px-8">
          <p className="font-display text-lg font-semibold tracking-wide text-gold">
            TradeBook
          </p>
          <a
            href={telegramUrl}
            className="text-[14px] text-mute transition hover:text-gold"
          >
            Open Telegram
          </a>
        </div>
      </footer>
    </div>
  );
}
