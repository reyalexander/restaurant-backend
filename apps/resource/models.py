from django.db import models

class Resource(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )
    name = models.CharField(max_length=100, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']