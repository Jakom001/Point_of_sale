from django.contrib import admin


from .models import Sector, Production

class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description', 'status')
    ordering = ('-id',)

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'weight', 'sector', 'total_price', 'description')
    ordering = ('-id',)


admin.site.register(Sector, SectorAdmin)
admin.site.register(Production, ProductionAdmin)