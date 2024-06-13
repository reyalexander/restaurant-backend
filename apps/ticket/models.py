from django.db import models
from apps.user.models import User
from apps.table.models import Table
from apps.company.models import Company


class Ticket(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    code = models.CharField(max_length=150, blank=True, verbose_name="Codigo")
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="CompanyTicket",
        null=True,
        blank=True,
    )
    ruc = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="ruc/datos del cliente"
    )
    discount = models.IntegerField(null=True, blank=True, verbose_name="Descuento")
    priceTotal = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, verbose_name="Precio Total"
    )
    priceFinal = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, verbose_name="Precio Total"
    )
    check_discount = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Tiene descuento"
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=1, verbose_name="Estado"
    )
    user_id = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Usuario"
    )
    table_id = models.ForeignKey(
        Table, on_delete=models.CASCADE, null=True, verbose_name="Mesa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Boleta de Venta"
        verbose_name_plural = "Boletas de Ventas"
        ordering = ["id"]

    def __str__(self):
        return f"{self.code} - s/{self.priceFinal}"

    def generate_order_code(self):
        ticket = self.id
        self.code = f"OR-010{ticket:02d}"
        self.save(update_fields=["code"])

    def save(self, *args, **kwargs):
        if not self.code:  ### PR-0001
            super().save(
                *args, **kwargs
            )  # Guarda el objeto primero para obtener un ID asignado
            self.generate_order_code()  # Genera el código de parte después de que el objeto se haya guardado
        else:
            super().save(*args, **kwargs)

    def delete(self):
        self.status = 3
        self.save()
