"use client";

const messages = [
  { from: "user" as const, lines: ["sold 3 rice 15000"] },
  { from: "bot" as const, lines: ["Recorded sale:", "3 rice = 15,000"] },
  { from: "user" as const, lines: ["stock"] },
  { from: "bot" as const, lines: ["rice: 7  beans: 15"] },
  { from: "user" as const, lines: ["summary"] },
  { from: "bot" as const, lines: ["Last 7 days", "In: 45,000", "Out: 62,000"] },
];

export function PhoneMock() {
  return (
    <div className="relative mx-auto w-[min(100%,20.5rem)]">
      <div
        className="pointer-events-none absolute -inset-10 rounded-full bg-[radial-gradient(circle,rgba(198,161,91,0.16),transparent_68%)]"
        aria-hidden="true"
      />
      <div className="float-phone relative rounded-[2.1rem] bg-[#0a0908] p-[7px] shadow-[0_28px_80px_rgba(0,0,0,0.45)]">
        <div className="overflow-hidden rounded-[1.75rem] bg-panel">
          <div className="flex items-center gap-2.5 bg-[#241f1a] px-3.5 py-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gold text-[13px] font-semibold text-ink">
              T
            </div>
            <div className="min-w-0">
              <p className="truncate text-[13px] font-medium leading-tight text-cream">
                TradeBook
              </p>
              <p className="text-[11px] leading-tight text-gold">online</p>
            </div>
          </div>
          <div className="flex min-h-[26rem] flex-col gap-2.5 bg-[#171410] px-3 py-3.5">
            {messages.map((msg, i) => (
              <div
                key={`${msg.lines[0]}-${i}`}
                className={
                  msg.from === "user"
                    ? "ml-auto max-w-[85%]"
                    : "mr-auto max-w-[88%]"
                }
                style={{
                  animation: `rise 0.5s cubic-bezier(0.16, 1, 0.3, 1) ${0.35 + i * 0.28}s both`,
                }}
              >
                <div
                  className={
                    msg.from === "user"
                      ? "rounded-2xl rounded-br-md bg-gold px-3 py-2 text-[13px] leading-snug text-ink"
                      : "rounded-2xl rounded-bl-md bg-bubble px-3 py-2 text-[13px] leading-snug text-cream"
                  }
                >
                  {msg.lines.map((line) => (
                    <p key={line}>{line}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
