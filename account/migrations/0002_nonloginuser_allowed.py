# Generated by Django 3.2.5 on 2021-08-05 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonloginuser',
            name='allowed',
            field=models.CharField(blank=True, default='unknown', max_length=256, null=True, verbose_name='アクセス制限'),
        ),
    ]
