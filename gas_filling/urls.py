from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'gas_filling'

router = DefaultRouter()
router.register(r'tanks', views.TankViewSet)
router.register(r'pumps', views.PumpViewSet)
router.register(r'refuels', views.RefuelViewSet)

urlpatterns = [
    path('', views.register_refuel, name='register_refuel'),
    path('load_pumps/', views.load_pumps, name='load_pumps'),
    path('save_refuel/', views.save_refuel, name='save_refuel'),
    path('download-report/', views.download_report, name='download_report'),
    path('api/', include(router.urls)),
]