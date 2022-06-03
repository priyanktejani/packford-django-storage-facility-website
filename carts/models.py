from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

from django.db import models
from accounts.models import User
from inventory.models import Crate, Item


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def clean(self):
        """Ensure that one of two field can be true from Product, Item"""
        if self.crate and self.item:
            raise ValidationError("both product and Item can't be null")

    def crate_sub_total(self):
        return self.crate.delivery_price * self.quantity

    def item_sub_total(self):
        return self.item.delivery_price * self.quantity

    def __str__(self):
        return str(self.user)