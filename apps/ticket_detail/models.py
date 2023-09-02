from django.db import models
from apps.ticket.models import Ticket
from apps.product.models import Product

class TicketDetail(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )
    ticket_id = models.ForeignKey(Ticket, on_delete= models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    quantity = models.IntegerField(null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete= models.CASCADE)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']