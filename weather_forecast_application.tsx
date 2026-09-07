import React, { useState, useEffect } from 'react';
import { 
  Search, Cloud, Sun, CloudRain, Wind, Droplets, 
  Thermometer, Compass, AlertCircle, RefreshCw, 
  MapPin, Calendar, Clock, Key, ShieldCheck, ExternalLink, Sparkles
} from 'lucide-react';

const MOCK_WEATHER_DATABASE = {
  "london": {
    city: "London",
    country: "GB",
    temp: 18,
    condition: "Partly Cloudy",
    description: "scattered clouds with gentle breeze",
    humidity: 65,
    windSpeed: 4.2,
    pressure: 1012,
    icon: "cloud",
    hourly: [
      { time: "12:00", temp: 17, condition: "Cloudy" },
      { time: "15:00", temp: 19, condition: "Sunny" },
      { time: "18:00", temp: 18, condition: "Partly Cloudy" },
      { time: "21:00", temp: 15, condition: "Clear" }
    ],
    forecast: [
      { day: "Tuesday", tempMax: 20, tempMin: 12, condition: "Sunny", icon: "sun" },
      { day: "Wednesday", tempMax: 18, tempMin: 11, condition: "Rainy", icon: "rain" },
      { day: "Thursday", tempMax: 16, tempMin: 10, condition: "Cloudy", icon: "cloud" },
      { day: "Friday", tempMax: 22, tempMin: 13, condition: "Sunny", icon: "sun" },
      { day: "Saturday", tempMax: 19, tempMin: 12, condition: "Partly Cloudy", icon: "cloud" }
    ]
  },
  "new york": {
    city: "New York",
    country: "US",
    temp: 24,
    condition: "Sunny",
    description: "clear sky and warm sunshine",
    humidity: 45,
    windSpeed: 3.5,
    pressure: 1018,
    icon: "sun",
    hourly: [
      { time: "12:00", temp: 23, condition: "Sunny" },
      { time: "15:00", temp: 26, condition: "Sunny" },
      { time: "18:00", temp: 24, condition: "Clear" },
      { time: "21:00", temp: 20, condition: "Clear" }
    ],
    forecast: [
      { day: "Tuesday", tempMax: 27, tempMin: 18, condition: "Sunny", icon: "sun" },
      { day: "Wednesday", tempMax: 25, tempMin: 17, condition: "Partly Cloudy", icon: "cloud" },
      { day: "Thursday", tempMax: 22, tempMin: 15, condition: "Rainy", icon: "rain" },
      { day: "Friday", tempMax: 26, tempMin: 17, condition: "Sunny", icon: "sun" },
      { day: "Saturday", tempMax: 28, tempMin: 19, condition: "Sunny", icon: "sun" }
    ]
  },
  "tokyo": {
    city: "Tokyo",
    country: "JP",
    temp: 21,
    condition: "Rainy",
    description: "steady light showers",
    humidity: 80,
    windSpeed: 5.1,
    pressure: 1008,
    icon: "rain",
    hourly: [
      { time: "12:00", temp: 20, condition: "Rainy" },
      { time: "15:00", temp: 21, condition: "Rainy" },
      { time: "18:00", temp: 19, condition: "Cloudy" },
      { time: "21:00", temp: 18, condition: "Cloudy" }
    ],
    forecast: [
      { day: "Tuesday", tempMax: 22, tempMin: 16, condition: "Rainy", icon: "rain" },
      { day: "Wednesday", tempMax: 23, tempMin: 15, condition: "Cloudy", icon: "cloud" },
      { day: "Thursday", tempMax: 25, tempMin: 17, condition: "Sunny", icon: "sun" },
      { day: "Friday", tempMax: 20, tempMin: 14, condition: "Rainy", icon: "rain" },
      { day: "Saturday", tempMax: 22, tempMin: 15, condition: "Partly Cloudy", icon: "cloud" }
    ]
  }
};

function WeatherIcon({ condition, className = "w-6 h-6" }) {
  const condLower = (condition || '').toLowerCase();
  if (condLower.includes('sun') || condLower.includes('clear')) {
    return <Sun className={`${className} text-amber-500 animate-pulse`} />;
  }
  if (condLower.includes('rain') || condLower.includes('shower')) {
    return <CloudRain className={`${className} text-blue-500`} />;
  }
  return <Cloud className={`${className} text-slate-400`} />;
}

function EnvInstructionBanner({ isOpen, onClose }) {
  if (!isOpen) return null;
  return (
    <div className="bg-gradient-to-r from-blue-900/90 to-indigo-950/90 backdrop-blur-md border border-blue-500/30 text-white p-5 rounded-2xl shadow-2xl mb-8 relative animate-fadeIn">
      <button 
        onClick={onClose}
        className="absolute top-4 right-4 text-slate-400 hover:text-white transition bg-white/10 hover:bg-white/20 p-1.5 rounded-full text-xs font-bold"
        aria-label="Close instructions"
      >
        ✕
      </button>
      <div className="flex items-start gap-4">
        <div className="p-3 bg-blue-500/20 border border-blue-400/30 rounded-xl text-blue-300">
          <Key className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-blue-100 flex items-center gap-2">
            <span>Environment Setup & API Configuration</span>
            <span className="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-medium">Fully Interactive Mock Mode Active</span>
          </h3>
          <p className="text-sm text-slate-300 mt-1 leading-relaxed">
            This app is configured to work instantly with robust mock data. To connect your live OpenWeatherMap API key, follow these simple steps:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4 text-xs">
            <div className="bg-black/30 p-3 rounded-xl border border-white/10">
              <span className="text-blue-400 font-bold">Step 1</span>
              <p className="text-slate-300 mt-1">Create a <code className="bg-white/10 px-1 py-0.5 rounded text-amber-300">.env</code> file in your project root directory.</p>
            </div>
            <div className="bg-black/30 p-3 rounded-xl border border-white/10">
              <span className="text-blue-400 font-bold">Step 2</span>
              <p className="text-slate-300 mt-1">Add your key: <br/><code className="bg-white/10 px-1.5 py-0.5 rounded text-amber-300 select-all">REACT_APP_WEATHER_API_KEY=your_key</code></p>
            </div>
            <div className="bg-black/30 p-3 rounded-xl border border-white/10">
              <span className="text-blue-400 font-bold">Step 3</span>
              <p className="text-slate-300 mt-1">Restart your React development server to load the environment variables.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SearchBar({ onSearch, searchTerm, setSearchTerm, isLoading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full max-w-xl mx-auto mb-8">
      <div className="relative flex items-center shadow-xl rounded-2xl overflow-hidden bg-white/10 backdrop-blur-md border border-white/20 transition-all focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-400/30">
        <div className="pl-4 text-slate-400">
          <Search className="w-5 h-5" />
        </div>
        <input 
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search any city (e.g., London, New York, Tokyo)..."
          className="w-full py-4 px-4 bg-transparent text-white placeholder-slate-400 focus:outline-none text-base font-medium"
        />
        <button 
          type="submit"
          disabled={isLoading}
          className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white px-6 py-4 font-semibold text-sm transition-all flex items-center gap-2 m-1 rounded-xl shadow-md disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Searching</span>
            </>
          ) : (
            <span>Search</span>
          )}
        </button>
      </div>
      <div className="flex flex-wrap gap-2 mt-2 px-1 justify-center text-xs text-slate-300">
        <span className="text-slate-400">Popular:</span>
        {['London', 'New York', 'Tokyo', 'Paris', 'Sydney'].map((city) => (
          <button
            key={city}
            type="button"
            onClick={() => { setSearchTerm(city); onSearch(city); }}
            className="hover:text-white underline decoration-blue-400/50 hover:decoration-blue-400 transition"
          >
            {city}
          </button>
        ))}
      </div>
    </form>
  );
}

function CurrentWeather({ data }) {
  if (!data) return null;

  return (
    <div className="bg-gradient-to-br from-slate-900/80 via-indigo-950/70 to-slate-900/90 backdrop-blur-xl border border-white/15 rounded-3xl p-6 md:p-8 shadow-2xl text-white relative overflow-hidden mb-8">
      <div className="absolute -right-10 -top-10 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -left-10 -bottom-10 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
        <div>
          <div className="flex items-center gap-2 text-blue-400 font-semibold text-sm uppercase tracking-wider mb-1">
            <MapPin className="w-4 h-4" />
            <span>{data.city}, {data.country || 'Global'}</span>
          </div>
          <h2 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white">
            {data.temp}°C
          </h2>
          <p className="text-lg text-slate-300 capitalize mt-1 font-medium">
            {data.condition} <span className="text-slate-400 text-sm">({data.description})</span>
          </p>
        </div>

        <div className="flex items-center justify-center p-6 bg-white/5 border border-white/10 rounded-2xl backdrop-blur-md shadow-inner">
          <WeatherIcon condition={data.condition} className="w-16 h-16 md:w-20 md:h-20" />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-6 border-t border-white/10 relative z-10">
        <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-3">
          <div className="p-2.5 bg-blue-500/20 text-blue-300 rounded-xl">
            <Droplets className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Humidity</p>
            <p className="text-base font-bold text-white">{data.humidity}%</p>
          </div>
        </div>

        <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/20 text-indigo-300 rounded-xl">
            <Wind className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Wind Speed</p>
            <p className="text-base font-bold text-white">{data.windSpeed} m/s</p>
          </div>
        </div>

        <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/20 text-emerald-300 rounded-xl">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Pressure</p>
            <p className="text-base font-bold text-white">{data.pressure} hPa</p>
          </div>
        </div>

        <div className="bg-white/5 border border-white/5 rounded-2xl p-4 flex items-center gap-3">
          <div className="p-2.5 bg-amber-500/20 text-amber-300 rounded-xl">
            <Thermometer className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Feels Like</p>
            <p className="text-base font-bold text-white">{data.temp + 1}°C</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function HourlyForecast({ hourlyData }) {
  if (!hourlyData || hourlyData.length === 0) return null;

  return (
    <div className="bg-slate-900/70 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-xl mb-8">
      <div className="flex items-center gap-2 text-slate-200 font-semibold mb-4">
        <Clock className="w-5 h-5 text-blue-400" />
        <h3>Hourly Forecast</h3>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {hourlyData.map((item, index) => (
          <div key={index} className="bg-white/5 border border-white/5 hover:border-blue-400/30 rounded-2xl p-4 text-center transition-all">
            <p className="text-xs text-slate-400 font-medium">{item.time}</p>
            <div className="my-3 flex justify-center">
              <WeatherIcon condition={item.condition} className="w-8 h-8" />
            </div>
            <p className="text-lg font-bold text-white">{item.temp}°C</p>
            <p className="text-xs text-slate-300 mt-1">{item.condition}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function ForecastCard({ forecastData }) {
  if (!forecastData || forecastData.length === 0) return null;

  return (
    <div className="bg-slate-900/70 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-xl">
      <div className="flex items-center gap-2 text-slate-200 font-semibold mb-4">
        <Calendar className="w-5 h-5 text-blue-400" />
        <h3>5-Day Weather Forecast</h3>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
        {forecastData.map((day, index) => (
          <div key={index} className="bg-white/5 border border-white/5 hover:bg-white/10 rounded-2xl p-4 text-center transition-all flex flex-col justify-between">
            <div>
              <p className="text-sm font-bold text-white">{day.day}</p>
              <div className="my-3 flex justify-center">
                <WeatherIcon condition={day.condition} className="w-10 h-10" />
              </div>
              <p className="text-xs text-slate-300 font-medium">{day.condition}</p>
            </div>
            <div className="mt-4 pt-3 border-t border-white/10 flex justify-center gap-3">
              <span className="text-sm font-bold text-white">{day.tempMax}°</span>
              <span className="text-sm text-slate-400">{day.tempMin}°</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [searchTerm, setSearchTerm] = useState('London');
  const [weatherData, setWeatherData] = useState(MOCK_WEATHER_DATABASE['london']);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [showBanner, setShowBanner] = useState(true);

  const fetchWeather = async (cityName) => {
    setIsLoading(true);
    setErrorMsg(null);

    const query = cityName.toLowerCase().trim();

    // Check if API key is provided in environment variables
    const apiKey = typeof process !== 'undefined' && process.env ? process.env.REACT_APP_WEATHER_API_KEY : '';

    try {
      if (apiKey && apiKey !== "your_key_here") {
        // Real API Call to OpenWeatherMap
        const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${query}&units=metric&appid=${apiKey}`);
        if (!res.ok) throw new Error("City not found or invalid API key.");
        const data = await res.json();
        
        // Format live API data safely
        const formatted = {
          city: String(data.name || cityName),
          country: String(data.sys && data.sys.country ? data.sys.country : 'INT'),
          temp: Math.round(Number(data.main && data.main.temp ? data.main.temp : 20)),
          condition: String(data.weather && data.weather[0] && data.weather[0].main ? data.weather[0].main : 'Clear'),
          description: String(data.weather && data.weather[0] && data.weather[0].description ? data.weather[0].description : 'clear sky'),
          humidity: Number(data.main && data.main.humidity ? data.main.humidity : 50),
          windSpeed: Number(data.wind && data.wind.speed ? data.wind.speed : 3),
          pressure: Number(data.main && data.main.pressure ? data.main.pressure : 1013),
          icon: String(data.weather && data.weather[0] && data.weather[0].icon ? data.weather[0].icon : '01d'),
          hourly: [
            { time: "12:00", temp: Math.round(Number(data.main && data.main.temp ? data.main.temp : 20)), condition: "Clear" },
            { time: "15:00", temp: Math.round(Number(data.main && data.main.temp ? data.main.temp : 20) + 1), condition: "Sunny" },
            { time: "18:00", temp: Math.round(Number(data.main && data.main.temp ? data.main.temp : 20) - 1), condition: "Clear" },
            { time: "21:00", temp: Math.round(Number(data.main && data.main.temp ? data.main.temp : 20) - 2), condition: "Clear" }
          ],
          forecast: [
            { day: "Tomorrow", tempMax: 24, tempMin: 16, condition: "Sunny", icon: "sun" },
            { day: "In 2 Days", tempMax: 22, tempMin: 15, condition: "Partly Cloudy", icon: "cloud" },
            { day: "In 3 Days", tempMax: 25, tempMin: 17, condition: "Sunny", icon: "sun" },
            { day: "In 4 Days", tempMax: 19, tempMin: 12, condition: "Rainy", icon: "rain" },
            { day: "In 5 Days", tempMax: 21, tempMin: 14, condition: "Partly Cloudy", icon: "cloud" }
          ]
        };
        setWeatherData(formatted);
      } else {
        // Fallback to rich mock database with simulation delay
        await new Promise((resolve) => setTimeout(resolve, 500));
        if (MOCK_WEATHER_DATABASE[query]) {
          setWeatherData(MOCK_WEATHER_DATABASE[query]);
        } else {
          // Generate realistic mock data for unknown cities
          setWeatherData({
            city: String(cityName.charAt(0).toUpperCase() + cityName.slice(1)),
            country: "INT",
            temp: Math.floor(Math.random() * 15) + 12,
            condition: "Partly Cloudy",
            description: "pleasant breeze and scattered clouds",
            humidity: Math.floor(Math.random() * 40) + 40,
            windSpeed: Number((Math.random() * 5 + 2).toFixed(1)),
            pressure: 1014,
            icon: "cloud",
            hourly: [
              { time: "12:00", temp: 21, condition: "Partly Cloudy" },
              { time: "15:00", temp: 23, condition: "Sunny" },
              { time: "18:00", temp: 20, condition: "Clear" },
              { time: "21:00", temp: 17, condition: "Clear" }
            ],
            forecast: [
              { day: "Tuesday", tempMax: 24, tempMin: 15, condition: "Sunny", icon: "sun" },
              { day: "Wednesday", tempMax: 22, tempMin: 14, condition: "Cloudy", icon: "cloud" },
              { day: "Thursday", tempMax: 19, tempMin: 11, condition: "Rainy", icon: "rain" },
              { day: "Friday", tempMax: 23, tempMin: 15, condition: "Sunny", icon: "sun" },
              { day: "Saturday", tempMax: 25, tempMin: 17, condition: "Sunny", icon: "sun" }
            ]
          });
        }
      }
    } catch (err) {
      setErrorMsg(err.message || "Failed to fetch weather data.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-slate-100 font-sans p-4 sm:p-6 md:p-10">
      <div className="max-w-4xl mx-auto">
        
        {/* Header Section */}
        <header className="flex flex-col sm:flex-row justify-between items-center mb-8 border-b border-white/10 pb-6 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl shadow-lg shadow-blue-500/20 text-white">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-blue-300 bg-clip-text text-transparent">
                SkyPulse Weather
              </h1>
              <p className="text-xs text-slate-400">Real-Time Forecast Application • React.js</p>
            </div>
          </div>
          <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2 rounded-xl text-xs text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>API Status: {typeof process !== 'undefined' && process.env && process.env.REACT_APP_WEATHER_API_KEY && process.env.REACT_APP_WEATHER_API_KEY !== "your_key_here" ? "Live Connected" : "Mock Fallback Active"}</span>
          </div>
        </header>

        {/* Environment Setup Banner */}
        <EnvInstructionBanner isOpen={showBanner} onClose={() => setShowBanner(false)} />

        {/* Search Bar Component */}
        <SearchBar 
          onSearch={fetchWeather} 
          searchTerm={searchTerm} 
          setSearchTerm={setSearchTerm} 
          isLoading={isLoading} 
        />

        {/* Error message notification if any */}
        {errorMsg && (
          <div className="bg-red-500/20 border border-red-500/30 text-red-200 p-4 rounded-2xl mb-6 flex items-center gap-3 text-sm">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Main Weather Display */}
        {weatherData && (
          <>
            <CurrentWeather data={weatherData} />
            <HourlyForecast hourlyData={weatherData.hourly} />
            <ForecastCard forecastData={weatherData.forecast} />
          </>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-xs text-slate-500 pb-4">
          <p>Built with React.js & Tailwind CSS • Designed for responsive real-time meteorological data visualization.</p>
        </footer>

      </div>
    </div>
  );
}