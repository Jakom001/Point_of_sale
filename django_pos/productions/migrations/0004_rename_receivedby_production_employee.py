# Generated by Django 4.2.1 on 2023-05-11 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0003_alter_sector_options_alter_production_sector'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='receivedby',
            new_name='employee',
        ),
    ]
