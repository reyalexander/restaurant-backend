from django.db import models


class Table(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )

    name = models.CharField(max_length=70, blank=True)
    number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
