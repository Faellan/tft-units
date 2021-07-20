import random

from units.unit import Unit
from synergies import Revenant
from synergies import Abomination
from synergies import Mystic

class Fiddlesticks(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=800,
            starting_mana=50,
            total_mana=125,
            armor=40,
            magic_resist=40,
            attack_damage=60,
            attack_speed=0.75,
            attack_range=2,
            image_name='fiddlesticks',
            synergies=[Revenant, Abomination, Mystic],
            **kwargs,
        )
        self.cast_time = 1
        self.ticks_remaining = 0
        self.next_tick_at = None
        self.is_first_tick = False
        self.tp_range = 3
        self.spell_range = 2

    def get_crowstorm_damage(self):
        base_damage = {
            1: 175,
            2: 225,
            3: 600
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    # TODO: scale with AP ?
    def get_crowstorm_heal_ratio(self):
        return {
            1: 0.25,
            2: 0.25,
            3: 0.25
        }[max(1, self.star_level)]

    def get_crowstorm_base_duration(self):
        return {
            1: 5,
            2: 5,
            3: 5
        }[max(1, self.star_level)]

    # on cast instead of perform to tp under revive
    def cast_spell(self, map, time):
        super().cast_spell(map, time)
        self.next_tick_at = time + self.cast_time
        self.ticks_remaining = self.get_crowstorm_base_duration()  # TODO: +/- 1 ?
        self.is_first_tick = True

    def perform_spell(self, map, time):
        pass  # nothing to do

    def crowstorm_tp(self, map, time):
        best_row, best_col, best_score = None, None, None

        pos = []
        for row in range(8):
            for col in range(7):
                if map.is_tile_empty(row, col) and self.distance(row, col) <= self.tp_range:
                    pos.append((row, col))
        random.shuffle(pos)

        for (row, col) in pos:
            score = len([u for u in map.units if u.team != self.team and u.distance(row, col) <= self.spell_range])
            if best_score is None or score > best_score:
                best_row, best_col, best_score = row, col, score

        self.move_to(best_row, best_col, time, 0.1)

    def tick(self, map, time):
        super().tick(map, time)
        if self.ticks_remaining and self.next_tick_at and time >= self.next_tick_at:
            if self.is_first_tick:
                self.crowstorm_tp(map, time)
                self.is_first_tick = False
            self.ticks_remaining -= 1
            self.next_tick_at = time + 1
            for unit in self.enemies(map):
                if unit.distance(self.row, self.col) <= self.spell_range:
                    self.deal_magic_damage(unit, self.get_crowstorm_damage(), is_multitarget=True)
        if self.ticks_remaining:
            self.mana_locked_until = self.next_tick_at

    def fiddle_crowstorm_extend(self, unit):
        if self.team != unit.team and self.ticks_remaining > 0 and self.distance(unit.row, unit.col) <= self.spell_range:
            self.ticks_remaining += 1
