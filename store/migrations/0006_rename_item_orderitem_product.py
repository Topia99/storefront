# Generated by Django 4.2.5 on 2023-09-12 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_customer_last_first_makeIndex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='item',
            new_name='product',
        ),
    ]