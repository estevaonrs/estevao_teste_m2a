# Generated by Django 5.0.6 on 2024-06-19 19:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pump',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Refuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liters', models.DecimalField(decimal_places=2, max_digits=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('refuel_date', models.DateField(auto_now_add=True)),
                ('pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refuels', to='gas_filling.pump')),
            ],
        ),
        migrations.AddField(
            model_name='pump',
            name='tank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pumps', to='gas_filling.tank'),
        ),
    ]
