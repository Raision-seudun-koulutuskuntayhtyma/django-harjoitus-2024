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


class KysymysIndeksiNäkymäTests(TestCase):
    def test_ei_kysymyksiä(self):
        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertEqual(vastaus.status_code, 200)
        self.assertContains(vastaus, "Ei kyselyitä saatavilla.")
        self.assertQuerySetEqual(vastaus.context["kysymykset"], [])

    def test_mennyt_kysymys(self):
        kysymys = luo_kysymys("Mennyt kysymys", days=-30)

        vastaus = self.client.get(reverse("kysely:indeksi"))

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
        kysymys = luo_kysymys("Mennyt kysymys.", days=-30)
        luo_kysymys("Tuleva kysymys", days=30)

        vastaus = self.client.get(reverse("kysely:indeksi"))
        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys],
        )

    def test_2_mennyttä_kysymystä(self):
        kysymys1 = luo_kysymys("Mennyt kysymys 1", days=-30)
        kysymys2 = luo_kysymys("Mennyt kysymys 2", days=-5)

        vastaus = self.client.get(reverse("kysely:indeksi"))

        self.assertQuerySetEqual(
            vastaus.context["kysymykset"],
            [kysymys2, kysymys1],
        )
