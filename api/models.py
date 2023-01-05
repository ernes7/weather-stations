from django.db import models


# Weather Station Temperatures and Precipitation
class WeatherModel(models.Model):
    station = models.CharField(blank=False, max_length=11)
    # The date (YYYYMMDD format)
    date = models.DateField(null=True)
    # The maximum temperature for that day (in tenths of a degree Celsius)
    max_temp = models.IntegerField(null=True)
    # The minimum temperature for that day (in tenths of a degree Celsius)
    min_temp = models.IntegerField(null=True)
    # The amount of precipitation for that day (in tenths of a millimeter)
    amount_precipitation = models.IntegerField(null=True, default=None)

    class Meta:
        unique_together = ("station", "date")


# Corn Grain Harvested in a year
class CornGrainModel(models.Model):
    # total harvested corn grain yield in the United States measured in 1000s of megatons
    year = models.CharField(max_length=4, null=True)
    total_harvested = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("year", "total_harvested")


class ResultsModel(models.Model):
    # year
    year = models.CharField(max_length=4)
    # station
    station = models.CharField(blank=False, max_length=11)
    # Average maximum temperature (in degrees Celsius)
    avg_max_temp = models.IntegerField(null=True)
    # Average minimum temperature (in degrees Celsius)
    avg_min_temp = models.IntegerField(null=True)
    # Total accumulated precipitation (in centimeters)
    total_precipitation = models.PositiveIntegerField()

    class Meta:
        unique_together = ("year", "station")
