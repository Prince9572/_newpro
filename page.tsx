"use client";

import { ContentCard } from "@/components/ui/ContentCard";
import { MoodSelector } from "@/components/ui/MoodSelector";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { GENRES } from "@/data/content";
import { MOODS } from "@/data/moods";
import { getMoodRecommendations, getRecommendations } from "@/lib/recommendations";
import { cn } from "@/lib/utils";
import { useAppStore } from "@/store/useAppStore";
import { motion } from "framer-motion";
import { useMemo, useState } from "react";

export default function DiscoverPage() {
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);
  const activeMood = useAppStore((s) => s.activeMood);
  const preferences = useAppStore((s) => s.preferences);
  const savedIds = useAppStore((s) => s.savedIds);

  const filteredRecs = useMemo(() => {
    let recs = activeMood
      ? getMoodRecommendations(activeMood, preferences, 16)
      : getRecommendations({ preferences, savedIds, limit: 16 });

    if (selectedGenre) {
      recs = recs.filter((r) => r.genres.includes(selectedGenre));
    }
    return recs;
  }, [activeMood, preferences, savedIds, selectedGenre]);

  return (
    <>
      <header className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">Discover</h1>
        <p className="text-muted text-base md:text-lg max-w-2xl">
          Explore by mood and genre. Every pick is scored by our AI to match what you&apos;re feeling.
        </p>
      </header>

      <section className="mb-10" aria-labelledby="mood-explore-heading">
        <SectionHeader
          title="Explore by Mood"
          subtitle="Tap a mood to see tailored recommendations"
        />
        <MoodSelector />
      </section>

      <section className="mb-10" aria-labelledby="genre-filter-heading">
        <SectionHeader title="Filter by Genre" />
        <div className="flex flex-wrap gap-2" role="group" aria-label="Genre filters">
          <button
            onClick={() => setSelectedGenre(null)}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
              !selectedGenre
                ? "bg-[var(--accent)] text-white border-transparent"
                : "border-[var(--border)] text-muted hover:text-foreground hover:border-white/20"
            )}
            aria-pressed={!selectedGenre}
          >
            All
          </button>
          {GENRES.map((genre) => (
            <button
              key={genre}
              onClick={() => setSelectedGenre(selectedGenre === genre ? null : genre)}
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
                selectedGenre === genre
                  ? "bg-[var(--accent)] text-white border-transparent"
                  : "border-[var(--border)] text-muted hover:text-foreground hover:border-white/20"
              )}
              aria-pressed={selectedGenre === genre}
            >
              {genre}
            </button>
          ))}
        </div>
      </section>

      <section className="mb-12" aria-labelledby="mood-cards-heading">
        <SectionHeader title="All Moods" subtitle="Quick browse by emotional vibe" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {MOODS.map((mood, i) => (
            <motion.button
              key={mood.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              onClick={() =>
                useAppStore.getState().setActiveMood(
                  activeMood === mood.id ? null : mood.id
                )
              }
              className={cn(
                "relative overflow-hidden rounded-2xl p-5 text-left transition-transform duration-200 hover:scale-[1.02] active:scale-[0.98]",
                "bg-gradient-to-br",
                mood.gradient,
                activeMood === mood.id && "ring-2 ring-white ring-offset-2 ring-offset-background"
              )}
            >
              <span className="text-3xl mb-2 block" aria-hidden>{mood.emoji}</span>
              <span className="font-semibold text-white block">{mood.label}</span>
              <span className="text-xs text-white/70 mt-1 block line-clamp-2">
                {mood.description}
              </span>
            </motion.button>
          ))}
        </div>
      </section>

      <section aria-labelledby="discover-results-heading">
        <SectionHeader
          title={activeMood ? `${MOODS.find((m) => m.id === activeMood)?.label} Recommendations` : "Top Picks"}
          subtitle={`${filteredRecs.length} results${selectedGenre ? ` in ${selectedGenre}` : ""}`}
        />
        {filteredRecs.length > 0 ? (
          <div className="content-grid">
            {filteredRecs.map((item, i) => (
              <ContentCard
                key={item.id}
                item={item}
                matchReason={item.matchReason}
                showMatchReason
                index={i}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <p className="text-muted">No results for this combination. Try a different mood or genre.</p>
          </div>
        )}
      </section>
    </>
  );
}
