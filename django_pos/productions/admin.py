from django.contrib import admin


from .models import Sector, Production

admin.site.register(Sector)
admin.site.register(Production)