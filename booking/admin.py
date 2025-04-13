from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, Table, MenuCategory, MenuItem, Booking

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'opening_time', 'closing_time')
    search_fields = ('name', 'address', 'phone', 'email')
    fieldsets = (
        ('Restaurant Information', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
    )

class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'status', 'get_current_booking')
    list_filter = ('status', 'capacity')
    search_fields = ('table_number',)
    list_editable = ('status',)
    actions = ['mark_as_available', 'mark_as_maintenance']
    
    def get_current_booking(self, obj):
        current_bookings = obj.bookings.filter(status__in=['pending', 'confirmed']).order_by('date', 'time').first()
        if current_bookings:
            return format_html(
                '<a href="{}">{} - {} at {}</a>',
                f'/admin/booking/booking/{current_bookings.id}/change/',
                current_bookings.customer_name,
                current_bookings.date,
                current_bookings.time
            )
        return "No current booking"
    get_current_booking.short_description = 'Current Booking'
    
    def mark_as_available(self, request, queryset):
        queryset.update(status='available')
    mark_as_available.short_description = "Mark selected tables as available"
    
    def mark_as_maintenance(self, request, queryset):
        queryset.update(status='maintenance')
    mark_as_maintenance.short_description = "Mark selected tables as under maintenance"

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'price', 'is_available', 'is_halal')

class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_items_count')
    search_fields = ('name', 'description')
    inlines = [MenuItemInline]
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Number of Items'

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_halal')
    list_filter = ('category', 'is_available', 'is_halal')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Status', {
            'fields': ('is_available', 'is_halal')
        }),
        ('Image', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'date', 'time', 'number_of_guests', 'status', 'created_at')
    list_filter = ('date', 'status', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tables',)
    actions = ['confirm_bookings', 'cancel_bookings', 'mark_as_completed']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('date', 'time', 'number_of_guests', 'status')
        }),
        ('Table Assignment', {
            'fields': ('tables',)
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at', 'updated_at')
        }),
    )
    
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')
        # Release tables
        for booking in queryset:
            booking.tables.clear()
    cancel_bookings.short_description = "Cancel selected bookings"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected bookings as completed"

# Register models with custom admin classes
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Booking, BookingAdmin)

# Customize admin site
admin.site.site_header = "Sam's Halal Food Restaurant Administration"
admin.site.site_title = "Sam's Restaurant Admin"
admin.site.index_title = "Restaurant Management"

