from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Refuel, Pump, Tank
from reportlab.pdfgen import canvas
from django.db.models import Sum
from babel.numbers import format_currency
from rest_framework import viewsets
from .serializers import TankSerializer, PumpSerializer, RefuelSerializer
from decimal import Decimal, DecimalException
from django.utils import timezone


def register_refuel(request):
    tanks = Tank.objects.all()
    return render(request, 'gas_filling/register_refuel.html', {'tanks': tanks})

@csrf_exempt
def load_pumps(request):
    tank_id = request.POST.get('tank_id')
    pumps = Pump.objects.filter(tank_id=tank_id)
    pump_list = [{'id': pump.id, 'name': pump.name} for pump in pumps]
    return JsonResponse(pump_list, safe=False)

@csrf_exempt
def save_refuel(request):
    pump_id = request.POST.get('pump_id')
    liters = request.POST.get('liters')
    amount = request.POST.get('amount')

    cleaned_amount = ''.join(char for char in amount if char.isdigit() or char == '.')

    try:
        decimal_amount = Decimal(cleaned_amount)
    except DecimalException:
        return JsonResponse({'status': 'error', 'message': 'Valor inválido'}, status=400)

    tax = decimal_amount * Decimal('0.13')

    try:
        Refuel.objects.create(pump_id=pump_id, liters=liters, amount=decimal_amount, tax=tax)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'success'})

def download_report(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = timezone.make_aware(timezone.datetime.strptime(start_date_str, '%Y-%m-%d'))
        end_date = timezone.make_aware(timezone.datetime.strptime(end_date_str, '%Y-%m-%d'))
    except ValueError:
        return HttpResponse("Formato de data inválido", status=400)

    refuels = Refuel.objects.filter(refuel_date__date__range=(start_date, end_date))
    total = refuels.aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_tax = refuels.aggregate(Sum('tax'))['tax__sum'] or 0.00


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{start_date_str}_{end_date_str}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    title_text = f"Relatório de Abastecimento de {start_date_str} a {end_date_str}"
    total_text = f"Total do Período: {format_currency(total, 'BRL', locale='pt_BR')} - Total de taxas do Período: {format_currency(total_tax, 'BRL', locale='pt_BR')}"

    def draw_header(first_page):
        if first_page:
            p.drawString(60, 800, title_text)
            p.drawString(60, 780, total_text)

    first_page = True
    draw_header(first_page)


    y = 750
    for refuel in refuels:
        tank_name = refuel.pump.tank.name
        formatted_amount = format_currency(refuel.amount, 'BRL', locale='pt_BR')
        formatted_tax = format_currency(refuel.tax, 'BRL', locale='pt_BR')
        formatted_liters = refuel.liters_formatted()
        formatted_refuel_date = refuel.refuel_date.astimezone(timezone.get_current_timezone()).strftime('%d/%m/%Y %H:%M')

        text_lines = [
            f"Dia: {formatted_refuel_date}",
            f"Tanque: {tank_name}",
            f"Bomba: {refuel.pump.name}",
            f"Litros: {formatted_liters}",
            f"Valor: {formatted_amount}",
            f"Taxa: {formatted_tax}"
        ]

        for line in text_lines:
            if y < 60:
                p.showPage()
                draw_header(first_page)
                y = 750
            p.drawString(60, y, line)
            y -= 15

        y -= 10

    p.showPage()
    p.save()

    return response

class TankViewSet(viewsets.ModelViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer

class PumpViewSet(viewsets.ModelViewSet):
    queryset = Pump.objects.all()
    serializer_class = PumpSerializer

class RefuelViewSet(viewsets.ModelViewSet):
    queryset = Refuel.objects.all()
    serializer_class = RefuelSerializer

