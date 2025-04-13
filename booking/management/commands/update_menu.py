from django.core.management.base import BaseCommand
from booking.models import Restaurant, Table, MenuCategory, MenuItem
import datetime

class Command(BaseCommand):
    help = 'Update the menu with more food items for Sam\'s Halal Food Restaurant'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding more food items to the menu for Sam\'s Halal Food Restaurant...')
        
        # Create or get menu categories
        appetizers, _ = MenuCategory.objects.get_or_create(
            name="Appetizers",
            defaults={"description": "Start your meal with our delicious appetizers"}
        )
        
        main_courses, _ = MenuCategory.objects.get_or_create(
            name="Main Courses",
            defaults={"description": "Our signature halal dishes"}
        )
        
        desserts, _ = MenuCategory.objects.get_or_create(
            name="Desserts",
            defaults={"description": "Sweet treats to end your meal"}
        )
        
        beverages, _ = MenuCategory.objects.get_or_create(
            name="Beverages",
            defaults={"description": "Refreshing drinks to complement your meal"}
        )
        
        # Create new category for special dishes
        special_dishes, _ = MenuCategory.objects.get_or_create(
            name="Special Dishes",
            defaults={"description": "Chef's special halal creations"}
        )
        
        # Create new category for sides
        sides, _ = MenuCategory.objects.get_or_create(
            name="Side Dishes",
            defaults={"description": "Perfect accompaniments to your main course"}
        )
        
        # Create new category for kids menu
        kids_menu, _ = MenuCategory.objects.get_or_create(
            name="Kids Menu",
            defaults={"description": "Delicious options for our younger guests"}
        )
        
        # Add more appetizers
        appetizer_items = [
            {
                "name": "Stuffed Grape Leaves",
                "description": "Grape leaves stuffed with rice, herbs, and spices",
                "price": 8.99,
                "is_halal": True
            },
            {
                "name": "Baba Ghanoush",
                "description": "Smoky eggplant dip with tahini, garlic, and lemon juice",
                "price": 7.99,
                "is_halal": True
            },
            {
                "name": "Fattoush Salad",
                "description": "Fresh vegetables with toasted pita bread and sumac dressing",
                "price": 9.99,
                "is_halal": True
            },
            {
                "name": "Spinach Fatayer",
                "description": "Savory pastries filled with spinach, onions, and spices",
                "price": 6.99,
                "is_halal": True
            },
            {
                "name": "Lentil Soup",
                "description": "Hearty lentil soup with Middle Eastern spices",
                "price": 5.99,
                "is_halal": True
            }
        ]
        
        # Add more main courses
        main_course_items = [
            {
                "name": "Lamb Tagine",
                "description": "Slow-cooked lamb with dried fruits, almonds, and aromatic spices",
                "price": 18.99,
                "is_halal": True
            },
            {
                "name": "Chicken Shawarma Plate",
                "description": "Marinated chicken slices served with rice, salad, and tahini sauce",
                "price": 15.99,
                "is_halal": True
            },
            {
                "name": "Beef Kofta Kebab",
                "description": "Grilled ground beef kebabs seasoned with herbs and spices",
                "price": 16.99,
                "is_halal": True
            },
            {
                "name": "Vegetable Couscous",
                "description": "Fluffy couscous topped with seasonal vegetables and chickpeas",
                "price": 13.99,
                "is_halal": True
            },
            {
                "name": "Grilled Fish",
                "description": "Fresh fish of the day grilled with herbs and served with saffron rice",
                "price": 19.99,
                "is_halal": True
            },
            {
                "name": "Chicken Tikka Masala",
                "description": "Tender chicken pieces in a creamy tomato sauce with Indian spices",
                "price": 16.99,
                "is_halal": True
            }
        ]
        
        # Add special dishes
        special_dish_items = [
            {
                "name": "Mixed Grill Platter",
                "description": "Assortment of grilled meats including lamb chops, chicken, and beef kebabs",
                "price": 24.99,
                "is_halal": True
            },
            {
                "name": "Whole Roasted Lamb",
                "description": "24-hour notice required. Whole lamb roasted with special spices (serves 8-10)",
                "price": 199.99,
                "is_halal": True
            },
            {
                "name": "Seafood Paella",
                "description": "Saffron rice with a variety of seafood, prepared halal-style",
                "price": 22.99,
                "is_halal": True
            },
            {
                "name": "Chef's Special Biryani",
                "description": "Fragrant rice dish with your choice of protein, garnished with fried onions and nuts",
                "price": 18.99,
                "is_halal": True
            }
        ]
        
        # Add side dishes
        side_dish_items = [
            {
                "name": "Saffron Rice",
                "description": "Aromatic basmati rice cooked with saffron",
                "price": 4.99,
                "is_halal": True
            },
            {
                "name": "Garlic Naan",
                "description": "Freshly baked flatbread with garlic and herbs",
                "price": 3.99,
                "is_halal": True
            },
            {
                "name": "Tabbouleh",
                "description": "Parsley salad with bulgur wheat, tomatoes, and mint",
                "price": 5.99,
                "is_halal": True
            },
            {
                "name": "Hummus with Pita",
                "description": "Creamy chickpea dip served with warm pita bread",
                "price": 5.99,
                "is_halal": True
            },
            {
                "name": "Grilled Vegetables",
                "description": "Seasonal vegetables grilled with olive oil and herbs",
                "price": 6.99,
                "is_halal": True
            }
        ]
        
        # Add kids menu items
        kids_menu_items = [
            {
                "name": "Mini Chicken Kebabs",
                "description": "Kid-sized chicken kebabs served with rice and vegetables",
                "price": 8.99,
                "is_halal": True
            },
            {
                "name": "Cheese Fatayer",
                "description": "Pastry triangles filled with cheese",
                "price": 6.99,
                "is_halal": True
            },
            {
                "name": "Pasta with Halal Meatballs",
                "description": "Pasta with halal beef meatballs in tomato sauce",
                "price": 7.99,
                "is_halal": True
            },
            {
                "name": "Chicken Fingers",
                "description": "Breaded halal chicken strips with fries",
                "price": 7.99,
                "is_halal": True
            }
        ]
        
        # Add more desserts
        dessert_items = [
            {
                "name": "Kunafa",
                "description": "Sweet cheese pastry soaked in sugar syrup",
                "price": 7.99,
                "is_halal": True
            },
            {
                "name": "Rice Pudding",
                "description": "Creamy rice pudding flavored with rose water and pistachios",
                "price": 5.99,
                "is_halal": True
            },
            {
                "name": "Basbousa",
                "description": "Semolina cake soaked in sweet syrup",
                "price": 6.99,
                "is_halal": True
            },
            {
                "name": "Halva",
                "description": "Sweet tahini-based confection with pistachios",
                "price": 5.99,
                "is_halal": True
            },
            {
                "name": "Fruit Platter",
                "description": "Seasonal fresh fruits",
                "price": 8.99,
                "is_halal": True
            }
        ]
        
        # Add more beverages
        beverage_items = [
            {
                "name": "Turkish Coffee",
                "description": "Strong coffee prepared in a traditional copper pot",
                "price": 3.99,
                "is_halal": True
            },
            {
                "name": "Ayran",
                "description": "Traditional yogurt drink",
                "price": 2.99,
                "is_halal": True
            },
            {
                "name": "Jallab",
                "description": "Sweet syrup made from dates, grape molasses, and rose water",
                "price": 3.99,
                "is_halal": True
            },
            {
                "name": "Fresh Orange Juice",
                "description": "Freshly squeezed orange juice",
                "price": 4.99,
                "is_halal": True
            },
            {
                "name": "Tamarind Drink",
                "description": "Sweet and tangy tamarind-based beverage",
                "price": 3.99,
                "is_halal": True
            },
            {
                "name": "Hibiscus Tea",
                "description": "Refreshing cold tea made from hibiscus flowers",
                "price": 3.99,
                "is_halal": True
            }
        ]
        
        # Function to add items to a category
        def add_items_to_category(category, items):
            for item_data in items:
                # Check if item already exists
                if not MenuItem.objects.filter(name=item_data["name"], category=category).exists():
                    MenuItem.objects.create(
                        name=item_data["name"],
                        description=item_data["description"],
                        price=item_data["price"],
                        category=category,
                        is_available=True,
                        is_halal=item_data["is_halal"]
                    )
                    self.stdout.write(f'Added {item_data["name"]} to {category.name}')
        
        # Add all items to their respective categories
        add_items_to_category(appetizers, appetizer_items)
        add_items_to_category(main_courses, main_course_items)
        add_items_to_category(special_dishes, special_dish_items)
        add_items_to_category(sides, side_dish_items)
        add_items_to_category(kids_menu, kids_menu_items)
        add_items_to_category(desserts, dessert_items)
        add_items_to_category(beverages, beverage_items)
        
        self.stdout.write(self.style.SUCCESS('Successfully added more food items to the menu!'))

