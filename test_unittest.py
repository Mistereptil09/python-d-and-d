import unittest
import json
from classes.effects import DamageOverTimeEffect, HealOverTimeEffect, StatModifierEffect, EffectManager
from classes.abilities import Ability

class Creature:
    def __init__(self, name, level, stats):
        self.name = name
        self.level = level
        self.stats = stats
        self.resources = {"mana": 100, "stamina": 100}
        self.effect_manager = EffectManager(self)

class TestEffects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('./classes/templates/effectsTemplates.json', 'r') as file:
            cls.templates = json.load(file)
        cls.creature = Creature(name="Hero", level=5, stats={"strength": 10, "intelligence": 8})

    def test_create_damage_over_time_effect(self):
        template = self.templates["DamageOverTimeEffect"]["Burning"]
        effect = DamageOverTimeEffect.create_effect("Burning", source_type="creature", applier=self.creature, potency_modifier=1.5)
        expected_potency = template["potency"] * 1.5 * (1 + sum(self.creature.stats.get(stat, 0) * modifier for stat, modifier in template.get("potency_modifier", {}).items()))
        self.assertEqual(effect.name, "Burning")
        self.assertEqual(effect.duration, template["duration"])
        self.assertEqual(effect.potency, expected_potency)
        self.assertEqual(effect.damage_type, template["damage_type"])
        self.assertEqual(effect.description, template["description"])

    def test_create_heal_over_time_effect(self):
        template = self.templates["HealOverTimeEffect"]["Regeneration"]
        effect = HealOverTimeEffect.create_effect("Regeneration", source_type="creature", applier=self.creature, potency_modifier=2.0)
        expected_potency = template["potency"] * 2.0 * (1 + sum(self.creature.stats.get(stat, 0) * modifier for stat, modifier in template.get("potency_modifier", {}).items()))
        self.assertEqual(effect.name, "Regeneration")
        self.assertEqual(effect.duration, template["duration"])
        self.assertEqual(effect.potency, expected_potency)
        self.assertEqual(effect.description, template["description"])

    def test_create_stat_modifier_effect(self):
        template = self.templates["StatModifierEffect"]["StrengthBoost"]
        effect = StatModifierEffect.create_effect("StrengthBoost", source_type="creature", applier=self.creature, potency_modifier=1.0)
        expected_potency = template["potency"] * 1.0 * (1 + sum(self.creature.stats.get(stat, 0) * modifier for stat, modifier in template.get("potency_modifier", {}).items()))
        self.assertEqual(effect.name, "StrengthBoost")
        self.assertEqual(effect.duration, template["duration"])
        self.assertEqual(effect.potency, expected_potency)
        self.assertEqual(effect.stat_to_modify, template["stat_to_modify"])
        self.assertEqual(effect.description, template["description"])

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

if __name__ == '__main__':
    unittest.main()