from django.db import models
from products.models import Product
from employees.models import Employee
from django.forms import model_to_dict


# Create your models here.
class Sector(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the sector",
    )

    class Meta:
        # Table's name
        db_table = "Sector"
        verbose_name_plural = "Sectors"

    def __str__(self) -> str:
        return self.name
    
class Production(models.Model):
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='product')
    quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    receivedby = models.ForeignKey(
        Employee, models.DO_NOTHING, db_column='employee')
    quantity = models.IntegerField()
    sector = models.ForeignKey(
        Sector, related_name="sector", on_delete=models.CASCADE, db_column='Sector')    
    description = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    class Meta:
        # Table's name
        db_table = "Production"

    def __str__(self) -> str:
        return self.product
    def to_json(self):
        item = model_to_dict(self)
        item['id'] = self.id
        item['sector'] = self.sector.name
        item['quantity'] = 1
        item['total_production'] = 0
        return item