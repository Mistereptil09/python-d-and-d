import json
import logging
from typing import List, Union, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from creature import Creature

logging.basicConfig(level=logging.INFO)

def load_item_templates(file_path: str) -> dict:
    """
    Load item templates from a JSON file.

    :param file_path: Path to the JSON file.
    :return: Dictionary of item templates.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        return {}

class Inventory:
    def __init__(self, max_weight: float):
        """
        Initialize an inventory with a maximum weight limit.

        :param max_weight: Maximum weight the inventory can hold.
        """
        self.max_weight: float = max_weight
        self.items: List[Union['Armor', 'Weapon']] = []

    def add_item(self, item: Union['Armor', 'Weapon', ]) -> None:
        """
        Add an item to the inventory if it does not exceed the weight limit.

        :param item: Item to be added (Armor or Weapon).
        """
        if self.can_add_item(item):
            self.items.append(item)
            logging.info(f"Added {item.name} to inventory.")
        else:
            logging.warning(f"Cannot add {item.name} to inventory. Exceeds weight limit.")

    def remove_item(self, item: Union['Armor', 'Weapon']) -> None:
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

    def can_add_item(self, item: Union['Armor', 'Weapon']) -> bool:
        """
        Check if an item can be added to the inventory without exceeding the weight limit.

        :param item: Item to be checked (Armor or Weapon).
        :return: True if the item can be added, False otherwise.
        """
        return self.get_total_weight() + item.weight <= self.max_weight

class Armor:
    def __init__(self, name: str, defense: float, weight: float):
        """
        Initialize an armor item.

        :param name: Name of the armor.
        :param defense: Defense value of the armor.
        :param weight: Weight of the armor.
        """
        self.name: str = name
        self.defense: float = defense
        self.weight: float = weight

class Weapon:
    def __init__(self, name: str, attack: float, weight: float):
        """
        Initialize a weapon item.

        :param name: Name of the weapon.
        :param attack: Attack value of the weapon.
        :param weight: Weight of the weapon.
        """
        self.name: str = name
        self.attack: float = attack
        self.weight: float = weight

class Consumable:
    def __init__(self, name: str, description: str, weight: float, power, target = self, effect: List[Tuple[str, int]] = None):
        """
        Initialize a consumable item.

        :param name: Name of the consumable.
        :param description: Description of the consumable.
        :param weight: Weight of the consumable.
        :param effect: List of effects as tuples (effect type, potency).
        """
        self.name: str = name
        self.description: str = description
        self.weight: float = weight
        self.effect: List[Tuple[str, int]] = effect or []
        self.power: int = power
        self.target : Creature = target

def create_item(item_class: str, template: dict) -> Union[Armor, Weapon]:
    """
    Create an item (Armor or Weapon) from a template.

    :param item_class: Class of the item ("Armor" or "Weapon").
    :param template: Template dictionary containing item attributes.
    :return: Created item (Armor or Weapon).
    :raises ValueError: If the item class is unknown.
    """
    if item_class == "Consumable":
        return Consumable(
            name=template["name"],
            description=template["description"],
            weight=template["weight"],
            power=template["power"],
            effect=template["effect"]
        )
    elif item_class == "Armor":
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
    
