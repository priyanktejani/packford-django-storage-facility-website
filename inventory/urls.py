from django.urls import path
from inventory import views


# Create your views here.

urlpatterns = [
    path('category/<slug:category_slug>/<slug:crate_slug>/', views.crate_detail, name='crate_detail'),
    path('category/<slug:category_slug>/<slug:crate_slug>/<slug:item_slug>/', views.item_detail, name='item_detail'),
    path('crate/<slug:crate_slug>/add_item/', views.add_item, name='add_item'),
    path('category/<slug:category_slug>/<slug:crate_slug>/remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]