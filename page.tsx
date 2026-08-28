"use client";

import { HeroSection } from "@/components/home/HeroSection";
import { RecommendationRow } from "@/components/home/RecommendationRow";
import { FEATURED, TRENDING } from "@/data/content";
import { MOOD_MAP } from "@/data/moods";
import { getRecommendations } from "@/lib/recommendations";
import { useAppStore } from "@/store/useAppStore";
import { useMemo } from "react";

export default function HomePage() {
  const activeMood = useAppStore((s) => s.activeMood);
  const preferences = useAppStore((s) => s.preferences);
  const savedIds = useAppStore((s) => s.savedIds);

  const moodRecs = useMemo(
    () =>
      activeMood
        ? getRecommendations({ mood: activeMood, preferences, savedIds, limit: 8 })
        : [],
    [activeMood, preferences, savedIds]
  );

  const forYou = useMemo(
    () => getRecommendations({ preferences, savedIds, limit: 8 }),
    [preferences, savedIds]
  );

  const featuredScored = useMemo(
    () =>
      FEATURED.map((item) => ({
        ...item,
        score: item.rating * 10,
        matchReason: "Editor's pick",
      })),
    []
  );

  const trendingScored = useMemo(
    () =>
      TRENDING.map((item) => ({
        ...item,
        score: item.rating * 10,
        matchReason: "Trending now",
      })),
    []
  );

  return (
    <>
      <HeroSection />

      {activeMood && moodRecs.length > 0 && (
        <div className="mb-10">
          <RecommendationRow
            title={`${MOOD_MAP[activeMood].emoji} ${MOOD_MAP[activeMood].label} Picks`}
            subtitle="Curated by VibeBox AI based on your mood"
            items={moodRecs}
            showMatchReason
          />
        </div>
      )}

      <div className="space-y-10">
        <RecommendationRow
          title="Made For You"
          subtitle="Personalized recommendations based on your taste"
          items={forYou}
          href="/discover"
          showMatchReason
        />

        <RecommendationRow
          title="Featured"
          subtitle="Hand-picked highlights you'll love"
          items={featuredScored}
        />

        <RecommendationRow
          title="Trending Now"
          subtitle="What everyone's vibing to"
          items={trendingScored}
          href="/discover"
        />
      </div>
    </>
  );
}
