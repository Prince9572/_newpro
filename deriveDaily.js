/**
 * OpenWeatherMap's free tier only gives 5-day / 3-hour data, not a
 * true daily endpoint. This groups that list by calendar day (in the
 * location's own timezone) and picks a representative icon from
 * around midday, plus the day's min/max.
 */
export function deriveDaily(list, timezoneOffsetSec) {
  const days = new Map();

  list.forEach((item) => {
    const localMs = item.dt * 1000 + timezoneOffsetSec * 1000;
    const localDate = new Date(localMs);
    const key = localDate.toISOString().slice(0, 10);
    const hour = localDate.getUTCHours();

    if (!days.has(key)) {
      days.set(key, { key, dt: item.dt, min: item.main.temp, max: item.main.temp, midday: item });
    }
    const day = days.get(key);
    day.min = Math.min(day.min, item.main.temp_min);
    day.max = Math.max(day.max, item.main.temp_max);

    // Prefer the entry closest to noon as the "representative" icon
    const currentDist = Math.abs(hour - 12);
    const bestHour = new Date(day.midday.dt * 1000 + timezoneOffsetSec * 1000).getUTCHours();
    const bestDist = Math.abs(bestHour - 12);
    if (currentDist < bestDist) {
      day.midday = item;
    }
  });

  return Array.from(days.values()).slice(0, 5);
}
