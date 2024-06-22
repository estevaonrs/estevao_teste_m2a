# Generated by Django 5.0.6 on 2024-06-20 23:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gas_filling', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pump',
            options={'verbose_name': 'Bomba', 'verbose_name_plural': 'Bombas'},
        ),
        migrations.AlterModelOptions(
            name='refuel',
            options={'verbose_name': 'Abastecimento', 'verbose_name_plural': 'Abastecimentos'},
        ),
        migrations.AlterModelOptions(
            name='tank',
            options={'verbose_name': 'Tanque', 'verbose_name_plural': 'Tanques'},
        ),
        migrations.AlterField(
            model_name='pump',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pump',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome da Bomba'),
        ),
        migrations.AlterField(
            model_name='pump',
            name='tank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pumps', to='gas_filling.tank', verbose_name='Tanque'),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='liters',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Litros'),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='pump',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refuels', to='gas_filling.pump', verbose_name='Bomba'),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='refuel_date',
            field=models.DateField(auto_now_add=True, verbose_name='Data de Abastecimento'),
        ),
        migrations.AlterField(
            model_name='refuel',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Taxa'),
        ),
        migrations.AlterField(
            model_name='tank',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tank',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nome do Tanque'),
        ),
    ]
