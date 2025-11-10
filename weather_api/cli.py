import os
import argparse
from rich.console import Console
from rich.table import Table
from .providers.open_meteo import OpenMeteoProvider
from .providers.openweather import OpenWeatherProvider
from .util import parse_units, parse_lang

console = Console()

def build_parser():
    p = argparse.ArgumentParser(
        description="Weather API CLI / Consulta de Clima via API (PT/EN)"
    )
    p.add_argument("--city", type=str, help="City name / Nome da cidade")
    p.add_argument("--country", type=str, help="Country code (e.g., BR, US)")
    p.add_argument("--lat", type=float, help="Latitude (alternative to city)")
    p.add_argument("--lon", type=float, help="Longitude (alternative to city)")
    p.add_argument("--provider", type=str, default="open-meteo",
                   choices=["open-meteo", "openweather"],
                   help="Weather provider (default: open-meteo)")
    p.add_argument("--units", type=str, default="metric",
                   choices=["metric", "imperial"],
                   help="Units for temperature/wind (default: metric)")
    p.add_argument("--lang", type=str, default="en",
                   help="Language code (e.g., en, pt)")
    p.add_argument("--hourly", type=int, default=0,
                   help="Show next N hours (0=none)")
    p.add_argument("--daily", type=int, default=0,
                   help="Show next N days (0=none)")
    return p

def main(argv=None):
    args = build_parser().parse_args(argv)
    units = parse_units(args.units)
    lang = parse_lang(args.lang)

    if args.provider == "open-meteo":
        provider = OpenMeteoProvider(lang=lang, units=units)
    else:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            console.print("[red]OPENWEATHER_API_KEY not set[/red]")
            return 2
        provider = OpenWeatherProvider(api_key=api_key, lang=lang, units=units)

    if args.lat is not None and args.lon is not None:
        location = {"lat": args.lat, "lon": args.lon, "name": f"{args.lat},{args.lon}"}
    elif args.city:
        location = provider.geocode(city=args.city, country=args.country)
        if not location:
            console.print("[red]Location not found / Local não encontrado[/red]")
            return 1
    else:
        console.print("[yellow]Provide --city or --lat/--lon[/yellow]")
        return 2

    current, hourly, daily = provider.fetch(location, hours=args.hourly, days=args.daily)

    console.rule(f"[bold]Weather · Clima[/bold] · {location['name']}")

    t = Table(title="Current / Atual")
    t.add_column("Temp")
    t.add_column("Feels")
    t.add_column("Humidity")
    t.add_column("Wind")
    t.add_column("Desc")
    t.add_row(
        current.get("temperature","-"),
        current.get("feels_like","-"),
        current.get("humidity","-"),
        current.get("wind","-"),
        current.get("description","-"),
    )
    console.print(t)

    if hourly:
        th = Table(title="Next Hours / Próximas Horas")
        th.add_column("Time")
        th.add_column("Temp")
        th.add_column("Wind")
        th.add_column("Rain%")
        for row in hourly:
            th.add_row(row["time"], row["temperature"], row["wind"], row.get("pop","-"))
        console.print(th)

    if daily:
        td = Table(title="Next Days / Próximos Dias")
        td.add_column("Date")
        td.add_column("Min")
        td.add_column("Max")
        td.add_column("Rain%")
        for row in daily:
            td.add_row(row["date"], row["tmin"], row["tmax"], row.get("pop","-"))
        console.print(td)

    return 0