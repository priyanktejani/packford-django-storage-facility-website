from pyexpat import model
from django.contrib import admin
from clients.models import Branch, Company, Location
from orders.models import OrderProduct

# Register your models here.

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Location)

