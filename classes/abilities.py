# this file contains the Ability class and related functions
from classes.effects import DamageOverTimeEffect, HealOverTimeEffect, StatModifierEffect
import json
import logging
from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from creature import Creature

try:
    with open('classes/templates/abilitiesTemplates.json', 'r') as file:
        TEMPLATES = json.load(file)
except FileNotFoundError:
    logging.error("Abilities templates file not found.")
    TEMPLATES = {}
except json.JSONDecodeError:
    logging.error("Error decoding JSON from abilities templates file.")
    TEMPLATES = {}

effect_classes = {
    "DamageOverTimeEffect": DamageOverTimeEffect,
    "HealOverTimeEffect": HealOverTimeEffect,
    "StatModifierEffect": StatModifierEffect
}

# Custom exception for ability-related errors
class AbilityError(Exception):
    """Custom exception for ability-related errors."""
    def __init__(self, name, message):
        super().__init__(f"AbilityError: {name}: {message}")

class Ability:
    def __init__(self, 
        name: str, 
        description: str, 
        is_offensive: bool = True,
        power: int = 0,  # Renamed from damage to power to handle both healing and damage
        cost: int = 0, 
        cost_type: str = 'mana', # 'mana', 'stamina', etc.
        cooldown: int = 0, 
        power_type: str = 'physical', # Renamed from damage_type to power_type to handle both healing and damage
        target_type: str = 'single', # 'single', 'area', 'self', 'all'
        effects: List[Dict[str, Any]] = None,
        power_modifiers: List[tuple] = None,  # Renamed from damage_modifiers to power_modifiers to handle both healing and damage
        effect_multiplier: float = 1.0):
        self.name: str = name
        self.description: str = description
        self.base_power: int = power  # Renamed from base_damage to base_power to handle both healing and damage
        self.power_type: str = power_type  # Renamed from damage_type to power_type to handle both healing and damage
        self.cost: int = cost
        self.cost_type: str = cost_type
        self.max_cooldown: int = cooldown
        self.current_cooldown: int = 0
        self.target_type: str = target_type
        self.effect_multiplier: float = effect_multiplier
        self.effects: List[Dict[str, Any]] = effects or []
        self.power_modifiers: List[tuple] = power_modifiers or []  # Renamed from damage_modifiers to power_modifiers to handle both healing and damage

    @classmethod
    def create_ability(cls, name, template: dict) -> 'Ability':
        """
        Create an ability from a template.
        """
        effects = template.get("effects", [])
        if effects is []:
            logging.info("effect are not found for effect", name)
        return cls(
            name=name,
            description=template["description"],
            is_offensive=template.get("is_offensive", True),
            power=template.get("power", 0),
            cost=template.get("cost", 0),
            cost_type=template.get("cost_type", 'mana'),
            cooldown=template.get("cooldown", 0),
            power_type=template.get("power_type", 'physical'),
            target_type=template.get("target_type", 'single'),
            effects=effects,
            power_modifiers=template.get("power_modifiers", []),   
            effect_multiplier=template.get("effect_multiplier", 1.0)
        )

    def can_use(self, user: 'Creature', target: 'Creature') -> bool:
        """
        Handles checks to determine if the ability can be used.
        Raises AbilityError if the ability cannot be used.
        """
        if target is None:
            raise AbilityError(self.name, "No target provided")
        
        elif self.target_type == 'self' and target != user:
            raise AbilityError(self.name, "Ability can only target self")
        
        elif self.target_type == 'single' and target is user:
            raise AbilityError(self.name, "Ability cannot target self")

        elif user.resources.get(self.cost_type, 0) < self.cost and self.current_cooldown > 0:
            raise AbilityError(self.name, f"Insufficient {self.cost_type} ({self.cost} required) and Ability is on cooldown ({self.current_cooldown} turns left)")
        
        elif user.resources.get(self.cost_type, 0) < self.cost:
            raise AbilityError(self.name, f"Insufficient {self.cost_type} ({self.cost} required)")
        
        elif self.current_cooldown > 0:
            raise AbilityError(self.name, f"Ability is on cooldown ({self.current_cooldown} turns left)")
        
        return True
    
    def use(self, user: 'Creature', target: 'Creature') -> int:
        """
        Use the ability on the target.
        Reduces user's resources, applies damage or heal (depends wether the effect is agressive) and effects, and sets cooldown.
        Returns the actual damage dealt.
        """
        self.can_use(user, target)
        user.resources[self.cost_type] -= self.cost
        power = 0
        if self.base_power != 0:
            power = self.calculate_power(user)
            try:
                if self.is_offensive:
                    target.take_damage(self.power_type, power)
                else:
                    target.heal(power)
            except AttributeError as e:
                logging.error(f"Error using ability {self.name}: {e}")
        for effect_template in self.effects:
            effect_class_name = effect_template["effect_class"]
            effect_class = effect_classes.get(effect_class_name)
            if effect_class:
                created_effect = effect_class.create_effect(
                    name=effect_template["effect_name"],
                    source_type="creature",
                    applier=user,
                    potency_modifier=self.effect_multiplier
                )
                if created_effect:
                    target.effect_manager.add_effect(created_effect)
                else:
                    logging.error(f"Failed to create effect {effect_template['effect_name']} for ability {self.name}")
            else:
                logging.error(f"Effect class {effect_class_name} not found for ability {self.name}")
        self.current_cooldown = self.max_cooldown
        return power

    def calculate_power(self, user: 'Creature') -> int:
        """
        Calculate ability power based on user's stats.
        Returns the calculated power.
        """
        modifier = 1.0
        
        # Apply each modifier from the list
        for stat, factor in self.power_modifiers:
            if hasattr(user, stat):
                modifier += getattr(user, stat) * factor
        
        return int(self.base_power * modifier)

    def update_cooldown(self, specific_cooldown: int = None) -> None:
        """
        Reduce cooldown each turn or set to a specific value.
        """
        if specific_cooldown is not None:
            self.current_cooldown = specific_cooldown
        elif self.current_cooldown > 0:
            self.current_cooldown -= 1