from django.db import models


class Kysymys(models.Model):
    teksti = models.CharField(max_length=200)
    julkaisupvm = models.DateTimeField("julkaistu")

    class Meta:
        verbose_name = "kysymys"
        verbose_name_plural = "kysymykset"

    def __str__(self):
        return self.teksti


class Vaihtoehto(models.Model):
    kysymys = models.ForeignKey(Kysymys, on_delete=models.CASCADE)
    teksti = models.CharField(max_length=200)
    ääniä = models.IntegerField(default=0)

    class Meta:
        verbose_name = "vaihtoehto"
        verbose_name_plural = "vaihtoehdot"

    def __str__(self):
        return self.teksti
