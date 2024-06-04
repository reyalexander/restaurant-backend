from django.db import models


# Create your models here.
class Company(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    name = models.CharField(
        max_length=70, blank=True, verbose_name="Nombre de la Compañia"
    )
    description = models.TextField(
        null=True, blank=True, default=None, verbose_name="descripcion de la Compañia"
    )
    ruc = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="ruc de la Compañia"
    )
    company_image = models.ImageField(
        upload_to="company", blank=True, null=True, verbose_name="Imagen de la Compañia"
    )
    address = models.CharField(
        max_length=120, null=True, blank=True, verbose_name="Direccion de la Compañia"
    )
    phone_principal = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="Telefono de la Compañia"
    )
    phone_secundary = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name="Telefono Secundario de la Compañia",
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compañia"
        verbose_name_plural = "Compañias"
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}. {self.name}"
