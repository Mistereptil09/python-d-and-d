import json
import logging
from typing import List, Union, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from creature import Creature

try:
    with open('classes/templates/items.json', 'r') as file:
        TEMPLATES = json.load(file)
except FileNotFoundError:
    logging.error("Effects templates file not found.")
    TEMPLATES = {}
except json.JSONDecodeError:
    logging.error("Error decoding JSON from effects templates file.")
    TEMPLATES = {}

logging.basicConfig(level=logging.INFO)

class Inventory:
    def __init__(self, max_weight: float):
        """
        Initialize an inventory with a maximum weight limit.

        :param max_weight: Maximum weight the inventory can hold.
        """
        self.max_weight: float = max_weight
        self.items: List[Union['Armor', 'Weapon', 'Item']] = []

    def add_item(self, item: Union['Armor', 'Weapon', 'Item']) -> None:
        """
        Add an item to the inventory if it does not exceed the weight limit.

        :param item: Item to be added (Armor or Weapon).
        """
        if self.can_add_item(item):
            self.items.append(item)
            logging.info(f"Added {item.name} to inventory.")
        else:
            logging.warning(f"Cannot add {item.name} to inventory. Exceeds weight limit.")

    def remove_item(self, item: Union['Armor', 'Weapon', 'Item']) -> None:
        """
        Remove an item from the inventory.

        :param item: Item to be removed (Armor or Weapon).
        """
        if item in self.items:
            self.items.remove(item)
            logging.info(f"Removed {item.name} from inventory.")
        else:
            logging.warning(f"{item.name} not found in inventory.")

    def get_total_weight(self) -> float:
        """
        Get the total weight of items in the inventory.

        :return: Total weight of items.
        """
        return sum(item.weight for item in self.items)

    def list_items(self) -> None:
        """
        List all items in the inventory.
        """
        for item in self.items:
            logging.info(f"{item.name} (Weight: {item.weight}, Defense: {getattr(item, 'defense', 'N/A')}, Attack: {getattr(item, 'attack', 'N/A')})")

    def can_add_item(self, item: Union['Armor', 'Weapon', 'Item']) -> bool:
        """
        Check if an item can be added to the inventory without exceeding the weight limit.

        :param item: Item to be checked (Armor or Weapon).
        :return: True if the item can be added, False otherwise.
        """
        return self.get_total_weight() + item.weight <= self.max_weight

class Item:
    def __init__(self, name: str, weight: float, description: str = None):
        """
        Initialize an item.

        :param name: Name of the item.
        :param weight: Weight of the item.
        """
        self.name: str = name
        self.weight: float = weight
        self.description: str = description

    @classmethod
    def create_item(cls, item_type: str, name: str, template: Dict[str, Dict[str, Union[str, float, int]]]) -> 'Item':
        """
        Create an item from a template.

        :param item_type: Type of the item (e.g., 'Armor', 'Weapon', 'Consumable').
        :param name: Name of the item.
        :param template: Template dictionary containing item attributes.
        :return: Created item.
        """
        try:
            # Adjust to search through nested dictionaries for Armor items
            if item_type == 'Armor':
                for category, items in template[item_type].items():
                    if name in items:
                        item_template = items[name]
                        break
                else:
                    raise KeyError
            else:
                item_template = template[item_type][name]
        except KeyError:
            logging.error(f"Item template not found for {item_type} with name {name}.")
            return None

        if item_type == 'Armor':
            return Armor(
                name=name,
                defense=item_template["defense"],
                weight=item_template["weight"],
                description=item_template["description"],
                category=category
            )
        elif item_type == 'Weapon':
            return Weapon(
                name=name,
                attack=item_template["attack"],
                weight=item_template["weight"],
                description=item_template["description"]
            )
        elif item_type == 'Consumable':
            return Consumable(
                name=name,
                weight=item_template["weight"],
                description=item_template["description"],
                power=item_template.get("power", 0),
                target=item_template.get("target"),
                is_damage=item_template.get("is_damage", False),
                is_energy=item_template.get("is_energy", False),
                energy_type=item_template.get("energy_type"),
                effect=item_template.get("effect", [])
            )
        else:
            logging.error(f"Unknown item type: {item_type}")
            return None
                
class Armor(Item):
    def __init__(self, name: str, weight: float, description : str, defense: float, category : str = None):
        """
        Initialize an armor item.

        :param name: Name of the armor.
        :param defense: Defense value of the armor.
        :param weight: Weight of the armor.
        """
        super().__init__(name, weight, description)
        self.defense: float = defense
        self.category: str = category

class Weapon(Item):
    def __init__(self, name: str, weight: float, description : str, attack: float):
        """
        Initialize a weapon item.

        :param name: Name of the weapon.
        :param attack: Attack value of the weapon.
        :param weight: Weight of the weapon.
        """
        super().__init__(name, weight, description)
        self.attack: float = attack
        
class Consumable(Item):
    def __init__(self, name: str, weight: float, description: str, power : int = 0, target : 'Creature' = None, is_damage : bool = False, is_energy : bool = False, energy_type : str = None, effect: List[Dict[str, str]] = None):
        """
        Initialize a consumable item.

        :param name: Name of the consumable.
        :param description: Description of the consumable.
        :param weight: Weight of the consumable.
        :param effect: List of effects as tuples (effect type, potency).
        """
        super().__init__(name, weight, description)
        self.power: int = power
        self.target : 'Creature' = target
        self.is_damage : bool = is_damage
        self.is_energy : bool = is_energy
        self.energy_type : str = energy_type
        self.effect: List[Dict[str, str]] = effect or []
        
class EquipmentManager:
    """
    Equipement Manager class to handle equipping and unequipping items.
    """
    def __init__(self):
        self.equipped_items: Dict[str, Union[Armor, Weapon]] = {
            "head": None,
            "chest": None,
            "legs": None,
            "weapon": None
        }
        
    def equip_item(self, item: Union[Armor, Weapon]) -> None:
        """
        Equip an item.

        :param item: Item to be equipped.
        """
        if isinstance(item, Armor):
            if item.category in self.equipped_items:
                self.equipped_items[item.category] = item
            else:
                logging.error(f"Unknown armor category: {item.category}")
                return
        elif isinstance(item, Weapon):
            self.equipped_items["weapon"] = item
        else:
            logging.error(f"Item type not supported: {type(item)}")
            return
        logging.info(f"Equipped {item.name}")

    def unequip_item(self, slot: str) -> None:
        """
        Unequip an item from a specific slot.

        :param slot: Slot to unequip the item from.
        """
        if slot in self.equipped_items and self.equipped_items[slot] is not None:
            logging.info(f"Unequipped {self.equipped_items[slot].name}")
            self.equipped_items[slot] = None

    def get_equipped_items(self) -> Dict[str, Union[Armor, Weapon]]:
        """
        Get the currently equipped items.

        :return: Dictionary of equipped items.
        """
        return self.equipped_items

if __name__ == "__main__":
    # Example usage:
    TEMPLATES = {
        "Armor": {
            "head": {
                "Helmet": {
                    "name": "Helmet",
                    "weight": 5,
                    "defense": 5,
                    "description": "A simple helmet."
                },
            },
            "chest": {
                "Chainmail": {
                    "name": "Chainmail",
                    "weight": 10,
                    "defense": 10,
                    "description": "A suit of chainmail."
                },
            },
        },
        "Weapon": {
            "Sword": {
                "name": "Sword",
                "attack": 10,
                "weight": 8,
                "description": "A sharp sword."
            }
        }
    }

    # Create items
    helmet = Item.create_item("Armor", "Helmet", TEMPLATES)
    chestplate = Item.create_item("Armor", "Chainmail", TEMPLATES)
    sword = Item.create_item("Weapon", "Sword", TEMPLATES)

    # Equip items
    equipment = EquipmentManager()
    equipment.equip_item(helmet)
    equipment.equip_item(chestplate)
    equipment.equip_item(sword)

    # Get equipped items
    equipped_items = equipment.get_equipped_items()

    # Print equipped items
    for slot, item in equipped_items.items():
        if item:
            print(f"{slot.capitalize()}: {item.name}")
        else:
            print(f"{slot.capitalize()}: None")

