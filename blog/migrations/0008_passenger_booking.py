# Generated by Django 5.1.1 on 2024-09-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_flight_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='booking',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
