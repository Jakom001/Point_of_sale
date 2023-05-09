# Generated by Django 4.2.1 on 2023-05-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_shop_options_rename_department_employee_shop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='Active', max_length=100, verbose_name='Status of the employee'),
        ),
    ]
