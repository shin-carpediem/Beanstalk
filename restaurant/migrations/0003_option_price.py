# Generated by Django 3.2.5 on 2021-08-15 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20210815_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='価格'),
        ),
    ]