# Generated by Django 5.1.1 on 2024-09-09 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_reviews_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arrivalschedule',
            old_name='airline',
            new_name='airline_id',
        ),
        migrations.AlterUniqueTogether(
            name='arrivalschedule',
            unique_together={('arrival_time',)},
        ),
        migrations.AddField(
            model_name='arrivalschedule',
            name='route',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='arrivalschedule',
            name='arrival_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='arrivalschedule',
            name='flight_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterModelTable(
            name='arrivalschedule',
            table=None,
        ),
        migrations.RemoveField(
            model_name='arrivalschedule',
            name='departure_location',
        ),
    ]