from classes.effects import EffectManager

class Creature:
    def __init__(self, name, level, description, hp, max_hp=None, defense=10, initiative=10, abilities=None, damage_type='physical', resistances=None, weaknesses=None, max_attack=10, min_attack=1):
        self.name = name
        self.level = level
        self.description = description
        
        # HP management
        self.max_hp = max_hp or hp
        self.hp = hp
        
        # Combat stats
        self.defense = defense
        self.initiative = initiative
        self.max_attack = max_attack
        self.min_attack = min_attack
        self.damage_type = damage_type
        self.resistances = resistances or []
        self.weaknesses = weaknesses or []
        
        # Abilities and effects
        self.abilities = abilities or []
        self.is_alive = True
        
        # Effect management
        self.effect_manager = EffectManager(self)
        
        # Additional tracking
        self.resources = {
            'mana': 100,
            'stamina': 100
        }

    def take_damage(self, damage, damage_type=None, source=None):
        """
        Sophisticated damage calculation with defense and resistances
        """
        # calculate damage multiplier based on target's resistances
        multiply_damage = self.mutlitply_damage(damage_type)

        # Apply damage multiplier
        multipled_damage = int(damage * multiply_damage)
        # Apply damage reduction from defense if not from effect
        if source == "effect":
            print("source is effect")
            actual_damage = max(multipled_damage, 0)
        else:
            actual_damage = max(multipled_damage - self.defense, 0)
        
        # Apply damage to HP
        self.hp = max(self.hp - actual_damage, 0)

        # verify if creature is still alive
        if self.hp <= 0:
            self.is_alive = False
        return
        
    def mutlitply_damage(self, damage_type):
        """
        Calculate damage multiplier based on target's resistances
        """
        # if has damage type as weakness and resistance, return 1.0 mutliplier
        if (hasattr(self, 'resistances') and damage_type in self.resistances) and (hasattr(self, 'weaknesses') and damage_type in self.weaknesses):
            return 1.0
        # if has damage type as resistance, return 0.5 mutliplier
        elif hasattr(self, 'resistances') and damage_type in self.resistances:
            return 0.5
        # if has damage type as weakness, return 1.5 mutliplier
        elif hasattr(self, 'weaknesses') and damage_type in self.weaknesses:
            return 1.5
        # if none of the above, return 1.0
        return 1.0

    def heal(self, amount):
        """
        Heal the creature
        """
        self.hp = min(self.hp + amount, self.max_hp)
        return amount

    def get_available_actions(self):
        """
        Return possible actions based on current state
        Updated to work with our new Ability class
        """
        return [
            ability for ability in self.abilities 
            if ability.can_use(self)
        ]

    def learn_ability(self, ability):
        """
        Add a new ability to the creature's repertoire
        """
        self.abilities.append(ability)

    def update_turn(self):
        """
        Called at the start or end of each turn
        Manages effects and ability cooldowns
        """
        self.effect_manager.update_effects()
        
        # Update cooldowns for abilities
        if self.abilities != []:
            print("updating cooldowns")
                
            for ability in self.abilities:
                print("ability: ", ability.name, "cooldown: ", ability.current_cooldown)
                if hasattr(ability, 'update_cooldown'):
                    ability.update_cooldown()


class Hero(Creature):
    def __init__(self, name, level, description, hp, max_hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, exp=0, hero_class=None, off_weapon=None, weapon=None, inventory=None):
        super().__init__(name=name, level=level, description=description, hp=hp, max_hp=max_hp, defense=defense, initiative=initiative, max_attack=max_attack, min_attack=min_attack, damage_type=damage_type, abilities=abilities,resistances=resistances,weaknesses=weaknesses)
        self.hero_class = hero_class
        self.weapon = weapon
        self.off_weapon = off_weapon
        self.inventory = inventory
        self.exp = exp

class Monster(Creature):
    def __init__(self, name, level, description, hp, max_hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, xp=0, monster_type=None):
        
        # Call parent constructor with updated parameters
        super().__init__(name=name, level=level, description=description, hp=hp, max_hp=max_hp, defense=defense, initiative=initiative, max_attack=max_attack, min_attack=min_attack, damage_type=damage_type, abilities=abilities,resistances=resistances,weaknesses=weaknesses)
        
        # Monster-specific attributes
        self.monster_type = monster_type
        self.xp = xp