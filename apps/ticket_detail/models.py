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

    is_menu = models.BooleanField(default=True, null=True, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, verbose_name="Precio Total"
    )
    quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ticket Detalle"
        verbose_name_plural = "Detalles de los Ticket"
        ordering = ["id"]

    def __str__(self):
        return f"{self.ticket_id} -  ({self.quantity})"
