# Generated by Django 4.2.5 on 2023-10-06 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_item_orderitem_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
    ]
