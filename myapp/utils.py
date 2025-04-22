import json
import random
import datetime
import openai
from django.conf import settings
from decimal import Decimal

def extract_quantity_value(quantity_str):
    """
    Extracts numerical quantity from a string like "1 tablet" or "30 tablets"
    Returns a tuple of (numeric_value, unit)
    """
    parts = quantity_str.strip().split(' ', 1)
    try:
        value = int(parts[0])
        unit = parts[1] if len(parts) > 1 else ''
        return value, unit
    except (ValueError, IndexError):
        # Default to 1 if we can't parse the quantity
        return 1, 'unit'

def generate_invoice_number():
    """Generate a unique invoice number with format INV-YYYYMMDD-XXXX"""
    today = datetime.datetime.now()
    date_part = today.strftime("%Y%m%d")
    random_part = random.randint(1000, 9999)
    return f"INV-{date_part}-{random_part}"

def find_medicine_in_database(medicine_name):
    """Find a medicine in the database by searching different variations of the name"""
    from .models import Medicine
    
    # Try exact match first
    medicine = Medicine.objects.filter(name__iexact=medicine_name).first()
    if medicine:
        return medicine
    
    # Try contains match
    medicine = Medicine.objects.filter(name__icontains=medicine_name).first()
    if medicine:
        return medicine
    
    # Try searching for the first word of the medicine name (common generic name)
    parts = medicine_name.split()
    if parts:
        medicine = Medicine.objects.filter(name__icontains=parts[0]).first()
        if medicine:
            return medicine
    
    # No match found
    return None

def generate_bill_with_openai(call, orders):
    """
    Uses OpenAI to generate a formatted bill for the order
    """
    # Prepare data for OpenAI
    order_items = []
    total_amount = Decimal('0.00')
    
    for order in orders:
        medicine_name = order.medicine_name
        # Try to find the medicine in our database
        medicine = find_medicine_in_database(medicine_name)
        
        # Parse quantity (e.g., "1 tablet" -> 1)
        quantity_value, _ = extract_quantity_value(order.quantity)
        
        if medicine:
            # Use actual price from database
            price = medicine.price
            amount = price * Decimal(quantity_value)
            
            # Update inventory quantity
            if medicine.quantity >= quantity_value:
                medicine.quantity -= quantity_value
                medicine.save()
            
            order_items.append({
                "item": medicine.name,  # Use the actual name from the database
                "quantity": order.quantity,
                "price": float(price),
                "amount": float(amount)
            })
            total_amount += amount
        else:
            # Default price if medicine not found
            default_price = Decimal('50.00')
            amount = default_price * Decimal(quantity_value)
            
            order_items.append({
                "item": medicine_name,
                "quantity": order.quantity,
                "price": float(default_price),
                "amount": float(amount)
            })
            total_amount += amount
    
    # Calculate tax
    gst_percentage = Decimal('18.00')
    gst_amount = (total_amount * gst_percentage) / Decimal('100.00')
    grand_total = total_amount + gst_amount
    
    # Prepare context for OpenAI
    context = {
        "customer": {
            "name": f"Customer ({call.phone_number})",
            "phone": call.phone_number,
            "date": call.call_time.strftime("%B %d, %Y")
        },
        "invoice": {
            "number": generate_invoice_number(),
            "date": datetime.datetime.now().strftime("%B %d, %Y")
        },
        "order_items": order_items,
        "summary": {
            "subtotal": float(total_amount),
            "gst_percentage": float(gst_percentage),
            "gst_amount": float(gst_amount),
            "total": float(grand_total)
        },
        "delivery_method": orders[0].get_delivery_method_display() if orders else "Pickup"
    }

    # Generate bill using OpenAI
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    prompt = f"""
    Generate a professional looking invoice for a pharmacy in text format (no HTML).
    Use the following information to generate the invoice:
    
    {json.dumps(context, indent=2)}
    
    The format should include:
    1. Company header (Curestock Pharmacy)
    2. Invoice details (number, date)
    3. Customer information
    4. Line items with quantity, unit price, and amount
    5. Subtotal
    6. GST (tax)
    7. Total amount
    8. Payment and delivery information
    9. Thank you message
    
    Make it look well-formatted and professional using only plain text with proper spacing and alignment.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional invoice generator for a pharmacy."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    bill_content = response.choices[0].message.content.strip()
    
    return {
        "invoice_number": context["invoice"]["number"],
        "content": bill_content,
        "total_amount": grand_total,
        "gst_percentage": gst_percentage
    } 