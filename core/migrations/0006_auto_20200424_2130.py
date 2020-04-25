# Generated by Django 3.0.5 on 2020-04-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200421_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='item'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='carbohydrates',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='energy_value',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='fats',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='proteins',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='weight',
            field=models.IntegerField(),
        ),
    ]