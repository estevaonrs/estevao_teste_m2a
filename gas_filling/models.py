from django.db import models
from babel.numbers import format_currency, format_decimal

class Tank(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Tanque", blank=False, null=False)

    def __str__(self):
        return self.name

class Pump(models.Model):
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE, related_name='pumps', verbose_name="Tanque", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="Nome da Bomba", blank=False, null=False)

    def __str__(self):
        return self.name

class Refuel(models.Model):
    pump = models.ForeignKey('Pump', on_delete=models.CASCADE, related_name='refuels', verbose_name="Bomba", blank=False, null=False)
    liters = models.FloatField(verbose_name="Litros", blank=False, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor", blank=False, null=False)
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Taxa", blank=False, null=False)
    refuel_date = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora de Abastecimento", blank=False, null=False)

    class Meta:
        verbose_name = "Abastecimento"
        verbose_name_plural = "Abastecimentos"
        ordering = ['-refuel_date']

    def __str__(self):
        return f"{self.pump.name} - {self.liters_formatted()} L - {self.format_amount(self.amount)} R$"

    def format_amount(self, amount):
        return format_currency(amount, 'BRL', locale='pt_BR')

    def liters_formatted(self):
        return format_decimal(self.liters, format='#,##0.00', locale='pt_BR')

    def amount_display(self):
        return self.format_amount(self.amount)
    
    def tax_display(self):
        return self.format_amount(self.tax)

    amount_display.short_description = 'Valor Formatado'
    tax_display.short_description = 'Taxa Formatada'
    liters_formatted.short_description = 'Litros Formatados'
