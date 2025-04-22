#!/usr/bin/env python3
"""
Simple script to add sample medicine data to the database on Render.
This script automatically adds sample data without requiring any user input.
"""

import os
import sys
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

def setup_django():
    """Set up Django environment"""
    logger.info("Setting up Django environment...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.setup()
    logger.info("Django environment ready")

def add_sample_medicines():
    """Add sample medicines to the database"""
    try:
        # Import the Medicine model
        from myapp.models import Medicine
        
        # Check existing count
        existing_count = Medicine.objects.count()
        logger.info(f"Current medicine count in database: {existing_count}")
        
        # Sample data
        sample_medicines = [
            {
                'name': 'Paracetamol 500mg',
                'manufacturer': 'GSK',
                'price': '15.50',
                'quantity': 100,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '10 tablets',
                'composition1': 'Paracetamol',
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
                'composition2': 'Ammonium Chloride',
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
            },
            {
                'name': 'Dolo 650',
                'manufacturer': 'Micro Labs',
                'price': '30.00',
                'quantity': 120,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '15 tablets',
                'composition1': 'Paracetamol',
            },
            {
                'name': 'Cetrizine 10mg',
                'manufacturer': 'Cipla',
                'price': '45.00',
                'quantity': 50,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '10 tablets',
                'composition1': 'Cetirizine Hydrochloride',
            },
            {
                'name': 'Limcee 500mg',
                'manufacturer': 'Abbott',
                'price': '25.75',
                'quantity': 60,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '15 tablets',
                'composition1': 'Vitamin C',
            },
            {
                'name': 'Aspirin 75mg',
                'manufacturer': 'Bayer',
                'price': '15.25',
                'quantity': 90,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '14 tablets',
                'composition1': 'Acetylsalicylic Acid',
            },
            {
                'name': 'Metformin 500mg',
                'manufacturer': 'USV',
                'price': '35.00',
                'quantity': 45,
                'is_discontinued': False,
                'medicine_type': 'Tablet',
                'pack_size': '10 tablets',
                'composition1': 'Metformin Hydrochloride',
            }
        ]
        
        # Add the sample medicines to the database
        added_count = 0
        for medicine_data in sample_medicines:
            # Create medicine with default empty string for any missing fields
            medicine = Medicine(
                name=medicine_data.get('name', ''),
                manufacturer=medicine_data.get('manufacturer', ''),
                price=Decimal(medicine_data.get('price', '0')),
                quantity=int(medicine_data.get('quantity', 0)),
                is_discontinued=medicine_data.get('is_discontinued', False),
                medicine_type=medicine_data.get('medicine_type', ''),
                pack_size=medicine_data.get('pack_size', ''),
                composition1=medicine_data.get('composition1', ''),
                composition2=medicine_data.get('composition2', '')
            )
            medicine.save()
            added_count += 1
            logger.info(f"Added medicine: {medicine.name}")
        
        # Check final count
        final_count = Medicine.objects.count()
        logger.info(f"Successfully added {added_count} sample medicines")
        logger.info(f"Total medicines in database: {final_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding sample medicines: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("ADDING SAMPLE MEDICINES TO DATABASE")
    logger.info("=" * 60)
    
    # Setup Django
    setup_django()
    
    # Add sample medicines
    if add_sample_medicines():
        logger.info("Sample medicines added successfully")
    else:
        logger.error("Failed to add sample medicines")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("PROCESS COMPLETED")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 