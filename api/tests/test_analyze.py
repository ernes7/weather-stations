from datetime import datetime
from api.utils import analyze, read_weather_data
import timeit


def test_read_files():
    execution_time = timeit.timeit(lambda: read_weather_data("Data/wx_data"), number=1)
    # define a threshold for the maximum allowed execution time in seconds
    max_time = 2
    # assert that the execution time is below the threshold
    assert execution_time < max_time


def test_analyze():
    # List of dictionaries with test data
    dict_list = [
        {
            "station": "A",
            "date": datetime(2022, 1, 1),
            "max_temp": 20,
            "min_temp": 1,
            "amount_precipitation": 100,
        },
        {
            "station": "A",
            "date": datetime(2022, 1, 2),
            "max_temp": 22,
            "min_temp": 2,
            "amount_precipitation": 100,
        },
        {
            "station": "A",
            "date": datetime(2022, 1, 3),
            "max_temp": 21,
            "min_temp": 3,
            "amount_precipitation": 100,
        },
        {
            "station": "B",
            "date": datetime(2022, 1, 1),
            "max_temp": 25,
            "min_temp": 4,
            "amount_precipitation": 100,
        },
        {
            "station": "B",
            "date": datetime(2022, 1, 2),
            "max_temp": 27,
            "min_temp": 5,
            "amount_precipitation": 100,
        },
        {
            "station": "B",
            "date": datetime(2022, 1, 3),
            "max_temp": 26,
            "min_temp": 6,
            "amount_precipitation": 100,
        },
        {
            "station": "B",
            "date": datetime(2022, 1, 3),
            "max_temp": None,
            "min_temp": None,
            "amount_precipitation": 100,
        },
    ]

    results = analyze(dict_list)

    assert results == [
        {
            "station": "A",
            "year": 2022,
            "avg_max_temp": 2.10,
            "avg_min_temp": 0.20,
            "total_precipitation": 0.30,
        },
        {
            "station": "B",
            "year": 2022,
            "avg_max_temp": 2.60,
            "avg_min_temp": 0.50,
            "total_precipitation": 0.40,
        },
    ]
