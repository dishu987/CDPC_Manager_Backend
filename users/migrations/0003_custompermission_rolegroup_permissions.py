# Generated by Django 4.2.2 on 2023-06-21 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_usermodel_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('codename', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='rolegroup',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='permissions', null=True, to='users.custompermission'),
        ),
    ]
