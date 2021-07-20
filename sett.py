import uuid

from units.unit import Unit
from synergies import Brawler
from synergies import Draconic

class Sett(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=0,
            total_mana=50,
            armor=35,
            magic_resist=35,
            attack_damage=70,
            attack_speed=0.7,
            attack_range=1,
            image_name='sett',
            synergies=[Brawler, Draconic],
            **kwargs,
        )
        self.cast_time = 0.6
        self.cast_row = None
        self.cast_col = None
        self.cast_pos_row = None
        self.cast_pos_col = None

    def can_cast_spell(self, map, time):
        return super().can_cast_spell(map, time) and self.current_target and self.current_target.distance(self.row, self.col) <= 1

    def cast_spell(self, map, time):
        super().cast_spell(map, time)
        self.cast_row, self.cast_col = self.current_target.row, self.current_target.col
        self.cast_pos_row, self.cast_pos_col = self.row, self.col

    def get_haymaker_ad_ratio_damage(self):
        return {
            1: 1.7,
            2: 1.85,
            3: 2.0
        }[max(1, self.star_level)]

    def get_haymaker_damage(self):
        return self.get_attack_damage() * self.get_haymaker_ad_ratio_damage()

    def get_haymaker_armor_reduction(self):
        base_armor_reduction = {
            1: 20,
            2: 25,
            3: 30
        }[max(1, self.star_level)]
        return base_armor_reduction * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        for unit in map.units:
            if unit.team == self.team:
                continue
            if ((unit.row == self.cast_row and unit.col == self.cast_col) or
                (
                    unit.distance(self.cast_row, self.cast_col) <= 1 and
                    unit.distance(self.cast_pos_row, self.cast_pos_col) == 2
                )):
                unit.flat_bonus_armor_modifiers.add_component(uuid.uuid4(), time, 10, -self.get_haymaker_armor_reduction())
                self.deal_physical_damage(unit, self.get_haymaker_damage(), is_multitarget=True)
