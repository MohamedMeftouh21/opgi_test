# Generated by Django 3.2 on 2023-07-01 23:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification_chef_service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.unite')),
            ],
        ),
        migrations.CreateModel(
            name='MontantMensuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.PositiveIntegerField()),
                ('annee', models.PositiveIntegerField()),
                ('total', models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0, message='La valeur doit être supérieure ou égale à 0')])),
                ('total_of_month', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, message='La valeur doit être supérieure ou égale à 0')])),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.unite')),
            ],
            options={
                'unique_together': {('unite', 'annee', 'mois')},
            },
        ),
    ]
