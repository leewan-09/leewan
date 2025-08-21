import Navbar from "@/components/navbar";
import "@/styles/globals.css";
import { SITE_CONFIG } from "@/lib/constants";
import { Analytics } from "@vercel/analytics/next";

import { type Metadata } from "next";
import { Inter } from "next/font/google";

export const metadata: Metadata = {
  title: `${SITE_CONFIG.name} - ${SITE_CONFIG.title}`,
  description: SITE_CONFIG.description,
  icons: [{ rel: "icon", url: "/favicon.svg" }],
  openGraph: {
    title: `${SITE_CONFIG.name} - ${SITE_CONFIG.title}`,
    description: SITE_CONFIG.description,
    type: "website",
  },
};

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter-sans",
  display: "swap",
});

interface RootLayoutProps {
  readonly children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased">
        <Navbar />
        <main className="m-auto w-full max-w-screen-xl px-6">{children}</main>
        <Analytics />
      </body>
    </html>
  );
}
