from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from datetime import datetime, date
import django.utils.timezone



class Supplier(models.Model):
    name = models.CharField(max_length=256)
    contact_person = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'Suppliers'

    def __str__(self):
        return self.name
    
