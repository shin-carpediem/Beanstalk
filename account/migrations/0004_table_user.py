# Generated by Django 3.2.5 on 2021-08-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='user',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='利用人数'),
        ),
    ]