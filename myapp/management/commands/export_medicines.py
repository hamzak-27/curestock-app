import csv
import os
from django.core.management.base import BaseCommand
from myapp.models import Medicine

class Command(BaseCommand):
    help = 'Export all medicines from the database to a CSV file'

    def handle(self, *args, **options):
        # Get all medicines from the database
        medicines = Medicine.objects.all().order_by('name')
        
        # Define the CSV file path
        export_path = 'exported_medicines.csv'
        
        # Define the CSV header fields
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
        
        # Write to CSV file
        with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write medicine data
            for medicine in medicines:
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
            
        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(medicines)} medicines to {os.path.abspath(export_path)}')) 