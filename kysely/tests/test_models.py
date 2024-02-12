import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import Kysymys


class KysymysModelinTestit(TestCase):
    def test_onko_julkaistu_lähiaikoina_tulevaisuuden_kysymyksellä(self):
        """
        onko_julkaistu_lähiaikoina on False jos kysymys tulevaisuudessa.
        """
        tulevaisuuden_aika = timezone.now() + datetime.timedelta(days=30)
        tuleva_kysymys = Kysymys(julkaisupvm=tulevaisuuden_aika)

        vastaus = tuleva_kysymys.onko_julkaistu_lähiaikoina()

        self.assertIs(vastaus, False)

    def test_onko_julkaistu_lähiaikoina_vanhalla_kysymyksellä(self):
        """
        onko_julkaistu_lähiaikoina False jos vanhempi kuin 1 pv
        """
        päivä_ja_yksi_sek = datetime.timedelta(days=1, seconds=1)
        yli_vuorokausi_sitten = timezone.now() - päivä_ja_yksi_sek
        vanha_kysymys = Kysymys(julkaisupvm=yli_vuorokausi_sitten)

        vastaus = vanha_kysymys.onko_julkaistu_lähiaikoina()

        self.assertIs(vastaus, False)

    def test_onko_julkaistu_lähiaikoina_tuoreella_kysymyksellä(self):
        """
        onko_julkaistu_lähiaikoina True jos tuore kysymys
        """
        alle_vuorokausi = datetime.timedelta(hours=23, minutes=59, seconds=59)
        tuore_aika = timezone.now() - alle_vuorokausi
        tuore_kysymys = Kysymys(julkaisupvm=tuore_aika)

        vastaus = tuore_kysymys.onko_julkaistu_lähiaikoina()

        self.assertIs(vastaus, True)
