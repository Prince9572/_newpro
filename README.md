# VibeBox

A premium AI-powered entertainment assistant with mood-based recommendations. Built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Mood-based AI recommendations** — Select from 8 moods to get personalized content picks
- **Multi-format content** — Music, movies, series, and podcasts in one place
- **Personal library** — Save favorites with persistent storage
- **Smart search** — Find content by title, artist, or genre
- **Full customization** — Accent colors, display density, genre preferences, playback settings
- **Premium UI** — Dark theme inspired by Spotify, Netflix, and Apple Music
- **Accessible** — Skip links, ARIA labels, keyboard navigation, focus states

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Pages

| Page | Purpose |
|------|---------|
| **Home** | Personalized dashboard with mood selector and recommendations |
| **Discover** | Browse by mood and genre with AI-scored results |
| **Search** | Full-text search with trending and quick filters |
| **Library** | Your saved content organized by type |
| **Profile** | Theme, playback, and genre preferences |

## Tech Stack

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS 4
- Framer Motion
- Zustand (persistent state)
- Lucide React (icons)

## Project Structure

```
src/
├── app/           # Pages and layouts
├── components/    # UI, layout, and feature components
├── data/          # Content catalog and mood definitions
├── lib/           # Types, utils, recommendation engine
└── store/         # Global state (preferences, library, player)
```

## Scripts

- `npm run dev` — Start development server
- `npm run build` — Production build
- `npm run start` — Start production server
- `npm run lint` — Run ESLint
