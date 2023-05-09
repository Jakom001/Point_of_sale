from django.contrib import admin


from .models import Expense, Xcategory, Capital

admin.site.register(Expense)
admin.site.register(Xcategory)
admin.site.register(Capital)