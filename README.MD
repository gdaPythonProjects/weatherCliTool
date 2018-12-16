# CLIWeatherTool

CLIWeatherTool jest aplikacją służącą do pobierania informacji o aktualnej i przyszłej pogodzie dla podanej lokalizacji.

## Installation

W celu uruchomienia aplikacji konieczne jest jej sklonowanie oraz zainstalowanie niezbędnych bibliotek 
z wykorzystaniem managera pip oraz pythona w wersji 3.6>

```bash
pip install -r requirements.txt
```

## Usage

W celu skorzystania z aplikacji konieczne jest zarejestrowanie się na stronach oraz pobranie kluczy apikey:
http://www.mapquestapi.com - do pobrania współrzędnych geograficznych na podstawie określonej lokalizacji
https://api2.climacell.co - do pobrania aktualnej i przyszłej prognozy pogody na podstawie współrzędnych geograficznych

Obydwa serwisy umożliwiają korzystanie z udostępnionego API bez konieczności ponoszenia dodatkowych opłat 
(do określonej liczby wywołań miesięcznie).

Po zarejestrowaniu na w/w serwisach należy otrzymane klucze apikey wprowadzić do pliku config.ini utworzonego 
na podstawie config_default.ini 

```bash
# aktualna pogoda w Gdańsku
python weather.py --address=Gdansk

# aktualna pogoda w Gdańsku na al. Grunwaldzkiej
python weather.py --address=al.Grunwaldzka,Gdansk

# prognoza pogody w Gdańsku na następny dzień (1 oznacza dzień dzisiejszy)
python weather.py --address=Gdansk --forecast-days=2 
```
