from classes.effects import EffectManager

class Creature:
    def __init__(self, name: str, level: int, description: str, hp: int, max_hp: int = None, defense: int = 10, initiative: int = 10, abilities: list = None, damage_type: str = 'physical', resistances: list = None, weaknesses: list = None, max_attack: int = 10, min_attack: int = 1):
        # Initialize basic attributes
        self.name: str = name
        self.level: int = level
        self.description: str = description
        
        # HP management
        self.max_hp: int = max_hp or hp
        self.hp: int = hp
        
        # Combat stats
        self.defense: int = defense
        self.initiative: int = initiative
        self.max_attack: int = max_attack
        self.min_attack: int = min_attack
        self.damage_type: str = damage_type
        self.resistances: list = resistances or []
        self.weaknesses: list = weaknesses or []
        
        # Abilities and effects
        self.abilities: list = abilities or []
        self.is_alive: bool = True
        
        # Effect management
        self.effect_manager: EffectManager = EffectManager(self)
        
        # Additional tracking
        self.resources: dict = {
            'mana': 100,
            'stamina': 100
        }

    def take_damage(self, damage: int, damage_type: str = None, source: str = None) -> None:
        """
        Sophisticated damage calculation with defense and resistances
        """
        # Calculate damage multiplier based on target's resistances
        multiply_damage = self.mutlitply_power(damage_type)

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

        # Verify if creature is still alive
        if self.hp <= 0:
            self.is_alive = False

    def heal(self, heal: int, heal_type: str) -> int:
        """
        Heal the creature
        """
        multiply_heal = self.mutlitply_power(heal_type)

        self.hp = min(self.hp + heal * multiply_heal, self.max_hp)
    
    def mutlitply_power(self, power_type: str) -> float:
        """
        Calculate damage multiplier based on target's resistances
        """
        # If has damage type as weakness and resistance, return 1.0 multiplier
        if (hasattr(self, 'resistances') and power_type in self.resistances) and (hasattr(self, 'weaknesses') and power_type in self.weaknesses):
            return 1.0
        # If has damage type as resistance, return 0.5 multiplier
        elif hasattr(self, 'resistances') and power_type in self.resistances:
            return 0.5
        # If has damage type as weakness, return 1.5 multiplier
        elif hasattr(self, 'weaknesses') and power_type in self.weaknesses:
            return 1.5
        # If none of the above, return 1.0
        return 1.0
    
    def get_available_actions(self) -> list:
        """
        Return possible actions based on current state
        Updated to work with our new Ability class
        """
        return [
            ability for ability in self.abilities 
            if ability.can_use(self)
        ]

    def learn_ability(self, ability) -> None:
        """
        Add a new ability to the creature's repertoire
        """
        self.abilities.append(ability)

    def update_turn(self) -> None:
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
    def __init__(self, name: str, level: int, description: str, hp: int, max_hp: int, defense: int, initiative: int, abilities: list, damage_type: str, resistances: list, weaknesses: list, max_attack: int, min_attack: int, exp: int = 0, hero_class: str = None, off_weapon = None, weapon = None, inventory: list = None):
        # Call parent constructor with updated parameters
        super().__init__(name=name, level=level, description=description, hp=hp, max_hp=max_hp, defense=defense, initiative=initiative, max_attack=max_attack, min_attack=min_attack, damage_type=damage_type, abilities=abilities,resistances=resistances,weaknesses=weaknesses)
        self.hero_class: str = hero_class
        self.weapon = weapon
        self.off_weapon = off_weapon
        self.inventory: list = inventory
        self.exp: int = exp

class Monster(Creature):
    def __init__(self, name: str, level: int, description: str, hp: int, max_hp: int, defense: int, initiative: int, abilities: list, damage_type: str, resistances: list, weaknesses: list, max_attack: int, min_attack: int, xp: int = 0, monster_type: str = None):
        
        # Call parent constructor with updated parameters
        super().__init__(name=name, level=level, description=description, hp=hp, max_hp=max_hp, defense=defense, initiative=initiative, max_attack=max_attack, min_attack=min_attack, damage_type=damage_type, abilities=abilities,resistances=resistances,weaknesses=weaknesses)
        
        # Monster-specific attributes
        self.monster_type: str = monster_type
        self.xp: int = xp
