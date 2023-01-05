from django.urls import include, path
from .views import weather_view, yield_view, stats_view

corteva_urls = [
    path("weather/", weather_view),
    path("yield/", yield_view),
    path("weather/stats/", stats_view),
]

urlpatterns = [
    path("", include(corteva_urls)),
]
