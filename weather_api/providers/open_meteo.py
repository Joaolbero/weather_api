import requests
import unicodedata

class OpenMeteoProvider:
    def __init__(self, lang="en", units=None):
        self.lang = lang
        self.units = units or {"temp": "celsius", "wind": "kmh"}

    def _strip_accents(self, s: str) -> str:
        return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

    def geocode(self, city, country=None):
        base_url = "https://geocoding-api.open-meteo.com/v1/search"
        country = (country or "").strip().upper() or None

        def query(name_value):
            r = requests.get(base_url, params={"name": name_value, "count": 5, "language": self.lang}, timeout=10)
            if r.status_code != 200:
                return []
            data = r.json() or {}
            return data.get("results") or []

        results = query(city) or query(self._strip_accents(city))
        if not results:
            return None

        chosen = None
        if country:
            for it in results:
                if (it.get("country_code") or "").upper() == country:
                    chosen = it
                    break
        if not chosen:
            chosen = results[0]

        name = f"{chosen.get('name')}, {chosen.get('country_code')}"
        return {"lat": chosen["latitude"], "lon": chosen["longitude"], "name": name}
