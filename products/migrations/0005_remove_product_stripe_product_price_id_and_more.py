# Generated by Django 4.1.7 on 2023-03-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_stripe_product_price_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stripe_product_price_id',
        ),
        migrations.AddField(
            model_name='basket',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]