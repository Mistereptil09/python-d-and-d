from classes.ability import Ability

def create_ability(template):
    return Ability(
        name=template["name"],
        description=template["description"],
        damage=template["damage"],
        cost=template["cost"],
        cost_type=template["cost_type"],
        cooldown=template["cooldown"],
        damage_type=template["damage_type"],
        target_type=template["target_type"],
        effects=[(effect["effect_class"], effect["effect_name"]) for effect in template["effects"]],
        damage_modifiers=[(mod["stat"], mod["factor"]) for mod in template["damage_modifiers"]],
        effect_potency_modifiers={name: [(mod["stat"], mod["factor"]) for mod in mods] for name, mods in template["effect_potency_modifiers"].items()}
    )