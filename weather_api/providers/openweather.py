import requests

class OpenWeatherProvider:
    def __init__(self, api_key, lang="en", units=None):
        self.api_key = api_key
        self.lang = lang
        self.units = units or {"temp": "celsius", "wind": "kmh"}

    def geocode(self, city, country=None):
        q = city if not country else f"{city},{country}"
        url = "http://api.openweathermap.org/geo/1.0/direct"
        r = requests.get(url, params={"q": q, "limit": 1, "appid": self.api_key})
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        it = data[0]
        name = f"{it.get('name')}, {it.get('country')}"
        return {"lat": it["lat"], "lon": it["lon"], "name": name}

    def fetch(self, location, hours=0, days=0):
        unit = "imperial" if self.units["temp"] == "fahrenheit" else "metric"
        url = "https://api.openweathermap.org/data/2.5/forecast"
        r = requests.get(url, params={
            "lat": location["lat"],
            "lon": location["lon"],
            "appid": self.api_key,
            "units": unit,
            "lang": self.lang
        })
        r.raise_for_status()
        j = r.json()

        # aproxima "current" do primeiro item da previsão (3h)
        first = j["list"][0]
        current = {
            "temperature": f"{round(first['main']['temp'])}°",
            "feels_like": f"{round(first['main']['feels_like'])}°",
            "humidity": f"{first['main']['humidity']}%",
            "wind": f"{first['wind']['speed']} {'mph' if unit=='imperial' else 'm/s'}",
            "description": first['weather'][0]['description'].capitalize(),
        }

        hourly = []
        if hours:
            steps = max(1, hours // 3)  # previsão é de 3 em 3 horas
            for it in j["list"][:steps]:
                hourly.append({
                    "time": it["dt_txt"],
                    "temperature": f"{round(it['main']['temp'])}°",
                    "wind": f"{it['wind']['speed']} {'mph' if unit=='imperial' else 'm/s'}",
                    "pop": f"{int(it.get('pop',0)*100)}%"
                })

        daily = []
        if days:
            from collections import defaultdict
            agg = defaultdict(lambda: {"tmin": 10**9, "tmax": -10**9, "pop": 0})
            for it in j["list"]:
                date = it["dt_txt"].split(" ")[0]
                t = it["main"]["temp"]
                agg[date]["tmin"] = min(agg[date]["tmin"], t)
                agg[date]["tmax"] = max(agg[date]["tmax"], t)
                agg[date]["pop"] = max(agg[date]["pop"], int(it.get("pop",0)*100))
            dates = sorted(agg.keys())[:days]
            for d in dates:
                daily.append({
                    "date": d,
                    "tmin": f"{round(agg[d]['tmin'])}°",
                    "tmax": f"{round(agg[d]['tmax'])}°",
                    "pop": f"{agg[d]['pop']}%",
                })

        return current, hourly, daily