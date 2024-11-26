import json

def load_item_templates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
class Inventory:
    def __init__(self, max_weight):
        self.max_weight = max_weight
        self.items = []

    def add_item(self, item):
        if self.get_total_weight() + item.weight <= self.max_weight:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
        else:
            print(f"Cannot add {item.name} to inventory. Exceeds weight limit.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory.")
        else:
            print(f"{item.name} not found in inventory.")

    def get_total_weight(self):
        return sum(item.weight for item in self.items)

    def list_items(self):
        for item in self.items:
            print(f"{item.name} (Weight: {item.weight}, Defense: {getattr(item, 'defense', 'N/A')}, Attack: {getattr(item, 'attack', 'N/A')})")

class Armor:
    def __init__(self, name, defense, weight):
        self.name = name
        self.defense = defense
        self.weight = weight

class Weapon:
    def __init__(self, name, attack, weight):
        self.name = name
        self.attack = attack
        self.weight = weight

def create_item(item_class, template):
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