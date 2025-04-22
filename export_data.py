#!/usr/bin/env python
import os
import json
import sys
import django

"""
This script exports data from Django models to JSON files that can later be imported into PostgreSQL.
Run this script locally before deploying to Vercel with the PostgreSQL database.
"""

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.core.serializers.json import DjangoJSONEncoder
from myapp.models import Medicine, Call, Order, Bill  # Import your models

def export_model_data(model, output_file):
    """Export model data to a JSON file"""
    queryset = model.objects.all()
    
    if not queryset.exists():
        print(f"No data found for {model.__name__}")
        return
    
    data = []
    for obj in queryset:
        # Get fields and values
        fields = {}
        for field in obj._meta.fields:
            field_name = field.name
            field_value = getattr(obj, field_name)
            fields[field_name] = field_value
        
        data.append({
            "model": f"{model._meta.app_label}.{model._meta.model_name}",
            "pk": obj.pk,
            "fields": fields
        })
    
    # Ensure the exports directory exists
    if not os.path.exists("data_exports"):
        os.makedirs("data_exports")
    
    # Save to file
    with open(f"data_exports/{output_file}", 'w') as f:
        json.dump(data, f, cls=DjangoJSONEncoder, indent=4)
    
    print(f"Exported {len(data)} {model.__name__} records to data_exports/{output_file}")

if __name__ == "__main__":
    print("Exporting data from SQLite database...")
    
    # Export each model
    export_model_data(Medicine, "medicines.json")
    export_model_data(Call, "calls.json")
    export_model_data(Order, "orders.json")
    export_model_data(Bill, "bills.json")
    
    print("Data export complete. Files are in the data_exports/ directory.")
    print("To import this data to PostgreSQL, run 'python import_data.py' after setting up the PostgreSQL database.") 