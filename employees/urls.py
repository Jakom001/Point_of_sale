from django.urls import path

from . import views

app_name = "employees"
urlpatterns = [
    # List shops
    path('shops', views.ShopsListView, name='shops_list'),
    # Add shop
    path('shops/add', views.ShopsAddView, name='shops_add'),
    # Update shop
    path('shops/update/<str:shop_id>',
         views.ShopsUpdateView, name='shops_update'),
    # Delete shop
    path('shops/delete/<str:shop_id>',
         views.ShopsDeleteView, name='shops_delete'),

    # List employees
    path('', views.EmployeesListView, name='employees_list'),
    # Add employee
    path('add', views.EmployeesAddView, name='employees_add'),
    # Update employee
    path('update/<str:employee_id>',
         views.EmployeesUpdateView, name='employees_update'),
    # Delete employee
    path('delete/<str:employee_id>',
         views.EmployeesDeleteView, name='employees_delete'),
    
]

