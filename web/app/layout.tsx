import type { Metadata } from "next";
import { Cormorant_Garamond, Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["600", "700"],
  variable: "--font-cormorant",
  display: "swap",
});

export const metadata: Metadata = {
  title: "TradeBook",
  description:
    "Your stall. Your numbers. In one chat. Log sales, stock, and expenses in Telegram.",
  openGraph: {
    title: "TradeBook",
    description: "Your stall. Your numbers. In one chat.",
    images: ["/hero.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${outfit.variable} ${cormorant.variable}`}>
      <body>{children}</body>
    </html>
  );
}
