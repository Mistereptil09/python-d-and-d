class Effect:
    """
    Base class for all game effects
    """
    def __init__(self, name, duration, potency, description=None):
        self.name = name
        self.duration = duration  # Number of turns the effect lasts
        self.potency = potency  # Strength of the effect
        self.description = description
        self.active = True

    def apply(self, target):
        """
        Apply the effect to a target.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement apply method")

    def update(self, target):
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.duration -= 1
        
        if self.duration <= 0:
            self.active = False
        
        return self.active

    def __str__(self):
        return f"{self.name} (Duration: {self.duration}, Potency: {self.potency}, Description: {self.description}, Active: {self.active})"
    
class DamageOverTimeEffect(Effect):
    """
    An effect that deals damage each turn
    """
    def __init__(self, name, duration, potency, damage_type, description=None):
        super().__init__(name, duration, potency, description)
        self.damage_type = damage_type

    def apply(self, target):
        """
        Deal damage to the target creature each turn
        """        
        target.take_damage(self.potency, self.damage_type, "effect")
    
    def update(self, target):
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.apply(target)
            self.duration -= 1
            print(f"{self.name} deals {self.potency} {self.damage_type} damage to {target.name}. Duration left: {self.duration}")

        if self.duration <= 0:
            self.active = False
        
        return self.active

class HealOverTimeEffect(Effect):
    """
    An effect that heals the target each turn
    """
    def __init__(self, name, duration, potency, description=None):
        super().__init__(name, duration, potency, description)

    def apply(self, target):
        """
        Heal the target creature each turn
        """
        target.heal(self.potency)
    
    def update(self, target):
        """
        Update the effect's duration.
        Returns True if effect should continue, False if expired.
        """
        if self.duration > 0:
            self.apply(target)
            self.duration -= 1
            print(f"{self.name} heals {self.potency} HP for {target.name}. Duration left: {self.duration}")

        if self.duration <= 0:
            self.active = False
        
        return self.active
    
class StatModifierEffect(Effect):
    """
    An effect that temporarily modifies a creature's stats
    """
    def __init__(self, name, duration, potency, description=None, stat_to_modify=None):
        super().__init__(name, duration, potency, description)
        self.stat_to_modify = stat_to_modify
        self.applied = False

    def apply(self, target):
        """
        Apply the stat modification
        """
        if not self.applied:
            self.applied = True

            if hasattr(target, self.stat_to_modify):
                current_value = getattr(target, self.stat_to_modify)
                new_value = current_value + self.potency
                setattr(target, self.stat_to_modify, new_value)
                print(f"{self.stat_to_modify} modified by {self.potency} for {target.name}")
            else:
                print(f"{target} does not have a {self.stat_to_modify} stat")

    def remove(self, target):
        """
        Revert the stat modification
        """
        if hasattr(target, self.stat_to_modify) and self.applied:
            current_value = getattr(target, self.stat_to_modify)
            new_value = current_value - self.potency
            setattr(target, self.stat_to_modify, new_value)
            self.applied = False
            print(f"{self.stat_to_modify} reverted by {self.potency} for {target.name}")

    def update(self, target):
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
    def __init__(self, owner):
        self.owner = owner
        self.active_effects = []

    def add_effect(self, effect):
        """
        Add a new effect to the creature
        """
        self.active_effects.append(effect)
        effect.apply(self.owner)

    def remove_effect(self, effect):
        """
        Remove an effect from the creature
        """
        if effect in self.active_effects:
            self.active_effects.remove(effect)

    def update_effects(self):
        """
        Update all active effects and remove expired ones
        """
        for effect in self.active_effects[:]:
            if not effect.update(self.owner):
                self.remove_effect(effect)

    def get_effects(self):
        """
        Get the list of active effects
        """
        return self.active_effects
    