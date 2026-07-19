# ⬡ STRATOS — Premium Weather Intelligence Dashboard

A production-grade, industry-level weather application built with pure HTML, CSS and Vanilla JS ES Modules.

---

## 🚀 Quick Start

### 1. Get your free API key
Sign up at [openweathermap.org/api](https://openweathermap.org/api) — the free tier covers all features used.

### 2. Add your API key
Open `modules/weatherAPI.js` and replace:
```js
const API_KEY = 'YOUR_API_KEY';
```
Also update the two `'YOUR_API_KEY'` references in `script.js` (map calls).

### 3. Serve locally
```bash
# Option A — Python (built-in)
python3 -m http.server 3000

# Option B — Node (npx)
npx serve .

# Option C — VS Code Live Server extension
# Right-click index.html → Open with Live Server
```

> ⚠️ **Must be served over HTTP/HTTPS** (not file://) because ES Modules and Service Workers require a server origin.

---

## 📁 Project Architecture

```
weather-app/
├── index.html           ← App shell, semantic HTML, PWA meta tags
├── style.css            ← Full design system (tokens, components, themes, responsive)
├── script.js            ← App orchestrator / entry point
├── sw.js                ← Service Worker for offline PWA support
├── manifest.json        ← PWA web app manifest
│
├── modules/
│   ├── weatherAPI.js    ← OpenWeatherMap API, in-memory cache, data normalisation
│   ├── uiManager.js     ← All DOM rendering, Canvas icon drawing, toast, skeleton
│   └── storage.js       ← LocalStorage: history, favourites, preferences
│
└── assets/
    └── icons/           ← PWA icons (add icon-192.png + icon-512.png)
```

---

## 🌟 Feature Breakdown

### Core Weather Data
| Feature | Implementation |
|---|---|
| Current temperature | OWM `/weather` endpoint |
| Feels like, H/L | OWM `main` object |
| Condition + description | OWM `weather[0]` |
| Humidity, Pressure | OWM `main` |
| Wind speed + direction | OWM `wind`, converted m/s→km/h |
| Visibility | OWM `visibility` (m→km) |
| UV Index | Estimated from clouds, latitude, time |
| Air Quality Index | OWM `/air_pollution` endpoint |

### Forecast
- **7-day forecast** — OWM `/forecast` (3-hourly, grouped by day)
- **Hourly forecast** — next 8×3hr slots with rain probability
- **Precipitation chart** — Chart.js bar chart
- **24h temperature chart** — Chart.js line chart with gradient fill
- **Sunrise / Sunset** — Computed from OWM unix timestamps + timezone offset

### UI & UX
- **Dynamic weather themes** — 7 gradient backgrounds (sunny, rain, snow, storm, cloudy, night, clear)
- **Dark / Light mode** — CSS custom properties; persisted to localStorage
- **Glassmorphism cards** — `backdrop-filter: blur()` with layered backgrounds
- **Animated canvas icons** — Pure Canvas 2D drawing per condition
- **Skeleton loading** — shimmer placeholders while fetching
- **Toast notifications** — Error, success, info with auto-dismiss
- **Responsive design** — Mobile-first, works 320px to 4K

### Smart Features
- **Auto geolocation** — `navigator.geolocation` on first load
- **Voice search** — Web Speech API (`SpeechRecognition`)
- **Search suggestions** — OWM Geocoding API with 280ms debounce
- **Recent history** — Last 10 searches, removable chips
- **Favourite cities** — Star any city, persisted, quick-load cards
- **Temperature unit toggle** — °C / °F, auto-refetches with new units
- **Auto refresh** — Every 10 minutes if page is visible
- **Offline support** — Service Worker caches assets; shows last saved weather
- **In-memory API cache** — 10-minute TTL to avoid redundant requests

### Advanced
- **Weather map** — Embedded OpenWeatherMap map with layer switching (temp, precipitation, clouds, wind)
- **Weather alerts** — Renders active alerts from OWM One Call API with colour-coded cards
- **PWA** — Installable app (`manifest.json` + Service Worker)
- **Accessibility** — ARIA labels, roles, `aria-live` regions, focus rings
- **SEO basics** — Semantic HTML, meta description, manifest

---

## 🎨 Design System

### CSS Custom Properties
```css
--font-display  /* Syne — headings, temperatures */
--font-body     /* DM Sans — body copy */
--accent        /* Brand blue — interactive elements */
--glass-bg      /* Glassmorphism card background */
--t-spring      /* Spring animation timing */
```

### Weather Themes (data-weather attribute)
```
sunny  → warm gold gradient
rain   → dark blue gradient
storm  → near-black purple
snow   → cool navy gradient
cloudy → slate gradient
night  → deep purple gradient
clear  → default dark gradient
```

### Responsive Breakpoints
- `< 600px`  — Mobile: 2-column stats, compact hero, full-width toast
- `< 900px`  — Tablet: stacked charts, drawer sidebar, hidden clock
- `≥ 900px`  — Desktop: hover-expanded sidebar, side-by-side charts

---

## 🌐 API Integration

### Endpoints Used
```
GET /data/2.5/weather        ← Current conditions
GET /data/2.5/forecast       ← 5-day / 3-hourly forecast (40 slots)
GET /data/2.5/air_pollution  ← AQI data
GET /geo/1.0/direct          ← City search suggestions
```

### Rate Limits (Free Tier)
- 60 calls/minute
- 1,000,000 calls/month
- App uses in-memory caching to stay well within limits

---

## 📦 Deployment

### Netlify (recommended, free)
```bash
# Drag & drop the weather-app/ folder to netlify.com/drop
# Or install CLI:
npm install -g netlify-cli
netlify deploy --dir=. --prod
```

### Vercel
```bash
npx vercel --name stratos-weather
```

### GitHub Pages
1. Push to a GitHub repo
2. Settings → Pages → Deploy from branch (main/root)

### Cloudflare Pages
1. Connect GitHub repo
2. Build command: (none — static)
3. Output directory: `/`

> **Important for production:** Never expose your API key in client-side code for commercial apps. For production use, proxy requests through a serverless function (Netlify Functions, Vercel Edge Functions, Cloudflare Workers).

---

## ⚙️ Configuration Reference

| File | Variable | Description |
|---|---|---|
| `weatherAPI.js` | `API_KEY` | Your OWM API key |
| `weatherAPI.js` | `CACHE_TTL` | API cache duration (ms) |
| `script.js` | `REFRESH_MS` | Auto-refresh interval (ms) |

---

## 🛠 Extending the App

### Add a new weather provider
Replace functions in `modules/weatherAPI.js` — the rest of the app consumes the normalised data shape.

### Add a new stat card
1. Add HTML in `index.html` stats grid
2. Populate in `renderStats()` in `uiManager.js`
3. Style in `style.css`

### Customise themes
Edit the `[data-weather]` CSS rules in `style.css` to change gradient colours per condition.

---

## 📄 License
MIT — free for personal and commercial use.
