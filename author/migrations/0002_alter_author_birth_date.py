# Generated by Django 4.2 on 2023-04-30 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='birth_date',
            field=models.CharField(max_length=10),
        ),
    ]
