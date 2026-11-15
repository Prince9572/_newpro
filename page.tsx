"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { DisclaimerBanner } from "@/components/layout/DisclaimerBanner";
import { LEGAL_CATEGORIES } from "@/mock/mockCategories";
import { MOCK_LAWYERS } from "@/mock/mockLawyers";
import { LawyerCard } from "@/components/lawyers/LawyerCard";
import { useChat } from "@/context/ChatContext";
import {
  Scale,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Languages,
  BookOpen,
  Search,
  MessageSquare,
  Users,
  CheckCircle2,
  FileText,
  PhoneCall,
  Lock,
} from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const { createNewChat } = useChat();
  const [quickQuery, setQuickQuery] = useState("");

  const handleQuickSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickQuery.trim()) return;
    createNewChat(quickQuery.trim());
    router.push("/chat");
  };

  const samplePrompts = [
    "RERA builder delay refund and interest rights",
    "Filing cyber fraud UPI complaint within 1930 golden hour",
    "Mutual consent divorce procedure under Hindu Marriage Act",
    "Cheque bounce Section 138 30-day notice timeline",
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <Navbar />

      <main className="flex-1">
        {/* Top Disclaimer Bar */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-3">
          <DisclaimerBanner compact />
        </div>

        {/* Hero Section */}
        <section className="relative overflow-hidden py-12 sm:py-20 lg:py-24 bg-gradient-to-b from-white via-slate-50/50 to-slate-100 border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
            {/* Pill */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 text-blue-800 border border-blue-200 text-xs font-semibold mb-6 shadow-2xs">
              <Sparkles className="w-4 h-4 text-amber-500" />
              <span>AI-Assisted Legal Suggestion System for Indian Jurisprudence</span>
            </div>

            {/* Title */}
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-slate-950 tracking-tight leading-tight max-w-4xl mx-auto">
              Demystifying Indian Law with{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-700 via-blue-900 to-indigo-900">
                Intelligent AI Suggestions
              </span>
            </h1>

            {/* Subtitle */}
            <p className="mt-5 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
              Navigate the Bharatiya Nyaya Sanhita (BNS), CPC, RERA, and consumer regulations with clarity. Get instant actionable steps, required evidence checklists, and connect with verified advocates.
            </p>

            {/* Quick Interactive Prompt Search Box */}
            <div className="mt-8 max-w-2xl mx-auto">
              <form
                onSubmit={handleQuickSubmit}
                className="bg-white p-2 rounded-2xl border-2 border-slate-200 hover:border-blue-500 shadow-xl shadow-slate-200/50 flex flex-col sm:flex-row items-center gap-2 transition-all"
              >
                <div className="flex items-center gap-2.5 flex-1 w-full pl-3">
                  <Search className="w-5 h-5 text-slate-400 shrink-0" />
                  <input
                    type="text"
                    value={quickQuery}
                    onChange={(e) => setQuickQuery(e.target.value)}
                    placeholder="Ask any legal issue (e.g. 'Builder refusing flat handover')..."
                    className="w-full text-sm text-slate-800 placeholder-slate-400 focus:outline-none py-2"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full sm:w-auto px-5 py-3 bg-blue-700 hover:bg-blue-800 text-white rounded-xl text-xs font-bold shadow-md flex items-center justify-center gap-2 transition-colors cursor-pointer"
                >
                  <span>Ask NyaySetu AI</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>

              {/* Sample prompt chips */}
              <div className="mt-3 flex flex-wrap items-center justify-center gap-1.5 text-xs">
                <span className="text-slate-400 text-[11px] mr-1">Try asking:</span>
                {samplePrompts.map((p, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      createNewChat(p);
                      router.push("/chat");
                    }}
                    className="text-[11px] text-slate-600 hover:text-blue-700 bg-white hover:bg-blue-50/70 border border-slate-200 rounded-full px-3 py-1 transition-colors cursor-pointer shadow-2xs"
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Trust Badges */}
            <div className="mt-12 pt-8 border-t border-slate-200/80 grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-semibold text-slate-600 max-w-3xl mx-auto">
              <div className="flex items-center justify-center gap-2">
                <BookOpen className="w-4 h-4 text-blue-600" />
                <span>BNS & BNSS 2023 Ready</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <Languages className="w-4 h-4 text-amber-600" />
                <span>Bilingual (English & हिंदी)</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Bar Council Verified Advocates</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <Lock className="w-4 h-4 text-purple-600" />
                <span>DPDP Act 2023 Confidential</span>
              </div>
            </div>
          </div>
        </section>

        {/* 6 Legal Categories Section */}
        <section className="py-16 bg-white border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
              <div>
                <div className="text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
                  Comprehensive Coverage
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                  Indian Legal Assistance Categories
                </h2>
                <p className="text-sm text-slate-500 mt-1 max-w-xl">
                  Deep legal knowledge bases across criminal penal codes, family disputes, real estate RERA, consumer forums, cyber crime, and commercial suits.
                </p>
              </div>
              <Link
                href="/categories"
                className="mt-4 md:mt-0 inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 hover:text-blue-900"
              >
                <span>View All 6 Categories Detailed Guides</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {LEGAL_CATEGORIES.map((cat) => (
                <div
                  key={cat.id}
                  className="bg-slate-50/70 hover:bg-white rounded-2xl border border-slate-200/90 hover:border-blue-400 p-6 shadow-2xs hover:shadow-lg transition-all flex flex-col justify-between group"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
                        <Scale className="w-5 h-5" />
                      </div>
                      <span className="text-xs font-medium text-slate-400">{cat.nameHindi}</span>
                    </div>

                    <h3 className="text-lg font-bold text-slate-900 group-hover:text-blue-700 transition-colors mb-2">
                      {cat.name}
                    </h3>
                    <p className="text-xs text-slate-600 leading-relaxed mb-4">
                      {cat.shortDescription}
                    </p>

                    {/* Primary Acts */}
                    <div className="space-y-1 mb-4">
                      <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                        Key Governing Acts:
                      </div>
                      <div className="text-xs text-slate-700 font-medium">
                        {cat.primaryActs.slice(0, 2).join(" • ")}
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-200/80 flex items-center justify-between text-xs">
                    <Link
                      href={`/categories/${cat.slug}`}
                      className="font-semibold text-slate-700 hover:text-blue-700 flex items-center gap-1"
                    >
                      <span>Explore Laws & FAQs</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                    <button
                      onClick={() => {
                        createNewChat(`Tell me about legal remedies in ${cat.name} in India`);
                        router.push("/chat");
                      }}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Ask AI
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-16 bg-slate-900 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <span className="text-xs font-bold text-blue-400 uppercase tracking-wider">
                Transparent Process
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
                How NyaySetu Protects & Empowers You
              </h2>
              <p className="text-sm text-slate-400 mt-2">
                A structured, step-by-step workflow designed to take you from legal confusion to courtroom readiness.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Step 1 */}
              <div className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700/80 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-base">
                  1
                </div>
                <h3 className="font-bold text-base text-white">Describe Your Legal Situation</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Type or dictate your legal query in English, Hindi, or Hinglish. Attach notices, contracts, or bank transaction receipts for thorough AI review.
                </p>
                <div className="text-xs text-blue-400 font-medium flex items-center gap-1.5 pt-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Confidential & DPDP Compliant</span>
                </div>
              </div>

              {/* Step 2 */}
              <div className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700/80 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-base">
                  2
                </div>
                <h3 className="font-bold text-base text-white">Statutory Analysis & Action Plan</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  NyaySetu AI analyzes applicable sections under Bharatiya Nyaya Sanhita, CPC, CrPC, RERA, and delivers numbered procedural steps and required documents.
                </p>
                <div className="text-xs text-amber-400 font-medium flex items-center gap-1.5 pt-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Cites Official Indian Statutes & Precedents</span>
                </div>
              </div>

              {/* Step 3 */}
              <div className="bg-slate-800/80 rounded-2xl p-6 border border-slate-700/80 space-y-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-base">
                  3
                </div>
                <h3 className="font-bold text-base text-white">Engage Bar Council Advocates</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Need formal representation in High Court or District Court? Book pre-screened advocates with verified Bar registration numbers and transparent fees.
                </p>
                <div className="text-xs text-emerald-400 font-medium flex items-center gap-1.5 pt-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Transparent Schedule & Chamber Booking</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Verified Advocates Preview */}
        <section className="py-16 bg-slate-50 border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
              <div>
                <div className="text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
                  Verified Legal Representation
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                  Featured Bar Council Enrolled Advocates
                </h2>
                <p className="text-sm text-slate-500 mt-1 max-w-xl">
                  Consult high-caliber advocates practicing across the Supreme Court of India, High Courts, and Special Commercial Tribunals.
                </p>
              </div>
              <Link
                href="/lawyers"
                className="mt-4 md:mt-0 inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 hover:text-blue-900"
              >
                <span>Search All Advocates</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {MOCK_LAWYERS.slice(0, 3).map((lawyer) => (
                <LawyerCard key={lawyer.id} lawyer={lawyer} />
              ))}
            </div>
          </div>
        </section>

        {/* National Helplines & Emergency CTA */}
        <section className="py-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-gradient-to-r from-amber-500 via-orange-600 to-amber-600 text-white rounded-3xl p-8 sm:p-10 shadow-xl flex flex-col lg:flex-row lg:items-center justify-between gap-6">
              <div className="space-y-2 max-w-xl">
                <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider bg-white/20 px-3 py-1 rounded-full w-fit">
                  <PhoneCall className="w-3.5 h-3.5" />
                  <span>Immediate Emergency Assistance</span>
                </div>
                <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                  Lost funds to cyber fraud or need emergency legal aid?
                </h3>
                <p className="text-amber-100 text-sm leading-relaxed">
                  Call <strong>1930</strong> immediately to freeze cyber transactions within the golden hour, or call <strong>15100</strong> for government legal aid via NALSA.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <Link
                  href="/chat"
                  className="px-6 py-3 bg-slate-950 hover:bg-slate-900 text-white rounded-xl text-xs font-bold text-center shadow-lg transition-colors"
                >
                  Launch NyaySetu Assistant
                </Link>
                <Link
                  href="/help"
                  className="px-6 py-3 bg-white text-slate-900 hover:bg-amber-50 rounded-xl text-xs font-bold text-center shadow-lg transition-colors"
                >
                  All Helplines & Guides
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
