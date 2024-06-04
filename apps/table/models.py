from django.db import models
from apps.company.models import Company


class Table(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="CompanyTable",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=70, blank=True, verbose_name="Nombre")
    number = models.IntegerField(
        null=True, blank=True, verbose_name="Maximo de personas"
    )
    description = models.TextField(null=True, default=None, verbose_name="Nombre")
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ["id"]
