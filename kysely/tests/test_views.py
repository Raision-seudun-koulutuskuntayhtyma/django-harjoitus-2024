import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Kysymys


def luo_kysymys(teksti, days):
    aika = timezone.now() + datetime.timedelta(days=days)
    return Kysymys.objects.create(
        teksti=teksti,
        julkaisupvm=aika,
    )


class IndeksiNäkymänTestit(TestCase):
    def test_ei_kysymyksiä(self):
        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertEqual(vastaus.status_code, 200)  # HTTP-koodi 200 = OK
        self.assertContains(vastaus, "Ei kyselyitä saatavilla.")
        self.assertQuerySetEqual(vastaus.context["kysymykset"], [])

    def test_mennyt_kysymys(self):
        kysymys = luo_kysymys("Mennyt kysymys", days=-30)

        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertContains(vastaus, kysymys.teksti)
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_tuleva_kysymys(self):
        luo_kysymys("Tuleva kysymys", days=30)

        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertContains(vastaus, "Ei kyselyitä saatavilla.")
        self.assertQuerySetEqual(vastaus.context["kysymykset"], [])

    def test_tuleva_ja_mennyt_kysymys(self):
        kysymys = luo_kysymys("Mennyt kysymys", days=-30)
        luo_kysymys("Tuleva kysymys", days=30)

        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertContains(vastaus, "Mennyt kysymys")
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_2_mennyttä_kysymystä(self):
        kysymys1 = luo_kysymys("Mennyt kysymys 1", days=-30)
        kysymys2 = luo_kysymys("Mennyt kysymys 2", days=-5)

        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertContains(vastaus, "Mennyt kysymys 1")
        self.assertContains(vastaus, "Mennyt kysymys 2")
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys2, kysymys1],
        )


class NäytäNäkymänTestit(TestCase):
    def test_tuleva_kysymys(self):
        tuleva_kysymys = luo_kysymys("Tuleva kysymys", days=5)
        osoite = reverse("kysely:näytä", args=(tuleva_kysymys.id,))

        vastaus = self.client.get(osoite)

        self.assertEqual(vastaus.status_code, 404)  # HTTP-koodi 404 = ei löydy

    def test_mennyt_kysymys(self):
        mennyt_kysymys = luo_kysymys("Mennyt kysymys", days=-5)
        osoite = reverse("kysely:näytä", args=(mennyt_kysymys.id,))

        vastaus = self.client.get(osoite)

        self.assertContains(vastaus, mennyt_kysymys.teksti)
