from django.contrib import admin
from .models import Restaurant, Table, MenuCategory, MenuItem, Booking
# Regiter your models here
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'opening_time', 'closing_time')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'status')
    list_filter = ('status', 'capacity')
    search_fields = ('table_number',)
    list_editable = ('status',)

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_halal')
    list_filter = ('category', 'is_available', 'is_halal')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'date', 'time', 'number_of_guests', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tables',)
    
    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'mark_as_completed']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected bookings as completed"

