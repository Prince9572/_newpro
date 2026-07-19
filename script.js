/**
 * script.js — STRATOS Weather App entry point
 * Orchestrates all modules; handles all user interactions
 */

import {
  fetchByCoords,
  fetchByCity,
  geocodeSuggestions,
  bustCache,
} from './modules/weatherAPI.js';

import {
  getHistory, pushHistory, removeHistory,
  getFavourites, addFavourite, removeFavourite, isFavourite,
  saveLastWeather, getLastWeather,
  getPrefs, savePrefs,
} from './modules/storage.js';

import {
  applyWeatherTheme,
  renderHero, renderStats, renderHourly,
  renderTempChart, renderForecast,
  updateMap, bindMapLayers,
  renderFavourites, renderHistory,
  renderAlerts, setFavIcon,
  showSkeleton, showToast, dismissToast,
  startClock, switchPanel,
  renderSuggestions, hideSuggestions,
  hideLoader, qs, qsa,
} from './modules/uiManager.js';

// ══════════════════════════════════════════════════
// STATE
// ══════════════════════════════════════════════════
let currentWeather = null;
let prefs          = getPrefs();
let refreshTimer   = null;
const REFRESH_MS   = 10 * 60 * 1000; // auto refresh every 10 min

// ══════════════════════════════════════════════════
// BOOT
// ══════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', async () => {
  // Apply saved prefs immediately (no flash)
  applyPrefs();
  startClock();
  bindStaticEvents();

  // Load last cached weather while we fetch fresh
  const last = getLastWeather();
  if (last) {
    currentWeather = last;
    renderAll(last, true /* fromCache */);
  }

  // Attempt geolocation first, fallback to 'London'
  try {
    await detectLocation();
  } catch {
    await loadCity('London');
  }

  scheduleAutoRefresh();
  hideLoader();
});

// ══════════════════════════════════════════════════
// CORE FETCH + RENDER
// ══════════════════════════════════════════════════
async function loadCity(city) {
  showSkeleton();
  try {
    const data = await fetchByCity(city, prefs.units);
    currentWeather = data;
    saveLastWeather(data);
    pushHistory(data.city);
    renderAll(data);
    updateMap(data.lat, data.lon, 'YOUR_API_KEY', prefs.mapLayer);
  } catch (err) {
    showToast(err.message);
  }
}

async function loadCoords(lat, lon) {
  showSkeleton();
  try {
    const data = await fetchByCoords(lat, lon, prefs.units);
    currentWeather = data;
    saveLastWeather(data);
    pushHistory(data.city);
    renderAll(data);
    updateMap(data.lat, data.lon, 'YOUR_API_KEY', prefs.mapLayer);
  } catch (err) {
    showToast(err.message);
  }
}

function renderAll(data, fromCache = false) {
  applyWeatherTheme(data.condition, data.isNight);
  renderHero(data);
  renderStats(data);
  renderHourly(data);
  renderTempChart(data);
  renderForecast(data);
  renderAlerts(data.alerts || []);
  setFavIcon(isFavourite(data.city));
  renderHistory(getHistory(), loadCity, handleRemoveHistory);
  renderFavourites(getFavourites(), loadCity, handleRemoveFav);
  if (fromCache) showToast('Showing cached data — refreshing…', 'info');
}

// ══════════════════════════════════════════════════
// GEOLOCATION
// ══════════════════════════════════════════════════
function detectLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) { reject(new Error('Geolocation not supported')); return; }
    navigator.geolocation.getCurrentPosition(
      async pos => {
        await loadCoords(pos.coords.latitude, pos.coords.longitude);
        resolve();
      },
      err => reject(err),
      { timeout: 6000, maximumAge: 60000 }
    );
  });
}

// ══════════════════════════════════════════════════
// STATIC EVENT BINDING
// ══════════════════════════════════════════════════
function bindStaticEvents() {
  // ── Search with debounce ──
  const searchInput = qs('#searchInput');
  let debounceTimer, suggestTimer;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    clearTimeout(suggestTimer);
    const val = searchInput.value.trim();
    if (!val) { hideSuggestions(); return; }
    suggestTimer = setTimeout(async () => {
      const suggs = await geocodeSuggestions(val).catch(() => []);
      renderSuggestions(suggs, item => {
        searchInput.value = item.name;
        hideSuggestions();
        loadCoords(item.lat, item.lon);
      });
    }, 280);
  });

  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      clearTimeout(debounceTimer);
      hideSuggestions();
      const val = searchInput.value.trim();
      if (val) loadCity(val);
    }
    if (e.key === 'Escape') { hideSuggestions(); }
  });

  searchInput.addEventListener('blur', () => setTimeout(hideSuggestions, 200));

  // ── Locate button ──
  qs('#locateBtn').addEventListener('click', async () => {
    try { await detectLocation(); }
    catch { showToast('Could not access your location'); }
  });

  // ── Voice search ──
  const voiceBtn = qs('#voiceBtn');
  voiceBtn.addEventListener('click', startVoiceSearch);

  // ── Refresh button ──
  qs('#refreshBtn').addEventListener('click', async () => {
    if (!currentWeather) return;
    qs('#refreshBtn').classList.add('spinning');
    bustCache();
    await loadCoords(currentWeather.lat, currentWeather.lon);
    qs('#refreshBtn').classList.remove('spinning');
    showToast('Weather updated!', 'success');
  });

  // ── Fav button ──
  qs('#favCurrentBtn').addEventListener('click', () => {
    if (!currentWeather) return;
    if (isFavourite(currentWeather.city)) {
      removeFavourite(currentWeather.city);
      showToast(`Removed ${currentWeather.city} from favorites`);
    } else {
      addFavourite({ city:currentWeather.city, temp:currentWeather.temp, condition:currentWeather.condition });
      showToast(`${currentWeather.city} saved to favorites!`, 'success');
    }
    setFavIcon(isFavourite(currentWeather.city));
    renderFavourites(getFavourites(), loadCity, handleRemoveFav);
  });

  // ── Toast close ──
  qs('#toastClose').addEventListener('click', dismissToast);

  // ── Theme toggle ──
  qs('#themeToggle').addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const next = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    qs('#themeIcon').textContent = isDark ? '○' : '◑';
    savePrefs({ theme: next });
  });

  // ── Unit toggle ──
  qs('#unitToggle').addEventListener('click', async () => {
    prefs.units = prefs.units === 'metric' ? 'imperial' : 'metric';
    savePrefs({ units: prefs.units });
    qs('#unitLabel').textContent = prefs.units === 'metric' ? '°C' : '°F';
    if (currentWeather) {
      bustCache();
      await loadCoords(currentWeather.lat, currentWeather.lon);
    }
  });

  // ── Nav panel switching ──
  qsa('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchPanel(btn.dataset.panel);
      // Close mobile sidebar
      qs('#sidebar').classList.remove('open');
    });
  });

  // ── Mobile menu ──
  qs('#menuBtn').addEventListener('click', () => {
    qs('#sidebar').classList.toggle('open');
  });

  // ── Map layer buttons ──
  bindMapLayers(layer => {
    prefs.mapLayer = layer;
    savePrefs({ mapLayer: layer });
    if (currentWeather) updateMap(currentWeather.lat, currentWeather.lon, 'YOUR_API_KEY', layer);
  });

  // ── Online / offline events ──
  window.addEventListener('offline', () => {
    qs('#offlineBanner').hidden = false;
  });
  window.addEventListener('online', async () => {
    qs('#offlineBanner').hidden = true;
    if (currentWeather) {
      bustCache();
      await loadCoords(currentWeather.lat, currentWeather.lon);
    }
  });

  // ── PWA install prompt ──
  let deferredPrompt;
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    // Could show a custom "Install App" button here
  });
}

// ══════════════════════════════════════════════════
// FAVOURITES / HISTORY HANDLERS
// ══════════════════════════════════════════════════
function handleRemoveFav(city) {
  removeFavourite(city);
  renderFavourites(getFavourites(), loadCity, handleRemoveFav);
  if (currentWeather?.city === city) setFavIcon(false);
}

function handleRemoveHistory(city) {
  removeHistory(city);
  renderHistory(getHistory(), loadCity, handleRemoveHistory);
}

// ══════════════════════════════════════════════════
// VOICE SEARCH
// ══════════════════════════════════════════════════
function startVoiceSearch() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) { showToast('Voice search not supported in this browser'); return; }

  const recognition = new SpeechRecognition();
  recognition.lang  = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  const voiceBtn = qs('#voiceBtn');
  voiceBtn.classList.add('listening');

  recognition.start();
  recognition.onresult = e => {
    const city = e.results[0][0].transcript.trim();
    qs('#searchInput').value = city;
    loadCity(city);
  };
  recognition.onerror = () => showToast('Voice search failed. Please try again.');
  recognition.onend   = () => voiceBtn.classList.remove('listening');
}

// ══════════════════════════════════════════════════
// AUTO REFRESH
// ══════════════════════════════════════════════════
function scheduleAutoRefresh() {
  clearInterval(refreshTimer);
  refreshTimer = setInterval(async () => {
    if (!currentWeather || document.hidden) return;
    bustCache();
    await loadCoords(currentWeather.lat, currentWeather.lon).catch(() => {});
  }, REFRESH_MS);
}

// ══════════════════════════════════════════════════
// PREFS APPLY
// ══════════════════════════════════════════════════
function applyPrefs() {
  document.documentElement.setAttribute('data-theme', prefs.theme || 'dark');
  qs('#unitLabel').textContent = prefs.units === 'metric' ? '°C' : '°F';
  qs('#themeIcon').textContent = prefs.theme === 'dark' ? '◑' : '○';
}

// ══════════════════════════════════════════════════
// SERVICE WORKER (PWA)
// ══════════════════════════════════════════════════
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./sw.js').catch(() => {
    // SW optional; app still works without it
  });
}
