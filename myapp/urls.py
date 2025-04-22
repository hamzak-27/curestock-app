from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('export/csv/', views.export_medicines_csv, name='export_medicines_csv'),
    path('api/medicines/', views.api_medicines_json, name='api_medicines_json'),
    path('', views.home, name='home'),
    path('webhook/', views.webhook, name='webhook'),
    path('latest-calls/', views.latest_calls, name='latest_calls'),
    path('call/<int:call_id>/', views.call_detail, name='call_detail'),
    path('call/<int:call_id>/generate-bill/', views.generate_bill, name='generate_bill'),
    path('bill/<int:bill_id>/', views.view_bill, name='view_bill'),
]
