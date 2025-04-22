from django.db import models
from django.utils import timezone

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Rupees")
    quantity = models.PositiveIntegerField(default=0)
    is_discontinued = models.BooleanField(default=False)
    medicine_type = models.CharField(max_length=100, blank=True, null=True)
    pack_size = models.CharField(max_length=100, blank=True, null=True)
    composition1 = models.CharField(max_length=200, blank=True, null=True)
    composition2 = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Call(models.Model):
    phone_number = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)  # Duration in seconds
    call_time = models.DateTimeField(default=timezone.now)
    follow_up = models.BooleanField(default=False)
    summary = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    recording_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"Call from {self.phone_number} at {self.call_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-call_time']

class Order(models.Model):
    DELIVERY_CHOICES = (
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='orders')
    medicine_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50)  # e.g., "1 tablet"
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='pickup')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order: {self.medicine_name} ({self.quantity}) - {self.get_status_display()}"

class Bill(models.Model):
    call = models.OneToOneField(Call, on_delete=models.CASCADE, related_name='bill')
    invoice_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)
    content = models.TextField()  # Store the formatted bill content
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - ₹{self.total_amount}"
