import subprocess, sys, pathlib

def test_package_exists():
    assert pathlib.Path('weather_api').exists()

def test_help_runs():
    p = subprocess.run([sys.executable, "-m", "weather_api", "--help"], capture_output=True)
    assert p.returncode == 0