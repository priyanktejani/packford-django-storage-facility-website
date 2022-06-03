from django.db import models
from django.forms import ValidationError
from accounts.models import *
from inventory.models import *
from clients.models import *

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    company_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='billing_address')
    branch_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shipping_address')
    order_number = models.CharField(max_length=20)
    tax = models.FloatField()
    order_total = models.FloatField()
    monthly_charge = models.FloatField(null=True, blank=True)
    schedule = models.CharField(max_length=10, blank=True, null=True)
    schedule_duration = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    is_ordered = models.BooleanField(default=False)
    return_requested = models.BooleanField(default=False)
    delivery_date: models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class Return(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    return_number = models.CharField(max_length=20)
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    tax = models.FloatField()
    return_total = models.FloatField()
    pickup_date = models.DateField()
    returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.return_number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Ensure that one of two field can be true from Product, Item"""
        if self.crate and self.item:
            raise ValidationError("both product and Item can't be added")

    def __str__(self):
        return self.user.username
