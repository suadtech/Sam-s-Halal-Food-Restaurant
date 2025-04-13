from django import forms
from .models import Booking, Table
from django.utils import timezone
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingForm(forms.ModelForm):
    """Form for creating and updating bookings."""
    
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                 'date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # Set minimum date to today
        self.fields['date'].widget.attrs['min'] = timezone.now().date().isoformat()
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')
        
        # Basic validation
        if date and time and number_of_guests:
            # Check if booking date is in the past
            if date < timezone.now().date():
                self.add_error('date', "Booking date cannot be in the past.")
            
            # If booking is today, check if booking time is in the past
            if date == timezone.now().date() and time < timezone.now().time():
                self.add_error('time', "Booking time cannot be in the past.")
            
            # Check if there are enough tables available for the number of guests
            available_tables = self.get_available_tables(date, time)
            total_capacity = sum(table.capacity for table in available_tables)
            
            if total_capacity < number_of_guests:
                self.add_error('number_of_guests', 
                              f"Sorry, we don't have enough capacity for {number_of_guests} guests at this time. "
                              f"Maximum available capacity is {total_capacity}.")
        
        return cleaned_data
    
    def get_available_tables(self, date, time):
        """Get available tables for the given date and time."""
        # Convert time to datetime for comparison
        booking_datetime = datetime.datetime.combine(date, time)
        
        # Get all tables
        all_tables = Table.objects.filter(status='available')
        
        # Get tables that are already booked at the requested time
        # We consider a table unavailable if there's a booking within 2 hours of the requested time
        two_hours = datetime.timedelta(hours=2)
        start_time = (booking_datetime - two_hours).time()
        end_time = (booking_datetime + two_hours).time()
        
        booked_tables = Table.objects.filter(
            bookings__date=date,
            bookings__status__in=['pending', 'confirmed'],
            bookings__time__gte=start_time,
            bookings__time__lte=end_time
        )
        
        # Get available tables
        available_tables = all_tables.exclude(id__in=booked_tables.values_list('id', flat=True))
        
        return available_tables

class CancellationForm(forms.Form):
    """Form for cancelling bookings."""
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    confirmation = forms.BooleanField(
        label="I confirm that I want to cancel this booking",
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super(CancellationForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name != 'booking_id':
                field.widget.attrs['class'] = 'form-check-input'

        
 
