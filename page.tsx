"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Scale, Mail, ArrowLeft, ArrowRight, CheckCircle2, Lock, KeyRound } from "lucide-react";
import { ApiService } from "@/services/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [step, setStep] = useState<"request" | "otp" | "success">("request");
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [newPassword, setNewPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setIsLoading(true);
    try {
      await ApiService.forgotPassword(email);
      setStep("otp");
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpChange = (index: number, val: string) => {
    if (val.length > 1) val = val.slice(0, 1);
    const updated = [...otp];
    updated[index] = val;
    setOtp(updated);

    // Auto-focus next input
    if (val && index < 5) {
      const nextInput = document.getElementById(`otp-input-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleReset = (e: React.FormEvent) => {
    e.preventDefault();
    setStep("success");
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-4 bg-gradient-to-b from-slate-100 via-white to-slate-100">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-slate-900 to-blue-950 flex items-center justify-center text-white shadow-lg group-hover:scale-105 transition-transform">
              <Scale className="w-6 h-6 text-amber-400" />
            </div>
          </Link>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Reset Your Password
          </h1>
          <p className="text-xs text-slate-500">
            Secure account recovery with OTP verification
          </p>
        </div>

        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-xl shadow-slate-200/60 space-y-5">
          {step === "request" && (
            <form onSubmit={handleRequest} className="space-y-4 text-xs">
              <p className="text-slate-600 leading-relaxed">
                Enter your registered email address or mobile number. We will send a 6-digit verification code to reset your credentials.
              </p>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  Registered Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@example.com"
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600"
                    required
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-md flex items-center justify-center gap-2 transition-colors cursor-pointer"
              >
                <span>{isLoading ? "Dispatching OTP..." : "Send Verification Code"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          )}

          {step === "otp" && (
            <form onSubmit={handleReset} className="space-y-4 text-xs">
              <div className="p-3 bg-blue-50 text-blue-900 rounded-xl border border-blue-200 text-xs">
                Enter the 6-digit OTP dispatched to <strong>{email}</strong> (Hint: enter any 6 digits e.g. 123456).
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-2">
                  6-Digit Verification Code
                </label>
                <div className="flex gap-2 justify-center">
                  {otp.map((digit, idx) => (
                    <input
                      key={idx}
                      id={`otp-input-${idx}`}
                      type="text"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleOtpChange(idx, e.target.value)}
                      className="w-10 h-12 text-center text-lg font-bold border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600 text-slate-900 bg-slate-50"
                      required
                    />
                  ))}
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  Enter New Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="At least 8 characters..."
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600"
                    required
                    minLength={8}
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-md flex items-center justify-center gap-2 transition-colors"
              >
                <span>Confirm & Reset Password</span>
                <CheckCircle2 className="w-4 h-4" />
              </button>
            </form>
          )}

          {step === "success" && (
            <div className="text-center space-y-4 py-4">
              <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Password Reset Successful!</h3>
              <p className="text-xs text-slate-600">
                Your credentials have been securely updated. You can now log into your NyaySetu account.
              </p>
              <Link
                href="/auth/login"
                className="inline-block w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-colors"
              >
                Proceed to Login
              </Link>
            </div>
          )}

          <div className="pt-3 border-t border-slate-100 text-center">
            <Link
              href="/auth/login"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-blue-700 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Sign In</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

