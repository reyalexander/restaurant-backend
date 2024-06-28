from django.db import models
from apps.product.models import Product
from apps.company.models import Company


# Create your models here.
class Menu(models.Model):
    STATUS_CHOICES = (
        (1, "Activo"),
        (2, "Inactivo"),
        (3, "Eliminado"),
    )
    DAY_CHOICES = (
        (0, "Todos los dias"),
        (1, "Lunes"),
        (2, "Martes"),
        (3, "Miercoles"),
        (4, "Jueves"),
        (5, "Viernes"),
        (6, "Sabado"),
        (7, "Domingo"),
    )
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="CompanyMenu",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    starters = models.ManyToManyField(
        Product, related_name="menus_entradas", blank=True
    )
    main_courses = models.ManyToManyField(
        Product, related_name="menus_productos", blank=True
    )
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES, default=1)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0, verbose_name="Precio s/"
    )
    description = models.TextField(null=True, default=None, verbose_name="Descripcion")
    is_publish = models.BooleanField(default=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
