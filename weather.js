const express = require("express");
const axios = require("axios");

const router = express.Router();

const BASE_URL = "https://api.openweathermap.org";
const key = () => process.env.OPENWEATHER_API_KEY;

function requireKey(res) {
  if (!key()) {
    res.status(500).json({
      error: "Server is missing OPENWEATHER_API_KEY. Add it to backend/.env",
    });
    return false;
  }
  return true;
}

/**
 * GET /api/weather/geocode?city=London
 * Look up matching places for a search box (name, country, lat/lon).
 */
router.get("/geocode", async (req, res) => {
  if (!requireKey(res)) return;
  const { city } = req.query;
  if (!city) return res.status(400).json({ error: "city query param is required" });

  try {
    const { data } = await axios.get(`${BASE_URL}/geo/1.0/direct`, {
      params: { q: city, limit: 5, appid: key() },
    });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: "Failed to geocode city" });
  }
});

/**
 * GET /api/weather/reverse?lat=..&lon=..
 * Turn coordinates (from the browser's geolocation) into a place name.
 */
router.get("/reverse", async (req, res) => {
  if (!requireKey(res)) return;
  const { lat, lon } = req.query;
  if (!lat || !lon) return res.status(400).json({ error: "lat and lon query params are required" });

  try {
    const { data } = await axios.get(`${BASE_URL}/geo/1.0/reverse`, {
      params: { lat, lon, limit: 1, appid: key() },
    });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: "Failed to reverse geocode" });
  }
});

/**
 * GET /api/weather/current?lat=..&lon=..&units=metric
 */
router.get("/current", async (req, res) => {
  if (!requireKey(res)) return;
  const { lat, lon, units = "metric" } = req.query;
  if (!lat || !lon) return res.status(400).json({ error: "lat and lon query params are required" });

  try {
    const { data } = await axios.get(`${BASE_URL}/data/2.5/weather`, {
      params: { lat, lon, units, appid: key() },
    });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: "Failed to fetch current weather" });
  }
});

/**
 * GET /api/weather/forecast?lat=..&lon=..&units=metric
 * Returns the raw 5-day / 3-hour forecast list; the frontend derives
 * an hourly strip and a daily summary from it.
 */
router.get("/forecast", async (req, res) => {
  if (!requireKey(res)) return;
  const { lat, lon, units = "metric" } = req.query;
  if (!lat || !lon) return res.status(400).json({ error: "lat and lon query params are required" });

  try {
    const { data } = await axios.get(`${BASE_URL}/data/2.5/forecast`, {
      params: { lat, lon, units, appid: key() },
    });
    res.json(data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: "Failed to fetch forecast" });
  }
});

/**
 * GET /api/weather/maptile/:layer/:z/:x/:y
 * Proxies OpenWeatherMap's tile layers so the API key stays server-side
 * even though the browser is the one requesting each tile.
 */
router.get("/maptile/:layer/:z/:x/:y", async (req, res) => {
  if (!requireKey(res)) return;
  const { layer, z, x, y } = req.params;
  const allowedLayers = ["clouds_new", "precipitation_new", "pressure_new", "wind_new", "temp_new"];
  if (!allowedLayers.includes(layer)) {
    return res.status(400).json({ error: "Unknown map layer" });
  }

  try {
    const response = await axios.get(
      `${BASE_URL}/map/${layer}/${z}/${x}/${y}.png`,
      { params: { appid: key() }, responseType: "arraybuffer" }
    );
    res.set("Content-Type", "image/png");
    res.send(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({ error: "Failed to fetch map tile" });
  }
});

module.exports = router;
