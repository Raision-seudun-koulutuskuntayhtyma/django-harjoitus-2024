from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


from .models import Kysymys, Vaihtoehto


def indeksi(request):
    kysymyslista = Kysymys.objects.order_by("-julkaisupvm")[:2]
    context = {
        "kysymykset": kysymyslista,
    }
    return render(request, "kysely/indeksi.html", context)


def näytä(request, kysymys_id):
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)
    return render(request, "kysely/näytä.html", {"kysymys": kysym})


def tulokset(request, kysymys_id):
    kysym = get_object_or_404(Kysymys, pk=kysymys_id)
    return render(request, "kysely/tulokset.html", {"kysymys": kysym})


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
