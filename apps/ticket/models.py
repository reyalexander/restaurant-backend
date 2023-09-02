from django.db import models
from apps.user.models import User
from apps.table.models import Table

class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )
    local_name = models.CharField(max_length=70, blank=True)
    ruc = models.CharField(max_length=10, null=False)
    discount = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    user_id = models.ForeignKey(User, on_delete= models.CASCADE)
    table_id = models.ForeignKey(Table, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['-id']