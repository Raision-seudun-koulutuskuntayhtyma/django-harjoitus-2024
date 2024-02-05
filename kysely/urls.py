from django.urls import path

from . import views

app_name = "kysely"
urlpatterns = [
    # esim. /kyselyt/
    path("", views.ListaNäkymä.as_view(), name="indeksi"),
    # esim. /kyselyt/5/
    path("<int:pk>/", views.NäytäNäkymä.as_view(), name="näytä"),
    # esim. /kyselyt/5/tulokset/
    path(
        "<int:pk>/tulokset/",
        views.TuloksetNäkymä.as_view(),
        name="tulokset",
    ),
    # esim. /kyselyt/5/äänestä/
    path("<int:kysymys_id>/äänestä/", views.äänestä, name="äänestä"),
]
