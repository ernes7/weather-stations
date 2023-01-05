from django.core.management.base import BaseCommand
from dateutil.parser import parse
from api.models import WeatherModel, CornGrainModel, ResultsModel
from api.utils import read_weather_data, read_yield_data, analyze
import time
import datetime
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_time = time.perf_counter()
        num_weather_records = 0
        num_yield_records = 0
        print("Start Time: ", datetime.datetime.now().strftime("%H:%M:%S"))

        print("Reading Weather Data...")
        weather = read_weather_data("Data/wx_data")
        weather_data = []
        weather_records = WeatherModel.objects.all().values_list("station", "date")

        # Create a set of tuples from the weather_records queryset
        weather_records_set = {(record[0], record[1]) for record in weather_records}

        for record in weather:
            # Transform date
            date = parse(record["date"]).date()
            if (record["station"], date) not in weather_records_set:
                weather_data.append(
                    {
                        "station": record["station"],
                        "date": date,
                        "max_temp": record["max_temp"],
                        "min_temp": record["min_temp"],
                        "amount_precipitation": record["precipitation"],
                    }
                )
                num_weather_records += 1

        print("Reading Yield Data...")
        grain = read_yield_data("./Data/yld_data/US_corn_grain_yield.txt")
        yield_data = []
        yield_records = CornGrainModel.objects.all().values_list(
            "year", "total_harvested"
        )
        for record in grain:
            if (record["year"], record["total_harvested"]) not in yield_records:
                yield_data.append(
                    {
                        "year": record["year"],
                        "total_harvested": record["total_harvested"],
                    }
                )
                num_yield_records += 1

        print("Ingesting records...")
        with transaction.atomic():
            WeatherModel.objects.bulk_create(
                [WeatherModel(**record) for record in weather_data]
            )
            CornGrainModel.objects.bulk_create(
                [CornGrainModel(**record) for record in yield_data]
            )

        if len(weather_data) != 0:
            print("Analyzing Data...")
            analysis = analyze(WeatherModel.objects.all().values())

            print("Ingesting Results...")
            results_records = ResultsModel.objects.all().values_list("year", "station")
            results_data = [d for d in analysis if tuple(d.items()) in results_records]

            with transaction.atomic():
                ResultsModel.objects.bulk_create(
                    [ResultsModel(**record) for record in results_data]
                )

        end_time = time.perf_counter()
        print(
            f"Ingested {num_weather_records} weather records and ' + "
            f"{num_yield_records} yield records in {end_time - start_time:.2f} seconds"
        )

        print("End Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
