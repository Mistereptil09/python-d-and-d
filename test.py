from classes.effects import DamageOverTimeEffect, HealOverTimeEffect, StatModifierEffect
from classes.creature import Hero, Monster
from classes.ability import Ability


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def test_damage_over_time_effect():
    """
    test_damage_over_time_effect on a creature: Hero
    """
    damage = 15
    duration = 3
    try:
        # Create Hero
        hero = Hero(
            name="Aragorn",
            level=5,
            description="A brave warrior",
            hp=100,
            max_hp=100,
            defense=10,
            initiative=15,
            max_attack=20,
            min_attack=10,
            damage_type="physical",
            resistances=["fire"],
            weaknesses=["ice"],
            abilities=["Slash", "Parry"],
            weapon="Sword",
            off_weapon="Shield",
            inventory=["Potion", "Bandage"],
            hero_class="Warrior",
        )
        
        # Create Damage Over Time Effect
        poison_effect = DamageOverTimeEffect(
            name="Poison",
            duration=duration,
            potency=damage,
            damage_type="poison"
        )
        
        # Apply poison effect to hero
        hero.effect_manager.add_effect(poison_effect)
        
        # Simulate turns and check HP reduction
        initial_hp = hero.hp
        for turn in range(3):
            hero.update_turn()
            expected_hp = initial_hp - damage * (turn + 1)
            print(f"Turn {turn + 1}: Expected HP {expected_hp}, got {hero.hp}")
            assert hero.hp == expected_hp, f"Turn {turn + 1}: Expected HP {expected_hp}, got {hero.hp}"
        
        # Ensure effect is removed after duration
        assert len(hero.effect_manager.get_effects()) == 0, "Poison effect should expire after 3 turns\n"
        print_colored("Damage over Time Effect test passed for Hero!\n", "32")  # Green text
    except AssertionError as e:
        print_colored(f"Test failed: {e}", "31")  # Red text

def test_heal_over_time_effect():
    """
    test_heal_over_time_effect on a creature: Hero
    """

    try:
        # Create Hero
        hero = Hero(
            name="Aragorn",
            level=5,
            description="A brave warrior",
            hp=100,
            max_hp=100,
            defense=10,
            initiative=15,
            max_attack=20,
            min_attack=10,
            damage_type="physical",
            resistances=["fire"],
            weaknesses=["ice"],
            abilities=["Slash", "Parry"],
            weapon="Sword",
            off_weapon="Shield",
            inventory=["Potion", "Bandage"],
            hero_class="Warrior",
        )
        
        # Create Heal Over Time Effect
        regen_effect = HealOverTimeEffect(
            name="Regeneration",
            duration=3,
            potency=10
        )
        
        # Apply heal effect to hero
        hero.effect_manager.add_effect(regen_effect)
        
        # Simulate turns and check HP increase
        initial_hp = hero.hp
        for turn in range(3):
            hero.update_turn()
            expected_hp = min(initial_hp + 10 * (turn + 1), hero.max_hp)
            assert hero.hp == expected_hp, f"Turn {turn + 1}: Expected HP {expected_hp}, got {hero.hp}"
        
        # Ensure effect is removed after duration
        assert len(hero.effect_manager.get_effects()) == 0, "Regeneration effect should expire after 3 turns\n"
        print_colored("Heal Over Time Effect test passed for Hero!\n", "32")  # Green text
    except AssertionError as e:
        print_colored(f"Test failed: {e}", "31")  # Red text

def test_stat_modifier_effect():
    """
    test_stat_modifier_effect on a creature: Monster
    """

    initial_defense = 15
    bonus_defense = 5
    duration = 2
    turns = 3

    try:
        # Create Monster
        monster = Monster(
            name="bigbizard",
            level=5,
            description="A brave bizzard",
            hp=100,
            max_hp=100,
            defense=initial_defense,
            initiative=15,
            max_attack=20,
            min_attack=10,
            damage_type="physical",
            resistances=["fire"],
            weaknesses=["ice"],
            abilities=["Slash", "Parry"],
            xp=0,
            monster_type="Orc"
        )
        
        # Create Stat Modifier Effect
        defense_buff = StatModifierEffect(
            name="Defense Buff",
            duration=duration,
            stat_to_modify="defense",
            potency=bonus_defense
        )
        print("Initial defense: ", monster.defense)  # Should print: Initial defense: 15

        # Apply the effect
        monster.effect_manager.add_effect(defense_buff)
        expected_defense = initial_defense + bonus_defense  # 20
        
        # Simulate turns and check defense increase
        for turn in range(turns):
            monster.update_turn()
            print(f"Turn {turn + 1}: Defense: {monster.defense}")
            if turn < duration:
                assert monster.defense == expected_defense, f"Turn {turn + 1}: Expected Defense {expected_defense}, got {monster.defense}"
            else:
                assert monster.defense == initial_defense, f"Turn {turn + 1}: Expected Defense {initial_defense}, got {monster.defense}"
        
        print_colored("Stat Modifier Effect test passed for Monster!", "32")  # Green text

    except AssertionError as e:
        print_colored(f"Test failed: {e}", "31")  # Red text

def test_ability_use():
    # Create a user with some attributes
    user = Hero(
        name="Aragorn",
        level=5,
        description="A brave warrior",
        hp=100,
        max_hp=100,
        defense=10,
        initiative=15,
        max_attack=20,
        min_attack=10,
        damage_type="physical",
        resistances=["fire"],
        weaknesses=["ice"],
        abilities=[],
        weapon="Sword",
        off_weapon="Shield",
        inventory=["Potion", "Bandage"],
        hero_class="Warrior",
    )

    # Create a target with some health
    target = Monster(
        name="Monster",
        level=5,
        description="A fierce monster",
        hp=100,
        max_hp=100,
        defense=5,
        initiative=10,
        max_attack=15,
        min_attack=5,
        damage_type="physical",
        resistances=["ice"],
        weaknesses=["fire"],
        abilities=[],
        xp=0,
        monster_type="Orc"
    )

    # Create an ability with multiple effects and modifiers
    fireball = Ability(
        name="Fireball", 
        description="A fiery ball of magic", 
        damage=30, 
        cost=20, 
        cost_type="mana", 
        cooldown=3, 
        effects=[("DamageOverTimeEffect", "Burning"), ("HealOverTimeEffect", "Regeneration")], 
        damage_modifiers=[("strength", 0.1), ("intelligence", 0.05)],
        effect_potency_modifiers={
            "Burning": [("strength", 0.1), ("intelligence", 0.05)],
            "Regeneration": [("intelligence", 0.1)]
        }
    )
    
    # Add the ability to the hero
    user.learn_ability(fireball)
    
    # Use the ability
    damage = fireball.use(user, target)
    print(f"Used {fireball.name} on {target.name}, dealing {damage} damage.")
    
    # Output the target's remaining health
    print(f"{target.name} has {target.hp} health left.")
    
    # Check the effects applied to the target
    for effect in target.effect_manager.get_effects():
        print(f"Effect: {effect.name}, Duration: {effect.duration}, Potency: {effect.potency}")

    for i in range(3):
        user.update_turn()
        target.update_turn()
        print(f"Turn {i + 1}: {target.name} has {target.hp} health left.")


# Run the tests
#test_damage_over_time_effect()
#test_heal_over_time_effect()
#test_stat_modifier_effect()
test_ability_use()