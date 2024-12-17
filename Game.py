import json
from classes.creature import Hero, Monster
from classes.abilities import Ability
from classes.inventory import Item, Inventory, EquipmentManager

def load_templates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Load templates
abilities_templates = load_templates('classes/templates/abilitiesTemplates.json')
items_templates = load_templates('classes/templates/items.json')
effects_templates = load_templates('classes/templates/effectsTemplates.json')
hero_templates = load_templates('classes/templates/heroTemplate.json')

# Create heroes and monsters
hero = Hero("HeroName", 1, "A Small new hero", 100, 100, 10, 10, ["Fireball"], 'physical', [], [], 10, 1, 0, "Warrior", 100)
hero2 = Hero()
goblin = Monster("GoblinSama", 1, "A small goblin", 50, 50, 5, 5, [], 'physical', [], [], 5, 1, 10, "Goblin", {})
orc = Monster("OrcSama", 1, "A small orc", 75, 75, 7, 7, [], 'physical', [], [], 7, 2, 15, "Orc", {})
heroTemplate = Hero.create_hero('Jean Luc', "Warior", hero_templates)
# Assign abilities
fireball = Ability.create_ability("Fireball", abilities_templates)
hero.learn_ability(fireball)
print(hero.abilities)
print(hero.inventory.items)
print(hero.equipment_manager.equipped_items)
print(hero2.get_available_actions())
print(hero2.name)
print(hero2.level)
print(hero2.description)
print(hero2.hp)
print(hero2.max_hp)
print(hero2.defense)
print(hero2.initiative)
print(hero2.abilities)
print(hero2.damage_type)
print(hero2.resistances)
print(hero2.weaknesses)
print(hero2.max_attack)
print(hero2.min_attack)
print(hero2.exp)
print(hero2.hero_class)
print(hero2.max_weight)
print(hero2.inventory)
print(hero2.equipment_manager)
print(hero2.exp)
