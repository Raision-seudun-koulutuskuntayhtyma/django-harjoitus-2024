from django.contrib import admin

from .models import Kysymys, Vaihtoehto

admin.site.register(Kysymys)

@admin.register(Vaihtoehto)
class VaihtoehtoAdmin(admin.ModelAdmin):
    list_display = ["kysymys", "teksti"]
