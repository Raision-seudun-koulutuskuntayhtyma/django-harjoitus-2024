from django.shortcuts import render
from django.http import HttpResponse


def indeksi(request):
    return HttpResponse("Heippa! Olet kysely-appin index-sivulla.")


def näytä(request, question_id):
    return HttpResponse(f"Katsot juuri kysymystä {question_id}")


def tulokset(request, question_id):
    return HttpResponse(f"Katsot kysymyksen {question_id} tuloksia")


def äänestä(request, question_id):
    return HttpResponse(f"Olet äänestämässä kysymykseen {question_id}")
