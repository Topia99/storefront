# Generated by Django 4.2.5 on 2023-10-06 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_collection_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['first_name', 'last_name']},
        ),
    ]