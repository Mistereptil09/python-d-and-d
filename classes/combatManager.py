from actions import AbilityAction, DefendAction, WaitAction, UseItemAction

class CombatManager:
    def __init__(self, heroes, monsters):
        self.heroes = heroes
        self.monsters = monsters
        self.turn_order = self.calculate_initiative_order()
    
    def calculate_initiative_order(self):
        """Sort all combatants by initiative"""
        all_combatants = self.heroes + self.monsters
        return sorted(all_combatants, key=lambda x: x.initiative, reverse=True)
    
    def is_combat_over(self):
        """Check if combat has ended"""
        heroes_alive = any(hero.is_alive for hero in self.heroes)
        monsters_alive = any(monster.is_alive for monster in self.monsters)
        return not (heroes_alive and monsters_alive)
    
    def get_next_turn(self):
        """Cycle through turn order"""
        for combatant in self.turn_order:
            if combatant.is_alive:
                yield combatant

    def resolve_turn(self, active_combatant):
        """Execute a single turn"""
        chosen_action = self.select_action(active_combatant)
        action_result = chosen_action.execute()
        # Additional logging or game state updates

    def select_action(self, combatant):
        """Select an action for the combatant"""
        # Example logic for selecting an action
        if combatant.is_hero:
            # Hero selects an action (e.g., from player input)
            return self.player_select_action(combatant)
        else:
            # Monster AI selects an action
            return self.monster_select_action(combatant)

    def player_select_action(self, hero):
        """Player selects an action for the hero"""
        # Placeholder for player input logic
        # Example: return AbilityAction(hero, target, ability)
        pass

    def monster_select_action(self, monster):
        """AI selects an action for the monster"""
        # Placeholder for AI logic
        # Example: return AbilityAction(monster, target, ability)
        pass

    def start_combat(self):
        """Start the combat loop"""
        while not self.is_combat_over():
            for combatant in self.get_next_turn():
                self.resolve_turn(combatant)