# Generated by Django 4.2.1 on 2023-05-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_saledetail_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saledetail',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
