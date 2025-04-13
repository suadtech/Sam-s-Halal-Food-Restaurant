from django.contrib.auth.models import User
from booking.models import Restaurant, Table, MenuCategory, MenuItem
import datetime

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print('Created superuser: admin/adminpassword')

# Create restaurant
restaurant, created = Restaurant.objects.get_or_create(
    name="Sam's Halal Food Restaurant",
    defaults={
        'address': '123 Main Street, City, Country',
        'phone': '(123) 456-7890',
        'email': 'info@samshalal.com',
        'opening_time': datetime.time(11, 0),
        'closing_time': datetime.time(22, 0),
    }
)
print(f'Restaurant: {restaurant.name}')

# Create tables
for i in range(1, 9):
    capacity = 2 if i <= 2 else 4 if i <= 4 else 6 if i <= 6 else 8
    table, created = Table.objects.get_or_create(
        table_number=i,
        defaults={
            'capacity': capacity,
            'status': 'available'
        }
    )
    print(f'Table: {table}')

# Create menu categories
categories = [
    ('Appetizers', 'Start your meal with our delicious appetizers'),
    ('Main Courses', 'Our signature halal dishes'),
    ('Desserts', 'Sweet treats to end your meal'),
    ('Beverages', 'Refreshing drinks to complement your meal')
]

for name, desc in categories:
    category, created = MenuCategory.objects.get_or_create(
        name=name, defaults={'description': desc}
    )
    print(f'Category: {category.name}')

# Add some menu items
appetizers = MenuCategory.objects.get(name='Appetizers')
main_courses = MenuCategory.objects.get(name='Main Courses')
desserts = MenuCategory.objects.get(name='Desserts')
beverages = MenuCategory.objects.get(name='Beverages')

menu_items = [
    ('Hummus', 'Creamy chickpea dip with tahini', 6.99, appetizers),
    ('Falafel', 'Deep-fried patties made from ground chickpeas', 7.99, appetizers),
    ('Chicken Biryani', 'Fragrant rice with chicken', 14.99, main_courses),
    ('Lamb Kebabs', 'Juicy lamb kebabs with spices', 16.99, main_courses),
    ('Baklava', 'Sweet pastry with nuts and honey', 6.99, desserts),
    ('Mango Lassi', 'Yogurt drink with mango', 4.99, beverages)
]

for name, desc, price, category in menu_items:
    item, created = MenuItem.objects.get_or_create(
        name=name,
        category=category,
        defaults={
            'description': desc,
            'price': price,
            'is_available': True,
            'is_halal': True
        }
    )
    print(f'Menu item: {item.name}')

print('Initialization complete!')

