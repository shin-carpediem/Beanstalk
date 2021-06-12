# Generated by Django 3.1.6 on 2021-06-10 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20210605_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='allergies',
        ),
        migrations.AddField(
            model_name='menu',
            name='allergies',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='restaurant.allergy'),
        ),
    ]