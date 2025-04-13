from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Restaurant(models.Model):
    """Model representing the restaurant information."""
    name = models.CharField(max_length=100, default="Sam's Halal Food Restaurant")
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    def __str__(self):
        return self.name

class MenuCategory(models.Model):
    """Model representing menu categories."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Menu Categories"

class MenuItem(models.Model):
    """Model representing menu items."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    is_available = models.BooleanField(default=True)
    is_halal = models.BooleanField(default=True)  # Specific to halal restaurant
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Table(models.Model):
    """Model representing restaurant tables."""
    TABLE_STATUS = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    )
    
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=TABLE_STATUS, default='available')
    
    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"
    
    class Meta:
        ordering = ['table_number']

class Booking(models.Model):
    """Model representing table bookings."""
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    tables = models.ManyToManyField(Table, related_name='bookings')
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking for {self.customer_name} on {self.date} at {self.time}"
    
    def clean(self):
        """Validate booking to prevent double bookings."""
        # Check if booking date is in the past
        if self.date < timezone.now().date():
            raise ValidationError("Booking date cannot be in the past.")
        
        # If booking is today, check if booking time is in the past
        if self.date == timezone.now().date() and self.time < timezone.now().time():
            raise ValidationError("Booking time cannot be in the past.")
        
        # Check if restaurant is open at the requested time
        try:
            restaurant = Restaurant.objects.first()
            if restaurant:
                if self.time < restaurant.opening_time or self.time > restaurant.closing_time:
                    raise ValidationError("Restaurant is closed at the requested time.")
        except Restaurant.DoesNotExist:
            pass
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date', 'time']

