import os
import re

filepath = 'app/src/main/java/com/shiva/quickMart/viewmodel/MainViewModel.kt'

with open(filepath, 'r') as f:
    content = f.read()

# Replace images
replacements = {
    '1560806887-1e4cd0b6fac6': '1619546813926-a78fa6372cd2', # Apple
    '1566478989037-e924e50cb792': '1621852004158-f3bc188ace2d', # Chips
    '1572804013309-8c9959d0e2db': '1585653040134-4538ec2f004f', # Popcorn
    '1622483767028-3f66f32aef97': '1600271886742-f049cd451bba', # Orange juice (first one)
    '1555507036-ab1e4006aa24': '1530610476181-d83430b64dcb', # Croissant
    '1557925923-b6dc240a2a53': '1607958996333-41aef7caefaa', # Muffins
}

for old, new in replacements.items():
    content = content.replace(old, new)

# For beverages, we have 3 identical IDs: "1600271886742-f049cd451bba" now (since it was replaced).
# Let's fix Beverage section specifically:
# Beverage 1 (Orange Juice) -> 1600271886742-f049cd451bba
# Beverage 2 (Cola) -> 1622483767028-3f66f32aef97
# Beverage 3 (Energy Drink) -> 1622543925917-763c34d1a86e

# Let's just do a manual string replace on the whole Beverage block
old_beverage_block = """        // Beverages
        Product(13, "Orange Juice", "Beverages", 110.0, "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=300&q=80"),
        Product(14, "Cola", "Beverages", 40.0, "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=300&q=80"),
        Product(15, "Energy Drink", "Beverages", 120.0, "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=300&q=80"),"""

new_beverage_block = """        // Beverages
        Product(13, "Orange Juice", "Beverages", 110.0, "https://images.unsplash.com/photo-1600271886742-f049cd451bba?auto=format&fit=crop&w=300&q=80"),
        Product(14, "Cola", "Beverages", 40.0, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=300&q=80"),
        Product(15, "Energy Drink", "Beverages", 120.0, "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?auto=format&fit=crop&w=300&q=80"),"""

content = content.replace(old_beverage_block, new_beverage_block)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated MainViewModel.kt with distinct URLs.")
