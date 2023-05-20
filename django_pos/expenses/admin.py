from django.contrib import admin


from .models import Expense, Group, Capital

admin.site.register(Expense)
admin.site.register(Group)
admin.site.register(Capital)