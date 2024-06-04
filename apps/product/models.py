from django.db import models
from apps.product_type.models import ProductType
from apps.company.models import Company


class Product(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="CompanyProduct",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=70, blank=True, verbose_name="Nombre")
    description = models.TextField(null=True, default=None, verbose_name="Nombre")
    id_typeproduct = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, verbose_name="Tipo de Producto"
    )
    product_type_image = models.ImageField(
        upload_to="product_type", blank=True, null=True, verbose_name="Imagen"
    )
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, verbose_name="Precio s/"
    )
    discount = models.IntegerField(default=0, verbose_name="descuento en %")
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["id"]
