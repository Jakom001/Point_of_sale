from django.db import models
import django.utils.timezone


# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Xcategory', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # Table's name
        db_table = "Expense"
        verbose_name_plural = "expenses"

    def __str__(self) -> str:
        return self.name
    

class Xcategory(models.Model):
    STATUS_CHOICES = (  # new
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive")
    )

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=100,
        verbose_name="Status of the xcategory",
    )

    class Meta:
        # Table's name
        db_table = "Xcategory"
        verbose_name_plural = "xCategories"

    def __str__(self) -> str:
        return self.name



class Capital(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=django.utils.timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        # Table's name
        db_table = "Capital"
        verbose_name_plural = "capitals"

    def __str__(self) -> str:
        return self.source

