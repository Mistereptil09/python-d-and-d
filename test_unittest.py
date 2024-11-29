import unittest
import json
from classes.effects import EffectManager, EffectFactory
from classes.abilities import Ability
from classes.inventory import Item, Armor, Weapon, Consumable

class Creature:
    def __init__(self, name, level = 10, stats = {}):
        self.name = name
        self.level = level
        self.stats = stats
        self.resources = {"mana": 100, "stamina": 100}
        self.effect_manager = EffectManager(self)

class TestEffects(unittest.TestCase):
    def setUp(self):
        self.creature = Creature(name="TestCreature", stats={"strength": 10, "wisdom": 5, "endurance": 8})

    def test_create_damage_over_time_effect(self):
        effect = EffectFactory.create_effect("DamageOverTimeEffect", "Burning", source_type="creature", applier=self.creature, potency_modifier=1.5)
        self.assertIsNotNone(effect)
        self.assertEqual(effect.name, "Burning")
        self.assertEqual(effect.duration, 3)
        self.assertEqual(effect.potency, 15)  # Assuming base potency is 10 and modifier is 1.5

    def test_create_heal_over_time_effect(self):
        effect = EffectFactory.create_effect("HealOverTimeEffect", "Regeneration", source_type="creature", applier=self.creature, potency_modifier=2.0)
        self.assertIsNotNone(effect)
        self.assertEqual(effect.name, "Regeneration")
        self.assertEqual(effect.duration, 3)
        self.assertEqual(effect.potency, 15)  # Assuming base potency is 7 and modifier is 2.0 with the stats modifier of the creature added

    def test_create_stat_modifier_effect(self):
        effect = EffectFactory.create_effect("StatModifierEffect", "Strength Boost", source_type="creature", applier=self.creature, potency_modifier=1.0)
        self.assertIsNotNone(effect)
        self.assertEqual(effect.name, "Strength Boost")
        self.assertEqual(effect.duration, 3)
        self.assertEqual(effect.potency, 3)
        self.assertEqual(effect.stat_to_modify, "strength")


class TestAbility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('./classes/templates/effectsTemplates.json', 'r') as file:
            cls.effect_templates = json.load(file)
        with open('./classes/templates/abilitiesTemplates.json', 'r') as file:
            cls.ability_templates = json.load(file)
        cls.creature = Creature(name="Hero", level=5, stats={"strength": 10, "intelligence": 8})

    def test_create_ability_with_damage_over_time_effect(self):
        template = self.ability_templates["Fireball"]
        ability = Ability.create_ability("Fireball", template)
        
        self.assertEqual(ability.name, "Fireball")
        self.assertEqual(ability.description, template["description"])
        self.assertEqual(ability.base_power, template["power"])
        self.assertEqual(ability.cost, template["cost"])
        self.assertEqual(ability.cost_type, template["cost_type"])
        self.assertEqual(ability.max_cooldown, template["cooldown"])
        self.assertEqual(ability.power_type, template["power_type"])
        self.assertEqual(ability.target_type, template["target_type"])
        
        # Check effects
        effect_template = ability.effects
        self.assertEqual(effect_template["effect_class"], "DamageOverTimeEffect")
        self.assertEqual(effect_template["effect_name"], "Burning")

    def test_create_ability_with_heal_over_time_effect(self):
        template = self.ability_templates["Regeneration"]
        ability = Ability.create_ability("Regeneration", template)
        
        self.assertEqual(ability.name, "Regeneration")
        self.assertEqual(ability.description, template["description"])
        self.assertEqual(ability.base_power, template.get("power", 0))
        self.assertEqual(ability.cost, template["cost"])
        self.assertEqual(ability.cost_type, template["cost_type"])
        self.assertEqual(ability.max_cooldown, template["cooldown"])
        self.assertEqual(ability.power_type, template["power_type"])
        self.assertEqual(ability.target_type, template["target_type"])
        
        # Check effects
        effect_template = ability.effects
        self.assertEqual(effect_template["effect_class"], "HealOverTimeEffect")
        self.assertEqual(effect_template["effect_name"], "Regeneration")

    def test_create_ability_with_stat_modifier_effect(self):
        template = self.ability_templates["StrengthBoost"]
        ability = Ability.create_ability("StrengthBoost", template)
        
        self.assertEqual(ability.name, "StrengthBoost")
        self.assertEqual(ability.description, template["description"])
        self.assertEqual(ability.base_power, template.get("power", 0))
        self.assertEqual(ability.cost, template["cost"])
        self.assertEqual(ability.cost_type, template["cost_type"])
        self.assertEqual(ability.max_cooldown, template["cooldown"])
        self.assertEqual(ability.power_type, template["power_type"])
        self.assertEqual(ability.target_type, template["target_type"])
        
        # Check effects
        effect_template = ability.effects
        self.assertEqual(effect_template["effect_class"], "StatModifierEffect")
        self.assertEqual(effect_template["effect_name"], "StrengthBoost")


class TestItemCreation(unittest.TestCase):
    def setUp(self):
        self.templates = {
            "Armor": {
                "head": {
                    "Helmet": {
                        "name": "Helmet",
                        "defense": 5,
                        "weight": 10,
                        "description": "A sturdy helmet."
                    }
                },
            },
            "Weapon": {
                "Sword": {
                    "name": "Sword",
                    "attack": 10,
                    "weight": 8,
                    "description": "A sharp sword."
                }
            },
            "Consumable": {
                "Health Potion": {
                    "name": "Health Potion",
                    "description": "Restores 50 health points.",
                    "weight": 1,
                    "power": 50,
                    "target": "self",
                    "is_damage": False,
                    "effect": [
                        {"type": "heal", "potency": 50}
                    ]
                }
            }
        }

    def test_create_armor(self):
        item = Item.create_item("Armor", "Helmet", self.templates)
        self.assertIsInstance(item, Armor)
        self.assertEqual(item.name, "Helmet")
        self.assertEqual(item.defense, 5)
        self.assertEqual(item.weight, 10)

    def test_create_weapon(self):
        item = Item.create_item("Weapon", "Sword", self.templates)
        self.assertIsInstance(item, Weapon)
        self.assertEqual(item.name, "Sword")
        self.assertEqual(item.attack, 10)
        self.assertEqual(item.weight, 8)

    def test_create_consumable(self):
        item = Item.create_item("Consumable", "Health Potion", self.templates)
        self.assertIsInstance(item, Consumable)
        self.assertEqual(item.name, "Health Potion")
        self.assertEqual(item.power, 50)
        self.assertEqual(item.weight, 1)

if __name__ == '__main__':
    unittest.main()