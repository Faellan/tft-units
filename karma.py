import random

from units.unit import Unit
from synergies import Dawnbringer
from synergies import Invoker

class Karma(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=700,
            starting_mana=0,
            total_mana=50,
            armor=25,
            magic_resist=25,
            attack_damage=45,
            attack_speed=0.7,
            attack_range=4,
            image_name='karma',
            synergies=[Dawnbringer, Invoker],
            **kwargs,
        )
        self.cast_time = 0.5
        self.mana_lock_time = 1.5
        self.target_row = None
        self.target_col = None

    def get_soulflare_damage(self):
        base_damage = {
            1: 210,
            2: 260,
            3: 700
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_soulflare_mana_reduction(self):
        return {
            1: 15,
            2: 15,
            3: 30
        }[max(1, self.star_level)]

    def cast_spell(self, map, time):
        super().cast_spell(map, time)
        enemies = self.targetable_enemies(map)
        if enemies:
            target = random.choice(enemies)
            self.target_row, self.target_col = target.row, target.col

    def perform_spell(self, map, time):
        self.total_mana = max(self.total_mana - self.get_soulflare_mana_reduction(), 10)
        if not self.target_row or not self.target_col:
            return
        for unit in self.enemies(map):
            if unit.distance(self.target_row, self.target_col) <= 1:
                self.deal_magic_damage(unit, self.get_soulflare_damage())
        self.target_row, self.target_col = None, None
