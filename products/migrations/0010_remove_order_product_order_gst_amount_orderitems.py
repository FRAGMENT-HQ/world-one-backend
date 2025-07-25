# Generated by Django 5.0.2 on 2024-06-03 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_outlets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='gst_amount',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=40)),
                ('forex_amount', models.FloatField()),
                ('inr_amount', models.FloatField()),
                ('forex_rate', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.order')),
            ],
            options={
                'verbose_name': 'OrderItems',
                'verbose_name_plural': 'OrderItems',
            },
        ),
    ]
