from units.unit import Unit
from synergies import Spellweaver
from synergies import Forgotten

# DEPRECATED
class Viktor(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=30,
            total_mana=70,
            armor=20,
            magic_resist=20,
            attack_damage=45,
            attack_speed=0.65,
            attack_range=4,
            image_name='viktor',
            synergies=[Spellweaver, Forgotten],
            **kwargs,
        )
        self.damage_at = None
        self.cast_time = 0.4

    def get_siphon_power_damage(self):
        base_damage = {
            1: 300,
            2: 500,
            3: 850
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_siphon_power_shield(self):
        base_shield = {
            1: 150,
            2: 250,
            3: 425
        }[max(1, self.star_level)]
        return base_shield * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        if not self.current_target:
            print('viktor no target bug')
            return
        self.deal_magic_damage(self.current_target, self.get_siphon_power_damage())
        shield_targets = sorted(
            [u for u in map.units if u.team == self.team],
            key=lambda u: self.current_target.distance(u.row, u.col)
        )[:3]
        for shield_target in self.shield_targets:
            shield_target.add_shield_effect(self.get_siphon_power_shield(), 5)