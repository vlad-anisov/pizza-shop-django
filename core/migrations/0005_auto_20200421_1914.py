# Generated by Django 3.0.5 on 2020-04-21 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200421_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='carbohydrates',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='energy_value',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='fats',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='proteins',
            field=models.FloatField(default=1),
        ),
    ]