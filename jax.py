import uuid

from units.unit import Unit
from synergies import Skirmisher
from synergies import Ironclad

class Jax(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=900,
            starting_mana=0,
            total_mana=20,
            armor=50,
            magic_resist=50,
            attack_damage=80,
            attack_speed=0.9,
            attack_range=1,
            image_name='jax',
            synergies=[Ironclad, Skirmisher],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_empowered_strike_ad_ratio_damage(self):
        return {
            1: 2,
            2: 2.2,
            3: 3
        }[max(1, self.star_level)]

    def get_empowered_strike_damage(self):
        return self.get_attack_damage() * self.get_empowered_strike_ad_ratio_damage()

    def get_empowered_strike_bonus_attack_speed_ratio(self):
        base_ad_ratio = {
            1: 0.3,
            2: 0.35,
            3: 1
        }[max(1, self.star_level)]
        return base_ad_ratio * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        if not self.current_target:
            return
        if self.current_target.distance(self.row, self.col) > 1:
            row, col = self.current_target.closest_empty_tile(map, closest_from_row=self.row, closest_from_col=self.col)
            self.move_to(row, col, time, 0.1)
        self.deal_physical_damage(self.current_target, self.get_empowered_strike_damage())
        self.base_attack_speed_bonus_ratio_modifiers.add_component(
            uuid.uuid4(), time, 9999, self.get_empowered_strike_bonus_attack_speed_ratio()
        )