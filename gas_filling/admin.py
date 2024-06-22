from django.contrib import admin
from .models import Tank, Pump, Refuel

@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tank')
    search_fields = ('name', 'tank__name')
    list_filter = ('tank',)
    ordering = ('name',)

@admin.register(Refuel)
class RefuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'pump', 'liters_formatted', 'amount_display', 'tax_display', 'refuel_date')
    search_fields = ('pump__name', 'liters', 'amount')
    list_filter = ('pump', 'refuel_date')
    ordering = ('-refuel_date',)

 
