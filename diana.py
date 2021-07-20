import utils

from units.unit import Unit
from synergies import Nightbringer
from synergies import Assassin

class Diana(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=70,
            total_mana=140,
            armor=40,
            magic_resist=40,
            attack_damage=75,
            attack_speed=0.7,
            attack_range=1,
            image_name='diana',
            synergies=[Nightbringer, Assassin],
            **kwargs,
        )
        self.cast_time = 0.5

    def get_moonfall_damage(self):
        base_damage = {
            1: 300,
            2: 450,
            3: 2000
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_moonfall_stun_duration(self):
        return {
            1: 2,
            2: 2.5,
            3: 4
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        for unit in map.units:
            if unit.team != self.team and unit.distance(self.row, self.col) <= 2:
                unit.stun(time, self.get_moonfall_stun_duration())
                self.deal_magic_damage(unit, self.get_moonfall_damage())
                sym_row = unit.row + (self.row - unit.row) * 2
                if sym_row < 0: sym_row = 0
                if sym_row > 7: sym_row = 7
                sym_col = unit.col + (self.col - unit.col) * 2
                if sym_col < 0: sym_col = 0
                if sym_col > 6: sym_col = 6

                tr, tc = utils.closest_empty_tile_from_pos(sym_row, sym_col, map, closest_from_row=self.row, closest_from_col=self.col)
                unit.move_to(tr, tc, time, 0.1)