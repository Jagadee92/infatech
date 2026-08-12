from django.urls import path

from . import views


app_name = "companies"

urlpatterns = [
    path("", views.peers, name="peers"),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
]
