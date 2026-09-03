from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class UserInteraction(models.Model):

    INTERACTION_TYPES = [
        ("VIEW", "View"),
        ("CART", "Cart"),
        ("WISHLIST", "Wishlist"),
        ("PURCHASE", "Purchase"),
        ("RATING", "Rating"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    session_key = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.user:
            username = self.user.username
        else:
            username = "Anonymous"

        return f"{username} - {self.product.name} - {self.interaction_type}"