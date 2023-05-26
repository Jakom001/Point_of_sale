from django.contrib import admin
from .models import Purchase, PurchaseDetail

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'supplier', 'sub_total', 'grand_total', 'tax_amount', 'tax_percentage', 'amount_payed', 'amount_change')
    ordering = ('-id',)

class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'product', 'price', 'quantity', 'weight', 'total_detail')
    ordering = ('-id',)  

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail, PurchaseDetailAdmin)