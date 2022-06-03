from django.urls import path
from orders import views


# Create your views here.

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('return_order/<int:crate_id>/', views.return_crate, name='return_crate'),
    path('return_order_item/<int:item_id>/', views.return_item, name='return_item'),
    path('initiat_return/', views.initiat_return, name='initiat_return'),     
]