# 🌦️ Weather API CLI (Consulta de Clima via API)

Projeto em Python que consulta o clima atual e a previsão para as próximas horas ou dias.  
Ele funciona direto pelo terminal (linha de comando).

## 🔧 Funcionalidades
- Consulta clima usando duas APIs diferentes:
  - **Open-Meteo** → não precisa de chave de API.
  - **OpenWeather** → precisa da variável de ambiente `OPENWEATHER_API_KEY`.
- Mostra clima atual, previsão por horas e dias.
- Suporte a português e inglês.

---

## ⚙️ Instalação (sem venv, direto no Python global)
Abra o PowerShell na pasta do projeto e rode:
```bash
pip install -r requirements.txt