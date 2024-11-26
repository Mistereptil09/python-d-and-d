class Action:
    def __init__(self, performer, target):
        self.performer = performer
        self.target = target
    
    def execute(self):
        """Abstract method to be implemented by subclasses"""
        raise NotImplementedError("Each action must implement its execution")
    
    def listPossibleActions(self):
        """List possible actions for the performer"""
        return []
    
    def listCharacters(self):
        """List characters that can be targeted"""
        return []

class AttackAction(Action):
    def __init__(self, performer, target, weapon=None):
        super().__init__(performer, target)
        self.weapon = weapon
    
    def calculate_hit_chance(self):
        """Calculate probability of successful attack"""
        # Consider performer's skills, target's defense, etc.
        pass
    
    def calculate_damage(self):
        """Calculate damage based on weapon, skills, etc."""
        base_damage = self.performer.maxAttack
        if self.weapon:
            base_damage += self.weapon.damage
        return base_damage

    def execute(self):
        hit_probability = self.calculate_hit_chance()
        if hit_probability > 0.5:  # Simplified hit check
            damage = self.calculate_damage()
            self.target.take_damage(damage)
            return True
        return False

class HealAction(Action):
    def __init__(self, performer, target, heal_amount):
        super().__init__(performer, target)
        self.heal_amount = heal_amount
    
    def execute(self):
        """Heal the target"""
        max_heal = self.heal_amount
        self.target.hp = min(self.target.hp + max_heal, self.target.max_hp)

class BuffAction(Action):
    def __init__(self, performer, target, effect):
        super().__init__(performer, target)
        self.effect = effect
    
    def execute(self):
        """Apply a buff effect to the target"""
        self.target.add_status(self.effect)