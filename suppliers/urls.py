from django.urls import path

from . import views

app_name = "suppliers"
urlpatterns = [
    # List suppliers
    path('', views.SuppliersListView, name='suppliers_list'),
    # Add supplier
    path('add', views.SuppliersAddView, name='suppliers_add'),
    # Update supplier
    path('update/<str:supplier_id>',
         views.SuppliersUpdateView, name='suppliers_update'),
    # Delete supplier
    path('delete/<str:supplier_id>',
         views.SuppliersDeleteView, name='suppliers_delete'),
]
