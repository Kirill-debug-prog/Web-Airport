# Generated by Django 5.1.1 on 2024-09-08 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_reviews_reviews_review_text_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('date_of_revocation', 'review_text')},
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='passenger',
        ),
    ]
