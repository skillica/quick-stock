from django.db import models

from .managers import ProductManager


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    # null -> db, null -> form
    sku = models.CharField(
        max_length=30, unique=True, blank=True
    )  # form -> null -> ''
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    # float, decimal
    price = models.PositiveIntegerField(db_index=True)
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=3)

    # created_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="products"
    )

    objects = ProductManager()

    # def save(self, *args, **kwargs):
    #     created = self.pk is None
    #     super().save(*args, **kwargs)

    #     if created and not self.sku:
    #         self.sku = f"{uuid.uuid4()}"[:8]
    #         super().save(update_fields=["sku"])

    def __str__(self):
        return f"{self.name} ({self.sku})"


# instragram pk -> snowflake id timestampunique
# Product.objects.in_stock()

# build -> optimized
# pagination, indexing, caching, view_caching
# HTMX
