# Generated by Django 3.2 on 2023-07-01 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
    ]
