from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
import csv
import json
import datetime
import re
from .models import Medicine, Call, Order, Bill
from .utils import generate_bill_with_openai, generate_invoice_number

# Add a simple health check view
def health_check(request):
    """Simple health check endpoint that doesn't depend on database access"""
    return HttpResponse("OK", content_type="text/plain")

# Create your views here.

def inventory_list(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'myapp/inventory_list.html', {'medicines': medicines})

def medicine_detail(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    return render(request, 'myapp/medicine_detail.html', {'medicine': medicine})

def export_medicines_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="medicines_inventory_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    # Create a csv writer
    writer = csv.writer(response)
    
    # Add header row
    writer.writerow(['ID', 'Name', 'Manufacturer', 'Price (₹)', 'Quantity', 'Status',
                    'Type', 'Pack Size', 'Composition 1', 'Composition 2'])
    
    # Get all medicines and add rows
    medicines = Medicine.objects.all().order_by('name')
    for medicine in medicines:
        status = 'Discontinued' if medicine.is_discontinued else 'Active'
        writer.writerow([
            medicine.id,
            medicine.name,
            medicine.manufacturer,
            medicine.price,
            medicine.quantity,
            status,
            medicine.medicine_type or '',
            medicine.pack_size or '',
            medicine.composition1 or '',
            medicine.composition2 or ''
        ])
    
    return response

def api_medicines_json(request):
    medicines = Medicine.objects.all().order_by('name')
    
    # Format the data for JSON
    data = []
    for medicine in medicines:
        data.append({
            'id': medicine.id,
            'name': medicine.name,
            'manufacturer': medicine.manufacturer,
            'price': float(medicine.price),  # Convert Decimal to float for JSON
            'quantity': medicine.quantity,
            'is_discontinued': medicine.is_discontinued,
            'status': 'Discontinued' if medicine.is_discontinued else 'Active',
            'medicine_type': medicine.medicine_type or '',
            'pack_size': medicine.pack_size or '',
            'composition1': medicine.composition1 or '',
            'composition2': medicine.composition2 or ''
        })
    
    return JsonResponse(data, safe=False)

def format_transcript(transcript):
    """Clean up and format the transcript if needed"""
    # Currently, we just return the transcript as is
    # You can add any formatting logic here if needed
    return transcript

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Log the raw request data
            print("Webhook received!")
            
            body = request.body.decode('utf-8')
            print(f"Raw body: {body}")
            
            data = json.loads(body)
            
            # Check for different event types
            event_type = data.get('event')
            print(f"Event type: {event_type}")
            
            # Handle call_analyzed event
            if event_type == 'call_analyzed':
                call_data = data.get('call', {})
                
                # Extract phone number
                phone_number = call_data.get('from_number', 'Unknown')
                
                # Extract duration (convert ms to seconds)
                duration_ms = call_data.get('duration_ms', 0)
                duration = int(duration_ms / 1000) if duration_ms else 0
                
                # Extract call time
                start_timestamp = call_data.get('start_timestamp')
                if start_timestamp:
                    try:
                        call_time = datetime.datetime.fromtimestamp(
                            int(start_timestamp) / 1000,
                            tz=timezone.utc
                        )
                    except:
                        call_time = timezone.now()
                else:
                    call_time = timezone.now()
                
                # Extract follow-up flag, summary, transcript, recording URL
                follow_up = call_data.get('call_analysis', {}).get('custom_analysis_data', {}).get('_follow_up', False)
                summary = call_data.get('call_analysis', {}).get('call_summary', '')
                
                # Format the transcript if needed
                transcript = call_data.get('transcript', '')
                transcript = format_transcript(transcript)
                
                recording_url = call_data.get('recording_url', '')
                
                # Create call record
                call = Call.objects.create(
                    phone_number=phone_number,
                    duration=duration,
                    call_time=call_time,
                    follow_up=follow_up,
                    summary=summary,
                    transcript=transcript,
                    recording_url=recording_url
                )
                
                # Extract medicine and quantity information from custom analysis data
                medicines = call_data.get('call_analysis', {}).get('custom_analysis_data', {}).get('_medicines', '')
                quantities = call_data.get('call_analysis', {}).get('custom_analysis_data', {}).get('_quantities', '')
                
                # Create order if medicine information exists
                if medicines and quantities:
                    medicine_names = medicines.split(',')
                    quantity_values = quantities.split(',')
                    
                    # Determine delivery method from transcript (default to pickup)
                    delivery_method = 'pickup'
                    if 'delivery' in transcript.lower() and 'pickup' not in transcript.lower():
                        delivery_method = 'delivery'
                    elif 'pickup' in transcript.lower():
                        delivery_method = 'pickup'
                    
                    # Create order for each medicine (usually just one)
                    for i, medicine_name in enumerate(medicine_names):
                        quantity = quantity_values[i] if i < len(quantity_values) else "1"
                        Order.objects.create(
                            call=call,
                            medicine_name=medicine_name.strip(),
                            quantity=quantity.strip(),
                            delivery_method=delivery_method,
                            status='confirmed'
                        )
                
                print(f"Created call record with ID {call.id}")
                return JsonResponse({'status': 'success', 'id': call.id}, status=201)
            
            # Handle other event types (call_started, call_ended)
            elif event_type in ['call_started', 'call_ended']:
                return JsonResponse({'status': 'received', 'event': event_type}, status=200)
            
            # Handle test payloads from Postman
            elif not event_type and 'from_number' in data:
                # This is likely a test payload
                
                # Format the transcript if needed
                transcript = data.get('transcript', '')
                transcript = format_transcript(transcript)
                
                call = Call.objects.create(
                    phone_number=data.get('from_number', 'Unknown'),
                    duration=data.get('duration', 0),
                    call_time=timezone.now(),
                    follow_up=data.get('Follow_up', False),
                    summary=data.get('summary', ''),
                    transcript=transcript,
                    recording_url=data.get('recording_url', '')
                )
                
                return JsonResponse({'status': 'success', 'id': call.id}, status=201)
            
            # Handle unknown event types
            else:
                print(f"Unknown event type or structure: {data}")
                return JsonResponse({'status': 'received', 'message': 'Unknown event type'}, status=200)
                
        except Exception as e:
            import traceback
            print(f"Error processing webhook: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'method not allowed'}, status=405)

def latest_calls(request):
    last_id = request.GET.get('last_id')
    
    if last_id:
        new_calls = Call.objects.filter(id__gt=last_id).order_by('-call_time')
        calls_data = []
        
        for call in new_calls:
            calls_data.append({
                'id': call.id,
                'phone_number': call.phone_number,
                'duration': call.duration,
                'call_time': call.call_time.isoformat(),
                'follow_up': call.follow_up
            })
        
        return JsonResponse({'calls': calls_data})
    
    return JsonResponse({'calls': []})

def home(request):
    try:
        calls = Call.objects.all().order_by('-call_time')
        return render(request, 'myapp/home.html', {'calls': calls})
    except Exception as e:
        # Provide a fallback if database access fails
        return HttpResponse(f"Welcome to CureStock App. Setup your database connection to view calls. Error: {str(e)}")

def call_detail(request, call_id):
    call = get_object_or_404(Call, id=call_id)
    orders = call.orders.all()
    
    # Check if bill exists
    try:
        bill = call.bill
        has_bill = True
    except Bill.DoesNotExist:
        has_bill = False
        bill = None
    
    return render(request, 'myapp/call_detail.html', {
        'call': call, 
        'orders': orders,
        'has_bill': has_bill,
        'bill': bill
    })

def generate_bill(request, call_id):
    call = get_object_or_404(Call, id=call_id)
    orders = call.orders.all()
    
    # Check if a bill already exists
    try:
        bill = call.bill
        # Bill already exists, just show it
        return redirect('myapp:view_bill', bill_id=bill.id)
    except Bill.DoesNotExist:
        # Generate new bill
        pass
    
    if not orders:
        messages.error(request, "Cannot generate bill: No orders found for this call.")
        return redirect('myapp:call_detail', call_id=call.id)
    
    # Generate the bill using the synchronous function
    try:
        bill_data = generate_bill_with_openai(call, orders)
        
        # Create and save the bill
        bill = Bill.objects.create(
            call=call,
            invoice_number=bill_data['invoice_number'],
            total_amount=bill_data['total_amount'],
            gst_percentage=bill_data['gst_percentage'],
            content=bill_data['content']
        )
        
        return redirect('myapp:view_bill', bill_id=bill.id)
    except Exception as e:
        messages.error(request, f"Error generating bill: {str(e)}")
        return redirect('myapp:call_detail', call_id=call.id)

def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'myapp/bill_detail.html', {'bill': bill})
