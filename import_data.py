#!/usr/bin/env python
import os
import json
import sys
import django

"""
This script imports data from JSON files into the PostgreSQL database.
Run this script after migrating your database schema to PostgreSQL and exporting your data.
"""

# Force Vercel environment to use PostgreSQL
os.environ["VERCEL"] = "1"

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.apps import apps
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder

def import_model_data(input_file):
    """Import model data from a JSON file"""
    # Check if the file exists
    file_path = f"data_exports/{input_file}"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    # Load data from file
    with open(file_path, 'r') as f:
        data_list = json.load(f)
    
    if not data_list:
        print(f"No data found in {input_file}")
        return
    
    # Get the model class from the first item
    first_item = data_list[0]
    model_str = first_item["model"]
    app_label, model_name = model_str.split('.')
    model_class = apps.get_model(app_label, model_name)
    
    # Import data within a transaction
    with transaction.atomic():
        # Clear existing data
        model_class.objects.all().delete()
        
        # Create new objects
        for item in data_list:
            pk = item["pk"]
            fields = item["fields"]
            
            # Create the object
            model_class.objects.create(id=pk, **fields)
    
    print(f"Imported {len(data_list)} {model_name} records from {input_file}")

if __name__ == "__main__":
    print("Importing data to PostgreSQL database...")
    
    # Import each model's data
    # Import in order of dependencies (models without foreign keys first)
    import_model_data("medicines.json")
    import_model_data("calls.json")
    import_model_data("orders.json")
    import_model_data("bills.json")
    
    print("Data import complete.") 