from django.contrib import admin
from .models import Sale, SaleDetail

class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'customer', 'sub_total', 'grand_total', 'tax_amount', 'tax_percentage', 'amount_payed', 'amount_change')
    ordering = ('-id',)

class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'price', 'quantity', 'total_detail')
    ordering = ('-id',)  

admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)