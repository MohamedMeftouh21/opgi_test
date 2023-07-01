# Generated by Django 3.2 on 2023-07-01 16:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recouvrement', '0002_auto_20230701_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='montantmensuel',
            name='total',
            field=models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0, message='La valeur doit être supérieure ou égale à 0')]),
        ),
        migrations.AlterField(
            model_name='montantmensuel',
            name='total_of_month',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, message='La valeur doit être supérieure ou égale à 0')]),
        ),
    ]