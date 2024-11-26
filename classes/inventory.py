import json
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from creature import Hero

# Function to load item templates from a JSON file
def load_item_templates(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)

# Class representing an inventory with a maximum weight limit
class Inventory:
    def __init__(self, max_weight: float):
        self.max_weight: float = max_weight  # Maximum weight the inventory can hold
        self.items: List[Union['Armor', 'Weapon']] = []  # List to store items

    # Method to add an item to the inventory
    def add_item(self, item: Union['Armor', 'Weapon']) -> None:
        if self.get_total_weight() + item.weight <= self.max_weight:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
        else:
            print(f"Cannot add {item.name} to inventory. Exceeds weight limit.")

    # Method to remove an item from the inventory
    def remove_item(self, item: Union['Armor', 'Weapon']) -> None:
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory.")
        else:
            print(f"{item.name} not found in inventory.")

    # Method to get the total weight of items in the inventory
    def get_total_weight(self) -> float:
        return sum(item.weight for item in self.items)

    # Method to list all items in the inventory
    def list_items(self) -> None:
        for item in self.items:
            print(f"{item.name} (Weight: {item.weight}, Defense: {getattr(item, 'defense', 'N/A')}, Attack: {getattr(item, 'attack', 'N/A')})")

# Class representing an armor item
class Armor:
    def __init__(self, name: str, defense: float, weight: float):
        self.name: str = name  # Name of the armor
        self.defense: float = defense  # Defense value of the armor
        self.weight: float = weight  # Weight of the armor

# Class representing a weapon item
class Weapon:
    def __init__(self, name: str, attack: float, weight: float):
        self.name: str = name  # Name of the weapon
        self.attack: float = attack  # Attack value of the weapon
        self.weight: float = weight  # Weight of the weapon

# Function to create an item (Armor or Weapon) from a template
def create_item(item_class: str, template: dict) -> Union[Armor, Weapon]:
    if item_class == "Armor":
        return Armor(
            name=template["name"],
            defense=template["defense"],
            weight=template["weight"]
        )
    elif item_class == "Weapon":
        return Weapon(
            name=template["name"],
            attack=template["attack"],
            weight=template["weight"]
        )
    else:
        raise ValueError(f"Unknown item class: {item_class}")