from django.urls import path

from . import views

app_name = "productions"
urlpatterns = [
    # List sectors
    path('sectors', views.SectorsListView, name='sectors_list'),
    # Add sector
    path('sectors/add', views.SectorsAddView, name='sectors_add'),
    # Update sector
    path('sectors/update/<str:sector_id>',
         views.SectorsUpdateView, name='sectors_update'),
    # Delete sector
    path('sectors/delete/<str:sector_id>',
         views.SectorsDeleteView, name='sectors_delete'),

    # List productions
    path('', views.ProductionsListView, name='productions_list'),
    # Add product
    path('add', views.ProductionsAddView, name='productions_add'),
    # Update product
    path('update/<str:product_id>',
         views.ProductionsUpdateView, name='productions_update'),
    # Delete product
    path('delete/<str:product_id>',
         views.ProductionsDeleteView, name='productions_delete'),
    # Get productions AJAX
    path("get", views.GetProductionsAJAXView, name="get_productions"),
]
