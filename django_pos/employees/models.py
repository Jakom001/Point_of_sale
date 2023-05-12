from django.db import models
import django.utils.timezone

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    hire_date = models.DateTimeField(default=django.utils.timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Employees'

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
    

class Shop(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=50)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_department')
    location = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the shop",
    )
    class Meta:
        # Table's name
        db_table = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self) -> str:
        return self.name