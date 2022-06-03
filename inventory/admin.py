from django.contrib import admin
from .models import Category, Crate, Item

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class CrateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('crate_name',)}

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('item_name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Crate, CrateAdmin)
admin.site.register(Item, ItemAdmin)

