from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description', 'status')
    ordering = ('-id',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'description', 'status')
    ordering = ('-id',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
