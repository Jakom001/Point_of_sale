from django.db import models

# Create your models here.
class production(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    receivedby = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class Category(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the category",
    )

    class Meta:
        # Table's name
        db_table = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name