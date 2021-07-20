from units.unit import Unit

from synergies import Sentinel
from synergies import Draconic
from synergies import Knight

class Galio(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=1000,
            starting_mana=120,
            total_mana=180,
            armor=60,
            magic_resist=60,
            attack_damage=70,
            attack_speed=0.6,
            attack_range=1,
            image_name='galio',
            synergies=[Knight, Sentinel, Draconic],
            **kwargs,
        )
        self.cast_time = 0.1
        self.release_at = None
        self.galio_damage_blocked = 0
        self.mana_lock_time = 2

    def get_damage_percent_reduction(self):
        return {
            1: 60,
            2: 70,
            3: 90
        }[max(1, self.star_level)]

    def get_shield_of_durand_magic_damage(self):
        return {
            1: 200,
            2: 300,
            3: 2000
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def perform_spell(self, board, time):
        self.percent_damage_reduction_modifiers.add_component('galio', time, 2, self.get_damage_percent_reduction())
        self.galio_damage_blocked = 0
        for unit in self.targetable_enemies(board):
            if unit.distance(self.row, self.col) <= 2:
                unit.current_target = self
        self.release_at = time + 2

    def apply_additional_percent_damage_reduction(self, damage, is_multitarget):
        if self.release_at:
            self.galio_damage_blocked += self.get_damage_percent_reduction() / 100 * damage
        return super().apply_additional_percent_damage_reduction(damage, is_multitarget)

    def tick(self, board, time):
        super().tick(board, time)
        if self.release_at and time >= self.release_at:
            self.release_at = None
            damage = self.get_shield_of_durand_magic_damage() + 0.5 * self.galio_damage_blocked
            for unit in self.enemies(board):
                if unit.distance(self.row, self.col) <= 3:
                    self.deal_magic_damage(unit, damage)