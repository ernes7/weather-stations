# Weather Data from Stations by Year

## Description

Application ingest some weather and crop yield data from a Data folder, contains the database schemas for it,
and expose the data through a REST API.

The wx_data directory has files containing weather data records from 1985-01-01 to 2014-12-31.
Each file corresponds to a particular weather station

For every year, for every weather station, the following is calculated:

* Average maximum temperature (in degrees Celsius)

* Average minimum temperature (in degrees Celsius)

* Total accumulated precipitation (in centimeters)

## Endpoints

- /api/weather
- /api/yield
- /api/weather/stats

Each endpoint returns a JSON-formatted response with a representation of the ingested data
Can be filtered by date and station ID (where present) using the query string.
Data is paginated.

## Facts

- ~22 Seconds if not new records
- ~60 Seconds with clean database
- Able to ingest more than a million records from 167 different files

## Commands

### Run

`make run0` Just run

`make run1` Add/update data and run

### Clean Database

`python manage.py flush` or `make clean`

### Run Server

`python manage.py runserver`

### Populate Database

`python manage.py ingest_data`

### Test

`python -m pytest -s api/` or `make test`

## Tools

- Python 3.10
- Django Rest Framework
- SQL lite
- Flake8
- Pytest
- Black