from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from .models import Restaurant, Table, MenuItem, MenuCategory, Booking
from .forms import BookingForm, CancellationForm
import datetime

def home(request):
    """View for the homepage."""
    try:
        restaurant = Restaurant.objects.first()
    except Restaurant.DoesNotExist:
        restaurant = None
    
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'booking/home.html', context)

def menu(request):
    """View for displaying the restaurant menu."""
    categories = MenuCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'booking/menu.html', context)

def booking_create(request):
    """View for creating a new booking."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'pending'
            booking.save()
            
            # Assign tables to the booking
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_guests = form.cleaned_data['number_of_guests']
            
            # Get available tables
            available_tables = form.get_available_tables(date, time)
            
            # Sort tables by capacity to optimize table allocation
            available_tables = sorted(available_tables, key=lambda t: t.capacity)
            
            # Assign tables to accommodate the number of guests
            remaining_guests = number_of_guests
            assigned_tables = []
            
            for table in available_tables:
                if remaining_guests <= 0:
                    break
                
                assigned_tables.append(table)
                remaining_guests -= table.capacity
            
            # Add tables to the booking
            for table in assigned_tables:
                booking.tables.add(table)
            
            messages.success(request, 'Your booking has been created successfully! We will confirm your booking shortly.')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
    }
    return render(request, 'booking/booking_form.html', context)

def booking_detail(request, booking_id):
    """View for displaying booking details."""
    booking = get_object_or_404(Booking, id=booking_id)
    cancellation_form = CancellationForm(initial={'booking_id': booking.id})
    
    context = {
        'booking': booking,
        'cancellation_form': cancellation_form,
    }
    return render(request, 'booking/booking_detail.html', context)

def booking_list(request):
    """View for listing user's bookings."""
    # In a real application, this would filter by the logged-in user
    # For now, we'll just show all bookings
    bookings = Booking.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'time')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking/booking_list.html', context)

@require_POST
def booking_cancel(request):
    """View for cancelling a booking."""
    form = CancellationForm(request.POST)
    if form.is_valid():
        booking_id = form.cleaned_data['booking_id']
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Only allow cancellation of pending or confirmed bookings
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            
            # Release the tables
            booking.tables.clear()
            
            messages.success(request, 'Your booking has been cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
        
        return redirect('booking_list')
    
    messages.error(request, 'Invalid form submission.')
    return redirect('booking_list')

def check_availability(request):
    """AJAX view for checking table availability."""
    if request.method == 'GET':
        date_str = request.GET.get('date')
        time_str = request.GET.get('time')
        guests = request.GET.get('guests')
        
        if not all([date_str, time_str, guests]):
            return JsonResponse({'available': False, 'message': 'Missing parameters'})
        
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.datetime.strptime(time_str, '%H:%M').time()
            guests = int(guests)
        except (ValueError, TypeError):
            return JsonResponse({'available': False, 'message': 'Invalid parameters'})
        
        # Check if date is in the past
        if date < timezone.now().date():
            return JsonResponse({'available': False, 'message': 'Cannot book for past dates'})
        
        # If booking is today, check if time is in the past
        if date == timezone.now().date() and time < timezone.now().time():
            return JsonResponse({'available': False, 'message': 'Cannot book for past times'})
        
        # Create a temporary form to use its get_available_tables method
        form = BookingForm()
        available_tables = form.get_available_tables(date, time)
        total_capacity = sum(table.capacity for table in available_tables)
        
        if total_capacity >= guests:
            return JsonResponse({
                'available': True, 
                'message': f'Tables available for {guests} guests',
                'capacity': total_capacity
            })
        else:
            return JsonResponse({
                'available': False, 
                'message': f'Not enough capacity for {guests} guests. Maximum available: {total_capacity}',
                'capacity': total_capacity
            })
    
    return JsonResponse({'available': False, 'message': 'Invalid request method'})
