# Generated by Django 3.2.5 on 2021-08-26 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_table_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonloginuser',
            name='allowed',
            field=models.CharField(blank=True, default='allowed', max_length=256, null=True, verbose_name='アクセス制限'),
        ),
    ]