from multiprocessing.connection import Client
from unicodedata import category
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

from clients.models import Company


# Create your models here.
PRODUCT_STATUS = (
    ("Shelf", "Shelf"),
    ("Ordered", "Ordered"),
    ("Pick up room", "Pick up room"),
    ("In transit", "In transit"),
    ("Delivered", "Delivered"),
    ("Return initiated", "Return initiated")
)

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class Crate(models.Model):
    status = models.CharField(max_length=30, choices=PRODUCT_STATUS, default="Shelf")
    client = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    crate_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    delivery_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    return_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('crate_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.crate_name


class Item(models.Model):
    crate = models.ForeignKey(Crate, on_delete=models.CASCADE, null=True, related_name="item_storage")
    change_crate = models.ForeignKey(Crate, on_delete=models.CASCADE, null=True, related_name="change_item_location")
    status = models.CharField(max_length=30, choices=PRODUCT_STATUS, default="Shelf")
    client = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    delivery_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    return_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('item_detail', args=[self.category.slug, self.crate.slug, self.slug])

    def clean(self):
        if self.category.category_name != self.crate.category.category_name:
            raise ValidationError("Item Category should be " + self.crate.category.category_name)

    def __str__(self):
        return self.item_name

