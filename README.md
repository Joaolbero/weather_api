# Weather API CLI / Consulta de Clima via API

**EN:** Command-line tool using **Open-Meteo** (no API key) or **OpenWeather** (API key).  
**PT-BR:** Ferramenta de linha de comando usando **Open-Meteo** (sem chave) ou **OpenWeather** (com chave).

## Quickstart / Início Rápido
```bash
# Install deps globally / Instale deps globalmente
pip install -r requirements.txt

# Open-Meteo (no key / sem chave)
python -m weather_api --city "São Paulo" --country BR --lang pt --provider open-meteo --hourly 6 --daily 3

# OpenWeather (needs key / precisa chave)
# Windows (persiste):
setx OPENWEATHER_API_KEY "SUA_CHAVE_AQUI"
# Abra novo PowerShell e execute:
python -m weather_api --city "São Paulo" --country BR --lang pt --provider openweather --hourly 6 --daily 3