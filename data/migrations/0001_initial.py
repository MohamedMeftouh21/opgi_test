# Generated by Django 4.1.7 on 2023-04-30 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_Batiment', models.CharField(max_length=120)),
                ('nb_logts', models.PositiveIntegerField()),
                ('nb_etage', models.PositiveIntegerField()),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_cnt', models.DateTimeField(null=True)),
                ('date_strt_loyer', models.DateTimeField(null=True)),
                ('loyer', models.FloatField()),
                ('charge', models.CharField(max_length=120)),
                ('mnt_tva', models.FloatField()),
                ('total_of_month', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'data_contrat',
            },
        ),
        migrations.CreateModel(
            name='Occupant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oc_id', models.PositiveIntegerField(unique=True)),
                ('nom_oc', models.CharField(max_length=120)),
                ('prenom_oc', models.CharField(max_length=120)),
                ('date_naiss', models.DateTimeField(null=True)),
                ('lieu_naiss', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'data_occupant',
            },
        ),
        migrations.CreateModel(
            name='wilaya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_wilaya', models.CharField(max_length=120)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
            ],
            options={
                'db_table': 'data_wilaya',
            },
        ),
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_unit', models.CharField(max_length=120)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.wilaya')),
            ],
            options={
                'db_table': 'data_unite',
            },
        ),
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.FloatField(default='m2')),
                ('prix_logement', models.FloatField()),
                ('type_logement', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.batiment')),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.contrat')),
            ],
            options={
                'db_table': 'data_logement',
            },
        ),
        migrations.AddField(
            model_name='contrat',
            name='occupant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.occupant'),
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total', models.FloatField()),
                ('logement', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.logement')),
                ('occupant', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.occupant')),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.unite')),
            ],
            options={
                'db_table': 'data_consultation',
            },
        ),
        migrations.CreateModel(
            name='Cite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_Cite', models.CharField(max_length=120)),
                ('nb_logts', models.PositiveIntegerField()),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.unite')),
            ],
            options={
                'db_table': 'data_cite',
            },
        ),
        migrations.AddField(
            model_name='batiment',
            name='Cite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET, to='data.cite'),
        ),
    ]
