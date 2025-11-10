import requests

class OpenMeteoProvider:
    def __init__(self, lang="en", units=None):
        self.lang = lang
        self.units = units or {"temp": "celsius", "wind": "kmh"}

    def geocode(self, city, country=None):
        q = city if not country else f"{city},{country}"
        url = "https://geocoding-api.open-meteo.com/v1/search"
        r = requests.get(url, params={"name": q, "count": 1, "language": self.lang})
        if r.status_code != 200:
            return None
        data = r.json()
        if not data.get("results"):
            return None
        it = data["results"][0]
        name = f"{it.get('name')}, {it.get('country_code')}"
        return {"lat": it["latitude"], "lon": it["longitude"], "name": name}

    def fetch(self, location, hours=0, days=0):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location["lat"],
            "longitude": location["lon"],
            "current": ["temperature_2m","relative_humidity_2m","wind_speed_10m"],
            "hourly": ["temperature_2m","wind_speed_10m","precipitation_probability"],
            "daily": ["temperature_2m_max","temperature_2m_min","precipitation_probability_max"],
            "timezone": "auto",
            "temperature_unit": "fahrenheit" if self.units["temp"]=="fahrenheit" else "celsius",
            "wind_speed_unit": "mph" if self.units["wind"]=="mph" else "kmh",
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        j = r.json()

        current = {
            "temperature": f"{j['current']['temperature_2m']}°",
            "feels_like": "-",
            "humidity": f"{j['current']['relative_humidity_2m']}%",
            "wind": f"{j['current']['wind_speed_10m']} {self.units['wind']}",
            "description": "—",  # sem texto no endpoint básico
        }

        hourly = []
        if hours:
            times = j["hourly"]["time"][:hours]
            temps = j["hourly"]["temperature_2m"][:hours]
            winds = j["hourly"]["wind_speed_10m"][:hours]
            pops  = j["hourly"].get("precipitation_probability", [None]*hours)[:hours]
            for t, temp, w, p in zip(times, temps, winds, pops):
                hourly.append({
                    "time": t.replace("T"," "),
                    "temperature": f"{temp}°",
                    "wind": f"{w} {self.units['wind']}",
                    "pop": f"{p}%" if p is not None else "-",
                })

        daily = []
        if days:
            dates = j["daily"]["time"][:days]
            tmax = j["daily"]["temperature_2m_max"][:days]
            tmin = j["daily"]["temperature_2m_min"][:days]
            pops = j["daily"].get("precipitation_probability_max",[None]*days)[:days]
            for d, mx, mn, p in zip(dates, tmax, tmin, pops):
                daily.append({
                    "date": d,
                    "tmax": f"{mx}°",
                    "tmin": f"{mn}°",
                    "pop": f"{p}%" if p is not None else "-",
                })

        return current, hourly, daily