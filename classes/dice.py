import random

class Dice:
    @staticmethod
    def roll(sides=20):
        """Simulate dice roll"""
        return random.randint(1, sides)
    
    @staticmethod
    def roll_with_modifier(sides=20, modifier=0):
        """Roll with an additional modifier"""
        return Dice.roll(sides) + modifier