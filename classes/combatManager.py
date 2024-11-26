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

    def resolve_turn(self, active_combatant, chosen_action):
        """Execute a single turn"""
        action_result = chosen_action.execute()
        # Additional logging or game state updates