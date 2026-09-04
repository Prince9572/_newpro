import React, { useCallback, useEffect, useState } from "react";
import SearchBar from "./components/SearchBar";
import CurrentWeather from "./components/CurrentWeather";
import HourlyForecast from "./components/HourlyForecast";
import DailyForecast from "./components/DailyForecast";
import WeatherMap from "./components/WeatherMap";
import { getCurrentWeather, getForecast, reverseGeocode } from "./api/weatherApi";
import { deriveDaily } from "./utils/deriveDaily";
import "./App.css";

export default function App() {
  const [place, setPlace] = useState(null); // { lat, lon, name }
  const [units, setUnits] = useState("metric");
  const [current, setCurrent] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);
  const [locating, setLocating] = useState(false);
  const [error, setError] = useState(null);

  const loadWeather = useCallback(async (lat, lon, unitSystem) => {
    setLoading(true);
    setError(null);
    try {
      const [currentData, forecastData] = await Promise.all([
        getCurrentWeather(lat, lon, unitSystem),
        getForecast(lat, lon, unitSystem),
      ]);
      setCurrent(currentData);
      setForecast(forecastData);
    } catch (err) {
      setError("Couldn't load weather for that location. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (place) loadWeather(place.lat, place.lon, units);
  }, [place, units, loadWeather]);

  function handleSelectPlace(p) {
    setPlace({ lat: p.lat, lon: p.lon, name: p.name });
  }

  function handleUseLocation() {
    if (!navigator.geolocation) {
      setError("Geolocation isn't supported by this browser.");
      return;
    }
    setLocating(true);
    setError(null);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;
        try {
          const results = await reverseGeocode(latitude, longitude);
          const name = results?.[0]?.name || "Your location";
          setPlace({ lat: latitude, lon: longitude, name });
        } catch {
          setPlace({ lat: latitude, lon: longitude, name: "Your location" });
        } finally {
          setLocating(false);
        }
      },
      () => {
        setLocating(false);
        setError("Couldn't get your location. Please allow location access or search for a city.");
      }
    );
  }

  function toggleUnits() {
    setUnits((u) => (u === "metric" ? "imperial" : "metric"));
  }

  const daily = forecast ? deriveDaily(forecast.list, forecast.city.timezone) : [];

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__logo">Skyline</h1>
        <SearchBar
          onSelectPlace={handleSelectPlace}
          onUseLocation={handleUseLocation}
          locating={locating}
        />
      </header>

      <main className="app__main">
        {!place && !loading && (
          <div className="app__empty">
            <p>Search for a city or use your location to see the forecast.</p>
          </div>
        )}

        {error && <div className="app__error">{error}</div>}

        {loading && <div className="app__loading">Loading weather…</div>}

        {!loading && current && forecast && (
          <>
            <CurrentWeather data={current} units={units} onToggleUnits={toggleUnits} />
            <HourlyForecast
              list={forecast.list}
              timezone={forecast.city.timezone}
              units={units}
              sunrise={current.sys.sunrise}
              sunset={current.sys.sunset}
            />
            <DailyForecast days={daily} timezone={forecast.city.timezone} units={units} />
            <WeatherMap lat={forecast.city.coord.lat} lon={forecast.city.coord.lon} />
          </>
        )}
      </main>
    </div>
  );
}
