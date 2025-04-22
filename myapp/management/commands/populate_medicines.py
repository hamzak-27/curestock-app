import os
import csv
import random
from django.core.management.base import BaseCommand
from myapp.models import Medicine

class Command(BaseCommand):
    help = 'Populate the database with 50 random medicines from the dataset'

    def handle(self, *args, **options):
        # Path to the CSV file relative to manage.py
        csv_file_path = 'A_Z_medicines_dataset_of_India.csv'
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return

        # Read all medicines from CSV
        medicines = []
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                medicines.append(row)
        
        # Select 50 random medicines
        if len(medicines) > 50:
            selected_medicines = random.sample(medicines, 50)
        else:
            selected_medicines = medicines
            self.stdout.write(self.style.WARNING(f'Only {len(medicines)} medicines found in the dataset.'))
        
        # Clear existing medicines
        Medicine.objects.all().delete()
        
        # Add medicines to the database
        for med in selected_medicines:
            # Generate random quantity between 10 and 200
            quantity = random.randint(10, 200)
            
            # Clean price data - removing currency symbol if present
            price_str = med.get('price(₹)', '0')
            if not price_str or price_str.strip() == '':
                price_str = '0'
            
            # Try to convert price to decimal, handle potential formatting issues
            try:
                price = float(price_str.replace('₹', '').strip())
            except ValueError:
                price = 0.0
            
            is_discontinued = med.get('Is_discontinued', 'FALSE').upper() == 'TRUE'
            
            # Create the medicine object
            Medicine.objects.create(
                name=med.get('name', 'Unknown Medicine'),
                manufacturer=med.get('manufacturer_name', 'Unknown Manufacturer'),
                price=price,
                quantity=quantity,
                is_discontinued=is_discontinued,
                medicine_type=med.get('type', ''),
                pack_size=med.get('pack_size_label', ''),
                composition1=med.get('short_composition1', ''),
                composition2=med.get('short_composition2', '')
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(selected_medicines)} medicines to the database')) 