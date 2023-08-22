from django.db import models
from apps.product_type.models import ProductType 

class Product(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )
    name = models.CharField(max_length=70, blank=True)
    description = models.TextField(null=True, default=None)
    id_typeproduct = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_type_image = models.ImageField(upload_to='product_type', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)


    class Meta:
        ordering = ['-id']