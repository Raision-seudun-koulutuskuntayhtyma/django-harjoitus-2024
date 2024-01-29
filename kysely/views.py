from django.shortcuts import render
from django.http import HttpResponse


def indeksi(request):
    return HttpResponse("Heippa! Olet kysely-appin index-sivulla.")
