# Generated by Django 5.0.2 on 2024-02-15 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_sale_end_remove_product_sale_start_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Category',
            new_name='category',
        ),
    ]
