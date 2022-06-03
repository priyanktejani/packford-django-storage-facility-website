from django.urls import path
from adminpackford import views

urlpatterns = [
    path('dashboard/packford/', views.dasboard_packford, name='dasboard_packford'),
    path('dashboard/sales/add_company', views.add_company, name='add_company'),
    path('dashboard/company_detail/<int:company_id>/', views.company_detail, name='company_detail'),
    path('dashboard/sales/add_branch/<int:company_id>/', views.add_branch, name='add_branch'),
    path('dashboard/company_detail/<int:company_id>/branch_detail/<int:branch_id>/', views.branch_detail, name='branch_detail'),
    path('dashboard/sales/add_employee/company/<int:company_id>', views.add_company_employee, name='add_company_employee'),
    path('dashboard/sales/add_employee/company/<int:company_id>/branch/<int:branch_id>', views.add_branch_employee, name='add_branch_employee'),
    path('dashboard/packford/all_orders', views.all_order, name='all_order'),
    path('dashboard/packford/all_returns', views.all_return, name='all_returns'),
    path('dashboard/packford/change_item_location', views.change_item_location, name='change_item_location'),
]