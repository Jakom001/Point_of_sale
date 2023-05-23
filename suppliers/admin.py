from django.contrib import admin
from .models import Supplier

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'name', 'contact_person', 'address', 'email', 'phone')
    ordering = ('-id',)

admin.site.register(Supplier, SupplierAdmin)