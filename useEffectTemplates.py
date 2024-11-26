import json
from classes.effects import DamageOverTimeEffect, HealOverTimeEffect, StatModifierEffect

def load_effect_templates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_effect(effect_class, template, potency_modifier=1.0):
    if effect_class == "DamageOverTimeEffect":
        return DamageOverTimeEffect(
            name=template["name"],
            duration=template["duration"],
            potency=template["potency"] * potency_modifier,
            damage_type=template["damage_type"],
            description=template.get("description")
        )
    elif effect_class == "HealOverTimeEffect":
        return HealOverTimeEffect(
            name=template["name"],
            duration=template["duration"],
            potency=template["potency"] * potency_modifier,
            description=template.get("description")
        )
    elif effect_class == "StatModifierEffect":
        return StatModifierEffect(
            name=template["name"],
            duration=template["duration"],
            potency=template["potency"] * potency_modifier,
            stat_to_modify=template["stat_to_modify"],
            description=template.get("description")
        )
    else:
        raise ValueError(f"Unknown effect class: {effect_class}")
    
# effect_templates = load_effect_templates('effectTemplates.json')
# effect_class = "DamageOverTimeEffect"
# effect_name = "Burning"
# template = effect_templates[effect_class][effect_name]
# potency_modifier = 1.0  # This can be calculated based on user stats
# effect_instance = create_effect(effect_class, template, potency_modifier)
# print(effect_instance.name)  # Output: Burning
# print(effect_instance.potency)  # Output: 5