# Generated by Django 4.2.2 on 2023-06-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='reading_time',
            field=models.CharField(max_length=255),
        ),
    ]
