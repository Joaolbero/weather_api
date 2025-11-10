def parse_units(units):
    if units == "imperial":
        return {"temp": "fahrenheit", "wind": "mph"}
    return {"temp": "celsius", "wind": "kmh"}

def parse_lang(lang):
    return lang or "en"
