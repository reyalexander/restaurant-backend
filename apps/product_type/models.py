from django.db import models

class ProductType(models.Model):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )
    name = models.CharField(max_length=70, blank=True)
    description = models.TextField(null=True, default=None)
    product_image = models.ImageField(upload_to='products', blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['-id']