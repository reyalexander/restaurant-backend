from django.db import models
from apps.ticket.models import Ticket
from apps.product.models import Product


class TicketDetail(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ticket Detalle"
        verbose_name_plural = "Detalles de los Ticket"
        ordering = ["id"]

    def __str__(self):
        return f"{self.ticket_id} - {self.product_id.name} ({self.quantity})"
