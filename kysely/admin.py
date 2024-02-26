from django.contrib import admin

from .models import Kysymys, Vaihtoehto


class VastausvaihtoehtoInline(admin.TabularInline):
    model = Vaihtoehto
    extra = 3


@admin.register(Kysymys)
class KysymysAdmin(admin.ModelAdmin):
    date_hierarchy = "julkaisupvm"
    fieldsets = [
        ("Päivämäärätiedot", {"fields": ["julkaisupvm"]}),
        ("Sisältö", {"fields": ["teksti"]}),
    ]
    inlines = [VastausvaihtoehtoInline]
    list_display = ["teksti", "julkaisupvm", "onko_julkaistu_lähiaikoina"]
    search_fields = ["teksti"]


@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
    search_fields = ["teksti", "kysymys__teksti"]
    autocomplete_fields = ["kysymys"]
