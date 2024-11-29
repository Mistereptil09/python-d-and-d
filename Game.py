import json
from classes.creature import Hero, Monster
from classes.abilities import Ability
from classes.inventory import Item, Inventory, EquipmentManager

def load_templates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_hero(name, level, description, hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, exp, hero_class):
    hero = Hero(name, level, description, hp, hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, exp, hero_class)
    return hero

def create_monster(name, level, description, hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, xp, monster_type, drop_table):
    monster = Monster(name, level, description, hp, hp, defense, initiative, abilities, damage_type, resistances, weaknesses, max_attack, min_attack, xp, monster_type, drop_table)
    return monster

# Load templates
abilities_templates = load_templates('classes/templates/abilitiesTemplates.json')
items_templates = load_templates('classes/templates/items.json')
effects_templates = load_templates('classes/templates/effectsTemplates.json')

# Create heroes and monsters
hero = create_hero("HeroName", 1, "A brave hero", 100, 10, 10, [], 'physical', [], [], 10, 1, 0, "Warrior")
monster = create_monster("MonsterName", 1, "A scary monster", 50, 5, 5, [], 'physical', [], [], 5, 1, 10, "Goblin", {})

# Assign abilities
fireball = Ability.create_ability("Fireball", abilities_templates)
hero.learn_ability(fireball)

