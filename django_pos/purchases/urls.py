from django.urls import path

from . import views

app_name = "purchases"
urlpatterns = [
    # List purchases
    path('', views.PurchasesListView, name='purchases_list'),
    # Add purchase
    path('add', views.PurchasesAddView, name='purchases_add'),
    # Details purchase
    path('details/<str:purchase_id>',
         views.PurchasesDetailsView, name='purchases_details'),
    # purchase receipt PDF
    path("pdf/<str:purchase_id>",
         views.ReceiptPDFView, name="purchases_receipt_pdf"),
]
