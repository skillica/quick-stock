from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        blank=True,
        related_name="orders",
    )

    customer_name = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.PositiveIntegerField(default=0)
    sub_total = models.PositiveIntegerField(default=0)
    total_discount = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT)

    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.product.name} x {self.qty}"
