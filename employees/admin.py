from django.contrib import admin
from .models import Shop, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'hire_date', 'first_name', 'last_name', 'salary', 'email', 'phone', 'shop')
    ordering = ('-id',)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'name', 'manager', 'location', 'description', 'status')
    ordering = ('-id',)

admin.site.register(Shop, ShopAdmin)
admin.site.register(Employee, EmployeeAdmin)