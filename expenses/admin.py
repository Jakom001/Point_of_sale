from django.contrib import admin
from .models import Expense, Group, Capital

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'group', 'date_added', 'description')
    ordering = ('-id',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description', 'status')
    ordering = ('-id',)

class CapitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'source', 'date_added', 'description')
    ordering = ('-id',)

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Capital, CapitalAdmin)