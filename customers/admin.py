from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'first_name', 'last_name', 'address', 'email', 'phone')
    ordering = ('-id',)

admin.site.register(Customer, CustomerAdmin)
