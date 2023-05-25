import django.utils.timezone
from django.db import models
from suppliers.models import Supplier
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.

class Purchase(models.Model):
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    supplier = models.ForeignKey(
        Supplier, models.DO_NOTHING, db_column='supplier')
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)
    amount_payed = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)

    class Meta:
        db_table = 'Purchases'

    def __str__(self) -> str:
        return "Purchase ID: " + str(self.id) + " | Grand Total: " + str(self.grand_total) + " | Datetime: " + str(self.date_added)

    def sum_items(self):
        details = PurchaseDetail.objects.filter(purchase=self.id)
        return sum([d.quantity for d in details])


class PurchaseDetail(models.Model):

    purchase = models.ForeignKey(
        Purchase, models.DO_NOTHING, db_column='purchase')
    product = models.ForeignKey(
        Product, models.DO_NOTHING, db_column='product')
    price = models.FloatField()
    weight = models.IntegerField(default=0)
    quantity = models.IntegerField()
    total_detail = models.FloatField()
    
    class Meta:
        db_table = 'PurchaseDetails'

    def __str__(self) -> str:
        return "Detail ID: " + str(self.id) + " Purchase ID: " + str(self.purchase.id) + " Quantity: " + str(self.quantity) + " Weight: " + str(self.weight)