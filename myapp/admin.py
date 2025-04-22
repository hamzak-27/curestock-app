from django.contrib import admin
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import Medicine, Call, Order, Bill

def export_selected_medicines_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="medicines_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    fieldnames = [
        'id', 
        'name', 
        'manufacturer', 
        'price', 
        'quantity', 
        'is_discontinued', 
        'medicine_type', 
        'pack_size', 
        'composition1', 
        'composition2'
    ]
    
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    
    for medicine in queryset:
        writer.writerow({
            'id': medicine.id,
            'name': medicine.name,
            'manufacturer': medicine.manufacturer,
            'price': medicine.price,
            'quantity': medicine.quantity,
            'is_discontinued': medicine.is_discontinued,
            'medicine_type': medicine.medicine_type or '',
            'pack_size': medicine.pack_size or '',
            'composition1': medicine.composition1 or '',
            'composition2': medicine.composition2 or ''
        })
    
    return response
export_selected_medicines_to_csv.short_description = "Export selected medicines to CSV"

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price', 'quantity', 'is_discontinued')
    list_filter = ('manufacturer', 'is_discontinued', 'medicine_type')
    search_fields = ('name', 'manufacturer', 'composition1', 'composition2')
    actions = [export_selected_medicines_to_csv]

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ('created_at', 'updated_at')

class BillInline(admin.TabularInline):
    model = Bill
    extra = 0
    readonly_fields = ('created_at', 'invoice_number', 'total_amount')

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'call_time', 'duration', 'follow_up')
    list_filter = ('follow_up', 'call_time')
    search_fields = ('phone_number', 'summary', 'transcript')
    readonly_fields = ('recording_url',)
    inlines = [OrderInline, BillInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'quantity', 'delivery_method', 'status', 'created_at')
    list_filter = ('delivery_method', 'status', 'created_at')
    search_fields = ('medicine_name',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'call', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('invoice_number', 'call__phone_number')
    readonly_fields = ('created_at', 'invoice_number')
