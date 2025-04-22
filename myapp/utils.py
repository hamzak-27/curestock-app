import json
import random
import datetime
from decimal import Decimal
from django.conf import settings

# Import OpenAI safely with fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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
    Uses OpenAI to generate a formatted bill for the order, with fallback to simple format
    """
    # Prepare data 
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
    
    # Prepare context for bill generation
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

    # Try to use OpenAI if available
    if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
        try:
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
        except Exception as e:
            # Fallback to simple bill format if OpenAI fails
            bill_content = generate_simple_bill(context)
    else:
        # Use a simple bill generator if OpenAI is not available
        bill_content = generate_simple_bill(context)
    
    return {
        "invoice_number": context["invoice"]["number"],
        "content": bill_content,
        "total_amount": grand_total,
        "gst_percentage": gst_percentage
    }

def generate_simple_bill(context):
    """Generate a simple bill without using OpenAI"""
    invoice = context["invoice"]
    customer = context["customer"]
    items = context["order_items"]
    summary = context["summary"]
    
    # Format the header
    bill = [
        "=" * 60,
        "                CURESTOCK PHARMACY                ",
        "           Your Health is Our Priority            ",
        "=" * 60,
        "",
        f"INVOICE #{invoice['number']}",
        f"Date: {invoice['date']}",
        "",
        "CUSTOMER INFORMATION",
        f"Name: {customer['name']}",
        f"Phone: {customer['phone']}",
        "",
        "ITEMS",
        "-" * 60
    ]
    
    # Format line items
    bill.append(f"{'Item':<30} {'Quantity':<10} {'Price':<10} {'Amount':<10}")
    bill.append("-" * 60)
    
    for item in items:
        bill.append(f"{item['item']:<30} {item['quantity']:<10} {item['price']:<10.2f} {item['amount']:<10.2f}")
    
    # Format summary
    bill.extend([
        "-" * 60,
        f"{'Subtotal:':<50} {summary['subtotal']:<10.2f}",
        f"{'GST (' + str(summary['gst_percentage']) + '%):':<50} {summary['gst_amount']:<10.2f}",
        f"{'TOTAL:':<50} {summary['total']:<10.2f}",
        "",
        f"Delivery Method: {context['delivery_method']}",
        "",
        "PAYMENT",
        "Payment due within 30 days of invoice",
        "",
        "Thank you for choosing Curestock Pharmacy!",
        "For any queries, please contact us at support@curestock.com",
        "=" * 60
    ])
    
    return "\n".join(bill) 