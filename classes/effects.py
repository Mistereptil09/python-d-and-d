import json
import logging
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from creature import Creature

try:
    with open('classes/templates/effectsTemplates.json', 'r') as file:
        TEMPLATES = json.load(file)
except FileNotFoundError:
    logging.error("Effects templates file not found.")
    TEMPLATES = {}
except json.JSONDecodeError:
    logging.error("Error decoding JSON from effects templates file.")
    TEMPLATES = {}

class Effect:
    """
    Base class for all game effects
    """
    def __init__(self, name: str, duration: int, potency: int, description: str = None):
        # Initialize effect attributes
        self.name: str = name
        self.duration: int = duration  # Number of turns the effect lasts
        self.potency: int = potency  # Strength of the effect
        self.description: str = description
        self.active: bool = True    
    
    def apply(self, target: 'Creature') -> None:
        """
        Apply the effect to a target.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement apply method")

    def update(self, target: 'Creature') -> bool:
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.duration -= 1
        
        if self.duration <= 0:
            self.active = False
        
        return self.active
    

    def __str__(self) -> str:
        return f"{self.name} (Duration: {self.duration}, Potency: {self.potency}, Description: {self.description}, Active: {self.active})"
    

class DamageOverTimeEffect(Effect):
    """
    An effect that deals damage each turn
    """
    def __init__(self, name: str, duration: int, potency: int, damage_type: str, description: str = None):
        super().__init__(name, duration, potency, description)
        self.damage_type: str = damage_type
        
    def apply(self, target: 'Creature') -> None:
        """
        Deal damage to the target creature each turn
        """        
        try:
            target.take_damage(self.potency, self.damage_type, "effect")
        except AttributeError:
            logging.error(f"Target {target} does not have a take_damage method.")
    
    def update(self, target: 'Creature') -> bool:
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.apply(target)
            self.duration -= 1
            logging.info(f"{self.name} deals {self.potency} {self.damage_type} damage to {target.name}. Duration left: {self.duration}")

        if self.duration <= 0:
            self.active = False

        return self.active
    

class HealOverTimeEffect(Effect):
    """
    An effect that heals the target each turn
    """
    def __init__(self, name: str, duration: int, potency: int, description: str = None):
        super().__init__(name, duration, potency, description)
    
    def apply(self, target: 'Creature') -> None:
        """
        Heal the target creature each turn
        """
        try:
            target.heal(self.potency)
        except AttributeError:
            logging.error(f"Target {target} does not have a heal method.")
    
    def update(self, target: 'Creature') -> bool:
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.apply(target)
            self.duration -= 1
            logging.info(f"{self.name} heals {self.potency} HP for {target.name}. Duration left: {self.duration}")

        if self.duration <= 0:
            self.active = False
        
        return self.active
    

class StatModifierEffect(Effect):
    """
    An effect that temporarily modifies a creature's stats
    """
    def __init__(self, name: str, duration: int, potency: int, description: str = None, stat_to_modify: str = None):
        super().__init__(name, duration, potency, description)
        self.stat_to_modify: str = stat_to_modify
        self.applied: bool = False

    def apply(self, target: 'Creature') -> None:
        """
        Apply the stat modification
        """
        if not self.applied:
            self.applied = True

            if hasattr(target, self.stat_to_modify):
                current_value = getattr(target, self.stat_to_modify)
                new_value = current_value + self.potency
                setattr(target, self.stat_to_modify, new_value)
                logging.info(f"{self.stat_to_modify} modified by {self.potency} for {target.name}")
            else:
                logging.error(f"{target} does not have a {self.stat_to_modify} stat")

    def remove(self, target: 'Creature') -> None:
        """
        Revert the stat modification
        """
        if hasattr(target, self.stat_to_modify) and self.applied:
            current_value = getattr(target, self.stat_to_modify)
            new_value = current_value - self.potency
            setattr(target, self.stat_to_modify, new_value)
            self.applied = False
            logging.info(f"{self.stat_to_modify} reverted by {self.potency} for {target.name}")

    def update(self, target: 'Creature') -> bool:
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.duration -= 1
        
        elif self.duration <= 0:
            self.remove(target)
            self.active = False
        
        return self.active
    

class EffectManager:
    """
    Manages effects for a creature
    """
    def __init__(self, owner: 'Creature'):
        self.owner: 'Creature' = owner
        self.active_effects: list[Effect] = []

    def add_effect(self, effect: Effect) -> None:
        """
        Add a new effect to the creature
        """
        if effect:
            self.active_effects.append(effect)
            effect.apply(self.owner)

    def remove_effect(self, effect: Effect) -> None:
        """
        Remove an effect from the creature
        """
        if effect in self.active_effects:
            self.active_effects.remove(effect)

    def update_effects(self) -> None:
        """
        Update all active effects and remove expired ones
        """
        for effect in self.active_effects[:]:
            if not effect.update(self.owner):
                self.remove_effect(effect)

    def get_effects(self) -> list[Effect]:
        """
        Get the list of active effects
        """
        return self.active_effects

class EffectFactory:
    @staticmethod
    def create_effect(effect_type: str, name: str, source_type: str, applier: 'Creature' = None, potency_modifier: float = 1.0) -> Union['Effect', None]:
        """
        Create an effect from a template.

        :param effect_type: Type of the effect (e.g., 'DamageOverTimeEffect', 'HealOverTimeEffect', 'StatModifierEffect').
        :param name: Name of the effect.
        :param source_type: Source type of the effect (e.g., 'creature', 'environment').
        :param applier: The creature applying the effect.
        :param potency_modifier: Modifier to adjust the potency of the effect.
        :return: Created effect.
        """
        try:
            template = TEMPLATES[effect_type][name]
        except KeyError:
            logging.error(f"Effect template not found for {effect_type} with name {name}.")
            return None

        base_potency = template["potency"]

        if source_type == "creature" and applier:  # effect comes from a creature
            # Apply player and stats multipliers
            stats = applier.stats
            stats_multiplier = 1 + sum(stats.get(stat, 0) * modifier for stat, modifier in template.get("potency_modifier", {}).items())
            final_potency = int(base_potency * potency_modifier * stats_multiplier)
        else:  # effect comes from the world / environment / item
            final_potency = base_potency * potency_modifier

        if effect_type == 'DamageOverTimeEffect':
            return DamageOverTimeEffect(
                name=name,
                duration=template["duration"],
                potency=final_potency,
                damage_type=template["damage_type"],
                description=template.get("description")
            )
        elif effect_type == 'HealOverTimeEffect':
            return HealOverTimeEffect(
                name=name,
                duration=template["duration"],
                potency=final_potency,
                description=template.get("description")
            )
        elif effect_type == 'StatModifierEffect':
            return StatModifierEffect(
                name=name,
                duration=template["duration"],
                potency=final_potency,
                stat_to_modify=template["stat_to_modify"],
                description=template.get("description")
            )
        else:
            logging.error(f"Unknown effect type: {effect_type}")
            return None