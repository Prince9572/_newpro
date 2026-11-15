import type { Metadata } from "next";
import { AuthProvider } from "@/context/AuthContext";
import { ChatProvider } from "@/context/ChatContext";
import "./globals.css";

export const metadata: Metadata = {
  title: "NyaySetu | AI-Assisted Legal Suggestion System",
  description:
    "Empowering Indian citizens and legal professionals with intelligent, bilingual legal suggestions, case law insights, and expert lawyer discovery.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col font-sans antialiased bg-slate-50 text-slate-900">
        <AuthProvider>
          <ChatProvider>{children}</ChatProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
