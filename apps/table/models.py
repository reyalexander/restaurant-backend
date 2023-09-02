from django.db import models

class Table(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )

    RESERVATION_CHOICES = (
        (1, 'Sin reserva'),
        (2, 'Reservado'),
    )
    
    reservation = models.PositiveSmallIntegerField(choices=RESERVATION_CHOICES, default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
