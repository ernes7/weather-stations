from .models import WeatherModel, CornGrainModel, ResultsModel
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from django.http import JsonResponse


def index(request):
    return HttpResponseRedirect(reverse("api"))


@api_view(
    [
        "GET",
    ]
)
def weather_view(request):
    weather_data = WeatherModel.objects.all()

    date = request.GET.get("date")
    station = request.GET.get("station")
    if date:
        weather_data = weather_data.filter(date=date)
    if station:
        weather_data = weather_data.filter(station=station)

    # Paginate the data
    paginator = Paginator(weather_data, 25)  # Show 25 items per page
    page = request.GET.get("page")
    weather = paginator.get_page(page)

    # Convert the data to a list of dictionaries
    weather_list = list(weather.object_list.values())

    # Return the data as a JSON response
    return JsonResponse(weather_list, safe=False)


@api_view(
    [
        "GET",
    ]
)
def stats_view(request):
    stats_data = ResultsModel.objects.all()

    year = request.GET.get("year")
    station = request.GET.get("station")
    if year:
        stats_data = stats_data.filter(year=year)
    if station:
        stats_data = stats_data.filter(station=station)

    # Paginate the data
    paginator = Paginator(stats_data, 25)  # Show 25 items per page
    page = request.GET.get("page")
    stats = paginator.get_page(page)

    # Convert the data to a list of dictionaries
    stats_list = list(stats.object_list.values())

    # Return the data as a JSON response
    return JsonResponse(stats_list, safe=False)


@api_view(
    [
        "GET",
    ]
)
def yield_view(request):
    yield_data = CornGrainModel.objects.all()

    year = request.GET.get("year")
    if year:
        yield_data = yield_data.filter(year=year)

    # Paginate the data
    paginator = Paginator(yield_data, 25)  # Show 25 items per page
    page = request.GET.get("page")
    yields = paginator.get_page(page)

    # Convert the data to a list of dictionaries
    yield_list = list(yields.object_list.values())

    # Return the data as a JSON response
    return JsonResponse(yield_list, safe=False)
