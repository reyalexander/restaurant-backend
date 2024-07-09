from django.db import models
from apps.company.models import Company


class ProductType(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="CompanyTypeProduct",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=70, blank=True, verbose_name="Nombre")
    description = models.TextField(null=True, default=None, verbose_name="Descripcion")
    product_image = models.ImageField(
        upload_to="product_type", blank=True, null=True, verbose_name="Imagen"
    )
    is_publish = models.BooleanField(default=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Tipo de Productos"
        verbose_name_plural = "Tipos de Productos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id} -  {self.name}"
