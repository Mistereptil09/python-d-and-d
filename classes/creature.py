from classes.effects import EffectManager
from classes.inventory import Inventory, EquipmentManager
from classes.abilities import Ability

import random
from abc import ABC
import json
import logging


class Creature(ABC):
    def __init__(
        self, 
        name: str = "rien", 
        level: int = 0, 
        description: str = "c'est vide et ça devrais pas...", 
        hp: int = 0, 
        max_hp: int = 0, 
        defense: int = 10, 
        initiative: int = 10, 
        abilities: list = None, 
        damage_type: str = 'physical', 
        resistances: list = None, 
        weaknesses: list = None, 
        max_attack: int = 10, 
        min_attack: int = 1):
        
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
            ability.name for ability in self.abilities 
            if ability.cost_type in self.resources and ability.cost <= self.resources[ability.cost_type] and ability.current_cooldown == 0
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
    def __init__(        self, 
        name: str = "rien", 
        level: int = 0, 
        description: str = "c'est vide et ça devrais pas...", 
        hp: int = 0, 
        max_hp: int = 0, 
        defense: int = 10, 
        initiative: int = 10, 
        abilities: list = None, 
        damage_type: str = 'physical', 
        resistances: list = None, 
        weaknesses: list = None, 
        max_attack: int = 10, 
        min_attack: int = 1, 
        exp: int = 0, 
        hero_class: str = None, 
        max_weight: int = 100):
        
        # Call parent constructor with updated parameters
        super().__init__(name=name, 
                         level=level, 
                         description=description, 
                         hp=hp, 
                         max_hp=max_hp, 
                         defense=defense, 
                         initiative=initiative, 
                         max_attack=max_attack, 
                         min_attack=min_attack, 
                         damage_type=damage_type, 
                         abilities=abilities, 
                         resistances=resistances, 
                         weaknesses=weaknesses)
        
        self.hero_class: str = hero_class
        self.exp: int = exp
        self.max_weight: int = max_weight
        self.inventory: 'Inventory' = Inventory(self.max_weight)
        self.equipment_manager: EquipmentManager = EquipmentManager()
        self.exp: int = exp
        
    @classmethod   
    def create_hero(cls, name, hero_class, TEMPLATES):
        
        try:
            template = TEMPLATES[hero_class]
        except:
            logging.error(f"Ability template not found for {hero_class}.")
        
        print("Templates : ", TEMPLATES)
        print("template : ", template)
        hero = template.get(hero_class, [])
        if hero is []:
            logging.warning("Class not found : ", hero_class)
            hero = Hero() # initialisez a Dummy hero
            return hero
        else:
            max_weight = template["max_weight"]
            equipment_manager=EquipmentManager()
            inventory = Inventory(max_weight)
            
            equipment_manager.equip_item(template["Weapon"])
            inventory.add_item(template["Weapon"])
            for armor_piece in template["Armor"]:
                equipment_manager.equip_item(armor_piece)
                inventory.add_item(armor_piece)
            return cls (
                name=name, 
                level=1, 
                description=template["description"], 
                hp=template["max_hp"], 
                max_hp=template["max_hp"], 
                defense=template["defense"], 
                initiative=template["initiative"], 
                max_attack=template["max_attack"], 
                min_attack=template["min_attack"], 
                damage_type='physical', 
                abilities=template["abilities"], 
                resistances=template["resistances"], 
                weaknesses=template["weaknessses"],
                hero_class=hero_class,
                exp=0,
                max_weight=max_weight,
                inventory=inventory,
                equipment_manager=equipment_manager
            )
            


class Monster(Creature):
    def __init__(        self, 
        name: str = "rien", 
        level: int = 0, 
        description: str = "c'est vide et ça devrais pas...", 
        hp: int = 0, 
        max_hp: int = 0, 
        defense: int = 10, 
        initiative: int = 10, 
        abilities: list = None, 
        damage_type: str = 'physical', 
        resistances: list = None, 
        weaknesses: list = None, 
        max_attack: int = 10, 
        min_attack: int = 1,
        xp: int = 0,
        monster_type: str = None,
        drop_table: dict = None):
        
        # Call parent constructor with updated parameters
        super().__init__(
            name=name,
            level=level,
            description=description,
            hp=hp,
            max_hp=max_hp,
            defense=defense,
            initiative=initiative,
            max_attack=max_attack,
            min_attack=min_attack,
            damage_type=damage_type,
            abilities=abilities,
            resistances=resistances,
            weaknesses=weaknesses)
        
        # Monster-specific attributes
        self.monster_type: str = monster_type
        self.xp: int = xp
        self.drop_table: dict = drop_table or {}

    def drop_loot(self) -> list:
        """
        Drop loot based on drop table
        """
        loot = []
        for item, chance in self.drop_table.items():
            if random.random() < chance:
                loot.append(item)
        return loot
