from django.db import models
from apps.user.models import User


class Reservation(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuario"
    )
    date = models.DateField(null=True, blank=True, verbose_name="Fecha de Reserva")
    hour = models.TimeField(null=True, verbose_name="Hora de Reserva")
    name = models.CharField(
        max_length=70, blank=True, verbose_name="Nombre del Reservista"
    )
    number_person = models.IntegerField(
        null=True, default=0, verbose_name="Numero de personas"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Descripcion de la Reserva"
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    # estado del usuario
    created = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="fecha de actualización")

    class Meta:
        verbose_name = "Reserva de Mesa"
        verbose_name_plural = "Reservas de Mesas"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} - Reserva para el: {self.date}, a las {self.hour}"

    def delete(self):
        self.status = 3
        self.save()
