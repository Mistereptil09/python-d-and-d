from useEffectTemplates import create_effect, load_effect_templates
import json

def load_ability_templates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

effect_templates = load_effect_templates('effectTemplates.json')

class AbilityError(Exception):
    """Custom exception for ability-related errors."""
    def __init__(self, name, message):
        super().__init__(f"AbilityError: {name}: {message}")

class Ability:
    def __init__(self, 
                 name, 
                 description, 
                 damage=0, 
                 cost=0, 
                 cost_type='mana', # 'mana', 'stamina', etc.
                 cooldown=0, 
                 damage_type='physical', # 'physical', 'magical', etc.
                 target_type='single', # 'single', 'area', 'self', 'all'
                 effects=None,
                 damage_modifiers=None,
                 effect_potency_modifiers=None):
        self.name = name
        self.description = description
        self.base_damage = damage
        self.damage_type = damage_type
        self.cost = cost
        self.cost_type = cost_type
        self.max_cooldown = cooldown
        self.current_cooldown = 0
        self.target_type = target_type
        self.effects = effects or []
        self.damage_modifiers = damage_modifiers or []  # List of (stat, factor) tuples
        self.effect_potency_modifiers = effect_potency_modifiers or {}  # Dict of effect name to list of (stat, factor) tuples

    def can_use(self, user, target):
        """
        Handles checks to determine if the ability can be used
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
    
    def use(self, user, target):
        self.can_use(user, target)
        user.resources[self.cost_type] -= self.cost
        damage = self.calculate_damage(user)
        actual_damage = target.take_damage(damage)
        for effect_class, effect_name in self.effects:
            potency_modifier = self.calculate_effect_potency(user, effect_name)
            effect_template = effect_templates[effect_class][effect_name]
            effect_instance = create_effect(effect_class, effect_template, potency_modifier)
            target.effect_manager.add_effect(effect_instance)
        self.current_cooldown = self.max_cooldown
        return actual_damage


    def calculate_damage(self, user):
        """
        Calculate ability damage based on user's stats
        """
        modifier = 1.0
        
        # Apply each modifier from the list
        for stat, factor in self.damage_modifiers:
            if hasattr(user, stat):
                modifier += getattr(user, stat) * factor
        
        return int(self.base_damage * modifier)

    def calculate_effect_potency(self, user, effect_name):
        """
        Calculate effect potency multiplier based on user's stats
        """
        potency_multiplier = 1.0
        
        # Apply each modifier from the list
        for stat, factor in self.effect_potency_modifiers.get(effect_name, []):
            if hasattr(user, stat):
                potency_multiplier += getattr(user, stat) * factor
        
        return int(potency_multiplier)


    def update_cooldown(self, specific_cooldown=None):
        """
        Reduce cooldown each turn
        """
        if specific_cooldown is not None:
            self.current_cooldown = specific_cooldown
        elif self.current_cooldown > 0:
            self.current_cooldown -= 1