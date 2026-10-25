# OmniRec — AI-Powered Multi-Platform E-Commerce Aggregator & Personalized Recommendation Platform

[![Java Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Python FastAPI](https://img.shields.io/badge/FastAPI-0.110-blue.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-cyan.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**OmniRec** is an enterprise-grade multi-platform e-commerce aggregation and personalized shopping intelligence platform. It creates a unified intelligence layer across major shopping platforms—such as **Amazon, Flipkart, Myntra, and Nykaa**—by deduplicating products, providing multi-seller price comparisons, parsing natural-language shopping queries, and continuously computing personalized product recommendations via an independent Python FastAPI hybrid AI microservice.

---

## 🏛️ System Architecture Diagram

```
                              ┌─────────────────────────────────────────┐
                              │  React 18 + Vite + TypeScript + Tailwind │
                              │    (Frontend Application - Port 5173)   │
                              └────────────────────┬────────────────────┘
                                                   │
                                                   ▼ REST API (JWT Auth)
                              ┌─────────────────────────────────────────┐
                              │    Java + Spring Boot Main Backend      │
                              │           (Port 8080)                   │
                              └────────┬───────────┬────────────┬───────┘
                                       │           │            │
             ┌─────────────────────────┴─┐   ┌─────┴─────┐   ┌──┴────────────────────────┐
             │ MySQL Database            │   │ Redis     │   │ Python FastAPI AI Engine  │
             │ (Transactional / User Auth)│   │ (Cache)   │   │ (Hybrid Recs & NLP Search)│
             └───────────────────────────┘   └───────────┘   └───────────────────────────┘
                                                   │
                                            ┌──────┴────────┐
                                            │ MongoDB       │
                                            │ (Product Catalog)
                                            └───────────────┘
```

---

## ✨ Key Features

1. **Multi-Platform E-Commerce Aggregation**:
   - Unified catalog normalizing products from Amazon, Flipkart, Myntra, and Nykaa.
   - Grouping duplicate product listings across sellers with real-time multi-seller price comparison matrix (price, discount %, stock, delivery speed).

2. **Hybrid AI Recommendation Engine**:
   - Developed in Python FastAPI with `scikit-learn`, `numpy`, and `pandas`.
   - Combines **Content-Based TF-IDF Similarity**, **Category & Brand Affinity**, **Budget Sensitivity Quantiles**, and **Recency/Discount Factor Boosts**.
   - Natural Language Human-Readable Reasoning for every recommendation (e.g. *"Recommended because you frequently view running shoes and usually shop below ₹3,000"*).
   - Cold-start initializer for new users to prevent empty state.
   - Built-in resilience: Spring Boot automatically executes an internal rule-based fallback algorithm if the Python AI service is offline.

3. **Natural-Language Shopping Queries (NLP Search)**:
   - Global search input supports conversational queries like:
     - *"Find running shoes under ₹3,000"*
     - *"Show me college outfits under ₹5,000"*
     - *"Best skincare products under ₹1,500"*
     - *"I need a laptop for programming under ₹70,000"*
   - Converts raw strings into structured JSON query filters (Category, Max Price, Brand, Intent Tags).

4. **OAuth Sandbox & Connected Stores Management**:
   - Interactive store consent manager for Amazon, Flipkart, Myntra, and Nykaa.
   - **Zero Password Storage Guarantee**: OmniRec uses sandbox mock connectors (`MockAmazonConnector`, `MockFlipkartConnector`, etc.) and never asks for or stores third-party passwords, OTPs, session tokens, or payment credentials.

5. **Universal Wishlist & Product Comparison**:
   - Unified wishlist across stores with price drop tracking.
   - Multi-product side-by-side spec comparison table.

6. **Activity & Data-Grounded AI Insights**:
   - Visual category distribution & brand affinity progress charts based strictly on user interaction signals.

7. **Admin Metrics Dashboard (`ROLE_ADMIN`)**:
   - Real-time platform metrics: total users, active users, catalog scale, recommendation CTR %, API response times, and store connector health checks.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Framer Motion |
| **Main Backend** | Java 17/24, Spring Boot 3.2, Spring Security, Spring Data JPA |
| **AI Microservice**| Python 3.12, FastAPI, Uvicorn, Scikit-Learn, NumPy, Pandas, Pydantic |
| **Databases** | MySQL 8.0 (Relational / H2 In-Memory), MongoDB 6.0 (Catalog), Redis 7.0 (Caching) |
| **Security & Auth**| JWT (JSON Web Tokens), BCrypt Password Encoder, OAuth2 Sandbox Architecture |
| **Infrastructure** | Docker, Docker Compose, Nginx |

---

## 🚀 Quick Start Guide

### Option 1: Native Standalone Execution (Fastest Local Test)

Run the Python AI Microservice and React Frontend natively using the provided startup script:

```bash
# 1. Clone & Enter Project Directory
git clone https://github.com/your-username/OmniRec.git
cd OmniRec

# 2. Start Services
./start.sh
```

- **Frontend App**: `http://localhost:5173`
- **Python AI API Docs**: `http://localhost:8000/docs`
- **Spring Boot Swagger Docs**: `http://localhost:8080/swagger-ui.html`

---

### Option 2: Docker Compose Orchestration

To run the complete stack including MySQL, MongoDB, Redis, Python AI Service, Spring Boot, and React via Nginx:

```bash
docker-compose up --build
```

---

## 🧪 Automated Testing

### 1. Python AI Service Tests (Pytest)
```bash
python3 -m pytest ai-service/test_recommendation.py
```

### 2. Spring Boot Backend Tests (JUnit 5 / MockMvc)
```bash
cd backend
./mvnw test
```

### 3. React Frontend Build & Typecheck (Vite / TSC)
```bash
cd frontend
npm run build
```

---

## 🔒 Privacy & Compliance Architecture

OmniRec enforces strict data privacy standards:
- **No Third-Party Passwords**: Users authenticate directly with OmniRec.
- **Data Export & Revocation**: Users can export their preference data in JSON format or disconnect store permissions instantly from the Settings screen.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
