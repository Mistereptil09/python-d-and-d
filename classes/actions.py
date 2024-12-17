from abilities import Ability

class Action:
    def __init__(self, performer, target):
        self.performer = performer
        self.target = target
    
    def execute(self):
        """Abstract method to be implemented by subclasses"""
        raise NotImplementedError("Each action must implement its execution")
    
    def list_possible_actions(self):
        """List possible actions for the performer"""
        return []
    
    def list_characters(self):
        """List characters that can be targeted"""
        return []

class AbilityAction(Action):
    def __init__(self, performer, target, ability: Ability):
        super().__init__(performer, target)
        self.ability = ability
    
    def execute(self):
        """Execute the ability on the target"""
        if self.ability.is_offensive:
            damage = self.ability.calculate_power(self.performer)
            self.target.take_damage(damage)
        else:
            heal = self.ability.calculate_power(self.performer)
            self.target.heal(heal)
        # Apply effects if any
        for effect in self.ability.effects:
            self.target.apply_effect(effect)

class DefendAction(Action):
    def execute(self):
        """Increase the performer's defense for a turn"""
        self.performer.defend()

class WaitAction(Action):
    def execute(self):
        """Skip the turn"""
        pass

class UseItemAction(Action):
    def __init__(self, performer, target, item):
        super().__init__(performer, target)
        self.item = item
    
    def execute(self):
        """Use an item on the target"""
        self.item.use(self.target)