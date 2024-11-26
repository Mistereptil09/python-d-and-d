# ----------------- Weapon Class Definition -----------------
class Weapon:
    def __init__(self, name, damage, durability, damageType):
        self.name = name
        self.damage = damage
        self.durability = durability
        self.damageType = damageType