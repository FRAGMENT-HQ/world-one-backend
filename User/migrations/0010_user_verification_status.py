# Generated by Django 5.0.2 on 2024-07-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_user_otp_alter_user_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_status',
            field=models.BooleanField(default=False),
        ),
    ]
