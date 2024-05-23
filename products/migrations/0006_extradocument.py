import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_userquery_order_citizenship_order_purous_of_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='extra_document/')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_document', to='products.order')),
            ],
            options={
                'verbose_name': 'ExtraDocument',
                'verbose_name_plural': 'ExtraDocument',
            },
        ),
    ]
