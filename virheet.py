"""
Esimerkki virheiden käsittelystä.

Tutkitaan esimerkin avulla miten virheiden käsittely Pythonissa toimii.
Havainnollistaa miten tapahtuu poikkeuksen (Exception) nostaminen
(raise) ja ottaminen kiinni (try-except:llä).
"""

vaihtoehto = 5  # ks. koodi alla mitä eri vaihtoehdot ovat

class Virhe(Exception):
    pass


def main():
    try:
        onko_pouta = onko_huomenna_pouta()
    except Virhe as v:
        print("Tapahtui virhe sään hakemisessa:", v)
        return

    if onko_pouta:
        print("Huomenna on pouta")
    else:
        print("Huomenna ei ole pouta")


def onko_huomenna_pouta():
    sää = hae_sää_netistä()
    if sää == "pouta":
        return True
    else:
        return False


def hae_sää_netistä():
    kaupunki = hae_nykyinen_kaupunki()
    try:
        tulos = lähetä_kysely_web_palvelimelle(
            f"https://ilmatieteenlaitos.fi/{kaupunki}"
        )
    except IOError:
        tulos = {}
    if "sää" not in tulos:
        raise Virhe("Säätä ei löydy")
    return tulos["sää"]


def hae_nykyinen_kaupunki():
    return "Raisio"


def lähetä_kysely_web_palvelimelle(osoite):
    # Oikea kysely voisi olla tämän tyylinen...
    #vastaus = requests.post(osoite)

    # mutta ei tehdä oikeaa kyselyä tässä esimerkissä vaan simuloidaan
    # erilaisia vastauksia
    print("Lähetetään muka web-kysely osoitteeseen:", osoite)

    if vaihtoehto == 1:  # Pouta
        vastaus = {"sää": "pouta"}
    elif vaihtoehto == 2: # Muu sää
        vastaus = {"sää": "sadetta"}
    elif vaihtoehto == 3: # Virhevastaus palvelusta
        vastaus = {"virhe": "säätiedot eivät saatavilla"}
    elif vaihtoehto == 4:
        # Virhe sään hakemisessa. Simuloidaan virhetilannetta, joka
        # oikeassa koodissa voisi tapahtua requests.post-kutsun sisällä
        raise IOError("HTTP request failed")
    elif vaihtoehto == 5:
        # Ohjelmointivirhe. Koodissa on jokin virhe jota ei pitäisi
        # käsitellä.  Tässä tapauksessa käytetään funktiota
        # "lähetä_kysely", jota ei ole olemassa
        lähetä_kysely(osoite)

    return vastaus


if __name__ == "__main__":
    main()
