from django.contrib import admin

from .models import Kysymys, Vaihtoehto


class VastausvaihtoehtoInline(admin.TabularInline):
    model = Vaihtoehto
    extra = 3


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Päivämäärätiedot", {"fields": ["julkaisupvm"]}),
        ("Sisältö", {"fields": ["teksti"]}),
    ]
    inlines = [VastausvaihtoehtoInline]
    list_display = ["teksti", "julkaisupvm", "onko_julkaistu_lähiaikoina"]


@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
