from django.urls import path
from clients import views


urlpatterns = [
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/order_crate/', views.order_crate, name='order_crate'),
    path('dashboard/list_order', views.list_order, name='list_order'),
    path('dashboard/order_details/<int:order_id>', views.order_details, name='order_details'),
    path('dashboard/list_return', views.list_return, name='list_return'),
    path('dashboard/return_details/<int:return_id>', views.return_details, name='return_details'),
]