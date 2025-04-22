#!/usr/bin/env python3
"""
Script to import medicine data to the Render PostgreSQL database.
This will use the existing CSV file to populate the Medicine model.
"""

import os
import sys
import csv
import logging
import django
from decimal import Decimal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# CSV file path
CSV_FILE = "exported_medicines.csv"
# Alternative: A_Z_medicines_dataset_of_India.csv (larger dataset)
# CSV_FILE = "A_Z_medicines_dataset_of_India.csv"

def setup_django():
    """Set up Django environment"""
    logger.info("Setting up Django environment...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.setup()
    logger.info("Django environment ready")

def check_database_connection():
    """Check database connection"""
    try:
        logger.info("Checking database connection...")
        from django.db import connections
        
        conn = connections['default']
        conn.ensure_connection()
        if conn.is_usable():
            logger.info("Database connection is working!")
            return True
        else:
            logger.error("Database connection is not usable.")
            return False
    except Exception as e:
        logger.error(f"Error checking database connection: {e}")
        return False

def import_from_csv():
    """Import medicines from CSV file"""
    try:
        # Import the Medicine model
        from myapp.models import Medicine
        
        # Check if the CSV file exists
        if not os.path.exists(CSV_FILE):
            logger.error(f"CSV file '{CSV_FILE}' not found!")
            return False
        
        # Check if there are already medicines in the database
        existing_count = Medicine.objects.count()
        logger.info(f"Found {existing_count} existing medicines in the database")
        
        if existing_count > 0:
            confirm = input(f"There are already {existing_count} medicines in the database. Do you want to continue and add more? (yes/no): ")
            if confirm.lower() != 'yes':
                logger.info("Import cancelled")
                return False
        
        # Read and import data from CSV
        imported_count = 0
        with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Extract data from row
                    name = row.get('name', '')
                    manufacturer = row.get('manufacturer', '')
                    price_str = row.get('price', '0')
                    quantity_str = row.get('quantity', '0')
                    is_discontinued_str = row.get('is_discontinued', 'False')
                    medicine_type = row.get('medicine_type', '')
                    pack_size = row.get('pack_size', '')
                    composition1 = row.get('composition1', '')
                    composition2 = row.get('composition2', '')
                    
                    # Clean and convert data
                    price = Decimal(price_str.replace('₹', '').strip()) if price_str else Decimal('0.00')
                    quantity = int(quantity_str) if quantity_str and quantity_str.isdigit() else 0
                    is_discontinued = is_discontinued_str.lower() == 'true'
                    
                    # Create the medicine
                    medicine = Medicine(
                        name=name,
                        manufacturer=manufacturer,
                        price=price,
                        quantity=quantity,
                        is_discontinued=is_discontinued,
                        medicine_type=medicine_type,
                        pack_size=pack_size,
                        composition1=composition1,
                        composition2=composition2
                    )
                    medicine.save()
                    imported_count += 1
                    
                    # Log progress for large imports
                    if imported_count % 100 == 0:
                        logger.info(f"Imported {imported_count} medicines so far...")
                    
                except Exception as e:
                    logger.error(f"Error importing row: {row}")
                    logger.error(f"Error details: {e}")
        
        logger.info(f"Successfully imported {imported_count} medicines")
        return True
    
    except Exception as e:
        logger.error(f"Error during import: {e}")
        return False

def import_sample_data():
    """Import a few sample medicines if CSV is not available"""
    try:
        from myapp.models import Medicine
        
        # Create some sample medicines
        sample_data = [
            {
                'name': 'Paracetamol 500mg',
                'manufacturer': 'GSK',
                'price': '15.50',
                'quantity': 100,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '10 tablets',
                'composition1': 'Paracetamol',
                'composition2': ''
            },
            {
                'name': 'Crocin 650mg',
                'manufacturer': 'GSK',
                'price': '25.00',
                'quantity': 75,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '15 tablets',
                'composition1': 'Paracetamol',
                'composition2': ''
            },
            {
                'name': 'Allegra 120mg',
                'manufacturer': 'Sanofi',
                'price': '165.75',
                'quantity': 30,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '10 tablets',
                'composition1': 'Fexofenadine',
                'composition2': ''
            },
            {
                'name': 'Benadryl Cough Syrup',
                'manufacturer': 'Johnson & Johnson',
                'price': '110.00',
                'quantity': 15,
                'is_discontinued': False,
                'medicine_type': 'Syrup',
                'pack_size': '100ml',
                'composition1': 'Diphenhydramine',
                'composition2': 'Ammonium Chloride'
            },
            {
                'name': 'Azithromycin 250mg',
                'manufacturer': 'Cipla',
                'price': '85.50',
                'quantity': 20,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '6 tablets',
                'composition1': 'Azithromycin',
                'composition2': ''
            }
        ]
        
        # Add them to the database
        for item in sample_data:
            medicine = Medicine(
                name=item['name'],
                manufacturer=item['manufacturer'],
                price=Decimal(item['price']),
                quantity=item['quantity'],
                is_discontinued=item['is_discontinued'],
                medicine_type=item['medicine_type'],
                pack_size=item['pack_size'],
                composition1=item['composition1'],
                composition2=item['composition2']
            )
            medicine.save()
        
        logger.info(f"Added {len(sample_data)} sample medicines to the database")
        return True
    
    except Exception as e:
        logger.error(f"Error adding sample data: {e}")
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("MEDICINE DATA IMPORT TOOL")
    logger.info("=" * 60)
    
    # Setup Django
    setup_django()
    
    # Check database connection
    if not check_database_connection():
        logger.error("Failed to connect to database! Exiting.")
        sys.exit(1)
    
    # Try to import from CSV first
    if os.path.exists(CSV_FILE):
        logger.info(f"Found CSV file: {CSV_FILE}")
        
        if import_from_csv():
            logger.info("CSV import completed successfully")
        else:
            logger.error("CSV import failed")
            
            # Ask if user wants to add sample data instead
            add_samples = input("Would you like to add sample medicine data instead? (yes/no): ")
            if add_samples.lower() == 'yes':
                import_sample_data()
    else:
        logger.warning(f"CSV file '{CSV_FILE}' not found!")
        
        # Ask if user wants to add sample data
        add_samples = input("Would you like to add sample medicine data? (yes/no): ")
        if add_samples.lower() == 'yes':
            import_sample_data()
    
    # Check the final medicine count
    from myapp.models import Medicine
    final_count = Medicine.objects.count()
    logger.info(f"Total medicines in database: {final_count}")
    
    logger.info("=" * 60)
    logger.info("IMPORT PROCESS COMPLETED")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 