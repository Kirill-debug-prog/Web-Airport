# Generated by Django 5.1.1 on 2024-09-10 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_airline_arrivalschedule_airline_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]