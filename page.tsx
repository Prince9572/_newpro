"use client";

import { ContentCard } from "@/components/ui/ContentCard";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { CONTENT } from "@/data/content";
import { MOODS } from "@/data/moods";
import { searchContent } from "@/lib/recommendations";
import { useAppStore } from "@/store/useAppStore";
import { motion } from "framer-motion";
import { Search, TrendingUp } from "lucide-react";
import { useMemo } from "react";

const QUICK_SEARCHES = ["Electronic", "Jazz", "Sci-Fi", "Podcast", "Indie"];

export default function SearchPage() {
  const searchQuery = useAppStore((s) => s.searchQuery);
  const setSearchQuery = useAppStore((s) => s.setSearchQuery);
  const preferences = useAppStore((s) => s.preferences);
  const setActiveMood = useAppStore((s) => s.setActiveMood);

  const results = useMemo(
    () => (searchQuery ? searchContent(searchQuery, preferences) : []),
    [searchQuery, preferences]
  );

  const trending = useMemo(() => CONTENT.filter((c) => c.trending).slice(0, 6), []);

  return (
    <>
      <header className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-2">Search</h1>
        <p className="text-muted">Find music, movies, series, and podcasts</p>
      </header>

      <div className="mb-8 max-w-2xl">
        <Input
          showSearchIcon
          placeholder="Search titles, artists, genres..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onClear={() => setSearchQuery("")}
          aria-label="Search content"
          autoFocus
        />
      </div>

      {!searchQuery && (
        <>
          <section className="mb-10" aria-labelledby="quick-search-heading">
            <h2 id="quick-search-heading" className="text-sm font-medium text-muted mb-3">
              Popular searches
            </h2>
            <div className="flex flex-wrap gap-2">
              {QUICK_SEARCHES.map((term) => (
                <button
                  key={term}
                  onClick={() => setSearchQuery(term)}
                  className="px-4 py-2 rounded-full text-sm bg-surface-elevated border border-[var(--border)] text-muted hover:text-foreground hover:border-white/20 transition-colors"
                >
                  {term}
                </button>
              ))}
            </div>
          </section>

          <section className="mb-10" aria-labelledby="browse-moods-heading">
            <h2 id="browse-moods-heading" className="text-sm font-medium text-muted mb-3">
              Browse by mood
            </h2>
            <div className="flex flex-wrap gap-2">
              {MOODS.slice(0, 6).map((mood) => (
                <button
                  key={mood.id}
                  onClick={() => setActiveMood(mood.id)}
                  className="flex items-center gap-2 px-4 py-2 rounded-full text-sm bg-surface-elevated border border-[var(--border)] hover:border-white/20 transition-colors"
                >
                  <span aria-hidden>{mood.emoji}</span>
                  {mood.label}
                </button>
              ))}
            </div>
          </section>

          <section aria-labelledby="trending-search-heading">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-[var(--accent)]" />
              <h2 id="trending-search-heading" className="text-xl font-semibold">
                Trending
              </h2>
            </div>
            <div className="content-grid">
              {trending.map((item, i) => (
                <ContentCard key={item.id} item={item} index={i} />
              ))}
            </div>
          </section>
        </>
      )}

      {searchQuery && (
        <section aria-labelledby="search-results-heading">
          <div className="flex items-center gap-3 mb-6">
            <Search className="h-5 w-5 text-muted" aria-hidden />
            <h2 id="search-results-heading" className="text-lg font-semibold">
              Results for &ldquo;{searchQuery}&rdquo;
            </h2>
            <Badge variant="muted">{results.length}</Badge>
          </div>

          {results.length > 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="content-grid"
            >
              {results.map((item, i) => (
                <ContentCard
                  key={item.id}
                  item={item}
                  matchReason={item.matchReason}
                  showMatchReason
                  index={i}
                />
              ))}
            </motion.div>
          ) : (
            <div className="text-center py-16">
              <p className="text-muted mb-2">No results found</p>
              <p className="text-sm text-muted">Try different keywords or browse by mood</p>
            </div>
          )}
        </section>
      )}
    </>
  );
}
