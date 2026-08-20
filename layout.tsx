import { AppShell } from "@/components/layout/AppShell";
import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "VibeBox — AI Entertainment Assistant",
    template: "%s · VibeBox",
  },
  description:
    "Your premium AI-powered entertainment assistant. Discover music, movies, and more tailored to your mood.",
  keywords: ["entertainment", "music", "movies", "AI recommendations", "mood"],
};

export const viewport: Viewport = {
  themeColor: "#09090b",
  colorScheme: "dark",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full bg-background text-foreground">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:rounded-lg focus:bg-[var(--accent)] focus:text-white"
        >
          Skip to main content
        </a>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
