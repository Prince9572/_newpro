"use client";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { GENRES } from "@/data/content";
import { cn } from "@/lib/utils";
import { ACCENT_COLORS, useAppStore } from "@/store/useAppStore";
import { Check, Palette, RotateCcw, Settings2, Sliders, User } from "lucide-react";

const ACCENT_OPTIONS = Object.keys(ACCENT_COLORS) as Array<keyof typeof ACCENT_COLORS>;

export default function ProfilePage() {
  const { preferences, updatePreferences } = useAppStore();

  const toggleGenre = (genre: string) => {
    const current = preferences.favoriteGenres;
    updatePreferences({
      favoriteGenres: current.includes(genre)
        ? current.filter((g) => g !== genre)
        : [...current, genre],
    });
  };

  const resetPreferences = () => {
    updatePreferences({
      accentColor: "violet",
      density: "comfortable",
      autoplay: true,
      explicitContent: true,
      favoriteGenres: ["Electronic", "Indie"],
    });
  };

  return (
    <>
      <header className="mb-8">
        <div className="flex items-center gap-4 mb-4">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center">
            <User className="h-8 w-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight">Profile</h1>
            <p className="text-muted">Customize your VibeBox experience</p>
          </div>
        </div>
      </header>

      <div className="grid gap-6 max-w-2xl">
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-5">
            <Palette className="h-5 w-5 text-[var(--accent)]" />
            <div>
              <h2 className="font-semibold">Accent Color</h2>
              <p className="text-sm text-muted">Personalize the interface theme</p>
            </div>
          </div>
          <div className="flex gap-3" role="radiogroup" aria-label="Accent color">
            {ACCENT_OPTIONS.map((color) => (
              <button
                key={color}
                onClick={() => updatePreferences({ accentColor: color })}
                className={cn(
                  "h-10 w-10 rounded-full transition-all duration-200",
                  ACCENT_COLORS[color].primary,
                  preferences.accentColor === color
                    ? "ring-2 ring-white ring-offset-2 ring-offset-surface scale-110"
                    : "hover:scale-105 opacity-70 hover:opacity-100"
                )}
                aria-label={color}
                aria-checked={preferences.accentColor === color}
                role="radio"
              />
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-5">
            <Sliders className="h-5 w-5 text-[var(--accent)]" />
            <div>
              <h2 className="font-semibold">Display Density</h2>
              <p className="text-sm text-muted">Adjust content spacing</p>
            </div>
          </div>
          <div className="flex gap-2" role="radiogroup" aria-label="Display density">
            {(["comfortable", "compact"] as const).map((density) => (
              <button
                key={density}
                onClick={() => updatePreferences({ density })}
                className={cn(
                  "flex-1 py-3 px-4 rounded-xl text-sm font-medium border transition-all duration-200 capitalize",
                  preferences.density === density
                    ? "bg-[var(--accent)]/20 border-[var(--accent)] text-[var(--accent)]"
                    : "border-[var(--border)] text-muted hover:border-white/20"
                )}
                aria-checked={preferences.density === density}
                role="radio"
              >
                {density}
              </button>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-5">
            <Settings2 className="h-5 w-5 text-[var(--accent)]" />
            <div>
              <h2 className="font-semibold">Playback</h2>
              <p className="text-sm text-muted">Control how content plays</p>
            </div>
          </div>
          <div className="space-y-4">
            <label className="flex items-center justify-between cursor-pointer group">
              <div>
                <p className="text-sm font-medium">Autoplay</p>
                <p className="text-xs text-muted">Continue playing similar content</p>
              </div>
              <button
                role="switch"
                aria-checked={preferences.autoplay}
                onClick={() => updatePreferences({ autoplay: !preferences.autoplay })}
                className={cn(
                  "relative h-6 w-11 rounded-full transition-colors duration-200",
                  preferences.autoplay ? "bg-[var(--accent)]" : "bg-surface-elevated"
                )}
              >
                <span
                  className={cn(
                    "absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform duration-200",
                    preferences.autoplay ? "translate-x-5" : "translate-x-0.5"
                  )}
                />
              </button>
            </label>

            <label className="flex items-center justify-between cursor-pointer group">
              <div>
                <p className="text-sm font-medium">Explicit Content</p>
                <p className="text-xs text-muted">Include explicit-rated content</p>
              </div>
              <button
                role="switch"
                aria-checked={preferences.explicitContent}
                onClick={() =>
                  updatePreferences({ explicitContent: !preferences.explicitContent })
                }
                className={cn(
                  "relative h-6 w-11 rounded-full transition-colors duration-200",
                  preferences.explicitContent ? "bg-[var(--accent)]" : "bg-surface-elevated"
                )}
              >
                <span
                  className={cn(
                    "absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform duration-200",
                    preferences.explicitContent ? "translate-x-5" : "translate-x-0.5"
                  )}
                />
              </button>
            </label>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-5">
            <Check className="h-5 w-5 text-[var(--accent)]" />
            <div>
              <h2 className="font-semibold">Favorite Genres</h2>
              <p className="text-sm text-muted">Improve your recommendations</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {GENRES.map((genre) => {
              const selected = preferences.favoriteGenres.includes(genre);
              return (
                <button
                  key={genre}
                  onClick={() => toggleGenre(genre)}
                  className={cn(
                    "px-3 py-1.5 rounded-full text-sm border transition-all duration-200",
                    selected
                      ? "bg-[var(--accent)]/20 border-[var(--accent)] text-[var(--accent)]"
                      : "border-[var(--border)] text-muted hover:border-white/20"
                  )}
                  aria-pressed={selected}
                >
                  {genre}
                </button>
              );
            })}
          </div>
          {preferences.favoriteGenres.length > 0 && (
            <p className="text-xs text-muted mt-3">
              {preferences.favoriteGenres.length} genre{preferences.favoriteGenres.length !== 1 && "s"} selected
            </p>
          )}
        </Card>

        <Button
          variant="outline"
          onClick={resetPreferences}
          className="self-start"
        >
          <RotateCcw className="h-4 w-4" />
          Reset to defaults
        </Button>
      </div>
    </>
  );
}
