# Generated by Django 4.2.1 on 2023-05-03 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0003_remove_supplier_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
