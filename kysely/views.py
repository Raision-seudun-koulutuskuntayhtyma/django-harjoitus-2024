from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Kysymys, Vaihtoehto


class ListaNäkymä(generic.ListView):
    template_name = "kysely/indeksi.html"
    context_object_name = "kysymykset"

    def get_queryset(self):
        # Otetaan nykyinen ajanhetki muuttujaan "nyt"
        nyt = timezone.now()

        # Aloitetaan hakemalla kaikki kysymykset
        kaikki_kysymykset = Kysymys.objects.all()

        # Suodatetaan (filter) kaikista kysymyksistä ne, joiden
        # julkaisupvm on pienempi tai yhtäsuuri kuin tämänhetkinen aika
        # (muuttujassa "nyt")
        #
        # Huom. lte = Less Than or Equal = pienempi tai yhtäsuuri
        ei_tulevaisuudessa = kaikki_kysymykset.filter(julkaisupvm__lte=nyt)

        # Järjestetään kysymykset julkaisupvm:n mukaan
        #
        # Huom. "-"-merkki edessä kääntää järjestyksen niin, että suuret
        # arvot tulevat ennen pieniä, jolloin uusimmat kysymykset ovat
        # ensimmäisenä
        järjestetyt_kysymykset = ei_tulevaisuudessa.order_by("-julkaisupvm")

        # Palautetaan järjestettyjen kysymysten listan alusta 2 ensimmäistä
        return järjestetyt_kysymykset[:2]


class NäytäNäkymä(generic.DetailView):
    model = Kysymys
    template_name = "kysely/näytä.html"

    def get_queryset(self):
        nyt = timezone.now()
        return Kysymys.objects.filter(julkaisupvm__lte=nyt)


class TuloksetNäkymä(generic.DetailView):
    model = Kysymys
    template_name = "kysely/tulokset.html"


def äänestä(request, kysymys_id):
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)
    try:
        valittu = kysym.vaihtoehto_set.get(pk=request.POST["valittu"])
    except (KeyError, Vaihtoehto.DoesNotExist):
        # Näytä kysymyslomake uudelleen
        return render(
            request,
            "kysely/näytä.html",
            {
                "kysymys": kysym,
                "virheviesti": "Et valinnut mitään vaihtoehtoa.",
            },
        )
    else:
        valittu.ääniä += 1
        valittu.save()
        osoite = reverse("kysely:tulokset", args=(kysym.id,))
        return HttpResponseRedirect(osoite)
