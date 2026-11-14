# NyaySetu (न्यायसेतु) – AI-Assisted Legal Suggestion System

> Empowering Indian citizens, law students, and legal professionals with intelligent legal suggestions, statutory awareness (Bharatiya Nyaya Sanhita, CPC, BNSS, RERA, CPA 2019), and verified advocate discovery.

---

## 🏛️ Overview

**NyaySetu** is an Indian legal assistant platform inspired by ChatGPT. Built with a clean white and navy design system, it delivers bilingual (English & Hindi) legal guidance, procedural roadmaps, evidentiary document checklists, and connects citizens with Bar Council-verified advocates.

---

## 🚀 Tech Stack

- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS v4 (Clean White & Deep Navy palette)
- **Icons:** Lucide React
- **State Management:** React Context API with LocalStorage persistence (`AuthContext`, `ChatContext`)
- **Backend Readiness:** Modular API Client (`src/services/api.ts`) ready for immediate FastAPI integration via `NEXT_PUBLIC_FASTAPI_URL`

---

## 🌟 Core Features & Modules

### 1. 💬 ChatGPT-Style Legal Workspace (`/chat` & `/chat/[id]`)
- **Collapsible Sidebar:** Collapse and expand toggle with desktop and mobile drawer support.
- **New Consultation:** Instant new chat creation with auto-naming based on the legal issue.
- **Chat History & Search:** Search conversations in real-time, grouped by pinned and recent inquiries.
- **Rename & Delete Dialogs:** Custom accessible modals to rename or delete chats with confirmation.
- **Structured Legal Responses:**
  - Executive Legal Summary
  - Applicable Indian Statutes & Sections (BNS 2023, BNSS 2023, CPC, RERA, CPA 2019, IT Act)
  - Numbered immediate procedural next steps
  - Evidentiary checklist of required documents
  - **Bilingual Switcher:** Instant toggle between English and Hindi ('हिंदी सारांश')
  - One-click copy advice & export text summary
  - Thumbs up/down feedback
  - Direct "Find Relevant Advocates" button
- **Legal Input Bar:**
  - Expanding textarea with Enter to send (Shift+Enter for newline)
  - File attachment for legal documents (FIRs, Notices, Contracts, Agreements)
  - Voice dictation simulation
  - Language selection (English, Hindi, Hinglish)
  - Dynamic multi-step thinking indicator ("Reviewing against Indian Statutory Framework...")
- **Suggested Legal Prompts:** One-click chips across all 6 legal categories.

### 2. ⚖️ 6 Comprehensive Legal Categories (`/categories` & `/categories/[slug]`)
1. **Criminal Law:** Bharatiya Nyaya Sanhita (BNS 2023), BNSS 2023, BSA 2023, Section 138 NI Act, Bails.
2. **Family Law:** Hindu Marriage Act 1955, Special Marriage Act, Mutual Consent Divorce, Maintenance, Domestic Violence (PWDVA).
3. **Property Law:** RERA Act 2016, Transfer of Property Act 1882, Builder delay interest (SBI MCLR + 2%), Tenant eviction.
4. **Consumer Rights:** Consumer Protection Act 2019, e-Daakhil filing, E-Commerce Rules 2020, Defective products.
5. **Cyber Crime:** Information Technology Act 2000 (Sec 66C/66D), Golden Hour reporting via 1930, RBI Zero Liability rules.
6. **Civil Law:** Code of Civil Procedure (CPC 1908), Summary Suits (Order 37), Indian Contract Act 1872, Specific Relief.

### 3. 🧑‍⚖️ Advocate Discovery & Booking (`/lawyers` & `/lawyers/[id]`)
- **Search & Filters:** Filter by Specialization, City (New Delhi, Mumbai, Bengaluru, etc.), Verified status, Rating, Experience, and Consultation Fee.
- **Advocate Profiles:** Bar Council registration numbers, enrollment year, court practice (Supreme Court, High Courts, District Courts), biography, and verified client reviews.
- **Consultation Booking Modal:** Interactive booking with date picker, time slot selector, consultation mode (Online Video, Phone Call, Chamber Visit), and issue summary.

### 4. 📊 3 Tailored Dashboards
- **Citizen / Client Dashboard (`/dashboard`):** Active case files, statutory limitation periods, hearing schedules, quick category jumps.
- **Advocate Dashboard (`/dashboard/lawyer`):** Incoming citizen consultation briefs, accept/decline leads, chamber schedule, earnings tracker.
- **Admin Dashboard (`/dashboard/admin`):** DPDP Act compliance metrics, Indian statutory vector index sync (511 BNS sections), security audit logs.

### 5. 🔐 Authentication & Onboarding (`/auth/*`)
- **Login (`/auth/login`):** Multi-role login with **one-click demo persona buttons** for instant testing as Citizen, Advocate, or Admin.
- **Register (`/auth/register`):** Multi-role registration with Bar Council registration number verification for advocates.
- **Forgot Password (`/auth/forgot-password`):** 6-digit OTP verification and password reset flow.

### 6. 🛡️ Statutory Compliance & Safety
- **Bar Council of India (BCI) Disclaimer:** Prominent banners ensuring compliance with BCI Rule 36.
- **DPDP Act 2023 Privacy Policy (`/privacy`):** Attorney-client privilege safeguards under Bharatiya Sakshya Adhiniyam (BSA), user data export (JSON), and right to erasure.
- **Emergency Helplines (`/help`):** Direct access to official 24x7 Government of India helplines:
  - **1930:** National Cyber Crime Helpline (Golden Hour freeze)
  - **15100:** NALSA Free Legal Aid Tele-Law
  - **1915:** National Consumer Grievance
  - **1091 / 181:** Women in Distress Emergency Helpline

---

## 🛠️ Running the Application

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build production bundle
npm run build
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔌 FastAPI Integration Guide

To connect a live FastAPI backend:
1. Create a `.env.local` file in the project root:
   ```env
   NEXT_PUBLIC_FASTAPI_URL="http://localhost:8000/api/v1"
   ```
2. The frontend will automatically route requests through `src/services/api.ts` to your FastAPI endpoints. When omitted, it runs seamlessly in mock mode.
