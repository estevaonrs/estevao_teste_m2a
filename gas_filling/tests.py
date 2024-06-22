from django.test import TestCase
from django.urls import reverse
from .models import Pump, Refuel, Tank
from datetime import datetime


class RegisterRefuelViewTest(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Tank 1")

    def test_register_refuel_view(self):
        response = self.client.get(reverse('gas_filling:register_refuel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gas_filling/register_refuel.html')
        self.assertContains(response, self.tank.name)

class LoadPumpsViewTest(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Tank 1")
        self.pump = Pump.objects.create(name="Pump 1", tank=self.tank)

    def test_load_pumps_view(self):
        response = self.client.post(reverse('gas_filling:load_pumps'), {'tank_id': self.tank.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': self.pump.id, 'name': self.pump.name}])

class SaveRefuelViewTest(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Tank 1")
        self.pump = Pump.objects.create(name="Pump 1", tank=self.tank)

    def test_save_refuel_view(self):
        response = self.client.post(reverse('gas_filling:save_refuel'), {
            'pump_id': self.pump.id,
            'liters': '10.5',
            'amount': '50,00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
        self.assertTrue(Refuel.objects.filter(pump=self.pump).exists())

    def test_save_refuel_view_invalid_amount(self):
        response = self.client.post(reverse('gas_filling:save_refuel'), {
            'pump_id': self.pump.id,
            'liters': '10.5',
            'amount': 'invalid'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Valor inválido'})

class DownloadReportViewTest(TestCase):
    def setUp(self):
        self.tank = Tank.objects.create(name="Tank 1")
        self.pump = Pump.objects.create(name="Pump 1", tank=self.tank)
        self.refuel = Refuel.objects.create(
            pump=self.pump, liters=10.5, amount=50.00, tax=6.50,
            refuel_date=datetime.strptime('2023-01-01', '%Y-%m-%d')
        )

    def test_download_report_view(self):
        response = self.client.get(reverse('gas_filling:download_report'), {
            'start_date': '2023-01-01',
            'end_date': '2023-01-31'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

