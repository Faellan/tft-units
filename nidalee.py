import uuid

from units.unit import Unit
from synergies import Skirmisher
from synergies import Dawnbringer

class Nidalee(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=800,
            starting_mana=0,
            total_mana=60,
            armor=35,
            magic_resist=35,
            attack_damage=50,
            attack_speed=0.9,
            attack_range=3,
            image_name='nidalee',
            synergies=[Dawnbringer, Skirmisher],
            **kwargs,
        )
        self.cast_time = 0.01
        self.last_leap_at = None
        self.is_transformed = False
        self.cougar_attacks = 0

    def get_aspect_of_the_cougar_as_bonus(self):
        return {
            1: 0.4,
            2: 0.5,
            3: 0.75,
        }[max(1, self.star_level)]

    def get_aspect_of_the_cougar_damage(self):
        base_damage = {
            1: 200,
            2: 300,
            3: 600
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def leap_to(self, map, target, time):
        row, col = target.closest_empty_tile(map, farthest_from_row=self.row, farthest_from_col=self.col)
        self.move_to(row, col, time, 0.1)
        self.last_leap_at = time

    def before_auto_attack(self, target, map, time):
        if self.is_transformed:
            self.cougar_attacks += 1
            if self.cougar_attacks % 4 == 0:
                self.deal_magic_damage(target, self.get_aspect_of_the_cougar_damage())

    def lowest_health_enemy(self, map):
        enemies = [u for u in map.units if u.team != self.team and u.is_targetable]
        if not enemies:
            return
        return sorted(
            enemies,
            key=lambda e: e.health / e.total_health,
        )[0]

    def perform_spell(self, map, time):
        self.total_mana = 0
        self.range = 1
        self.is_transformed = True
        self.bonus_dodge += 0.45
        self.base_attack_speed_bonus_ratio_modifiers.add_component('cougar', time, 9999, 0.45)
        target = self.lowest_health_enemy(map)

        if target and target.distance(self.row, self.col) > 1:
            self.leap_to(map, target, time)

    def tick(self, map, time):
        super().tick(map, time)
        if self.is_transformed and self.last_leap_at and time >= self.last_leap_at + 1:
            if self.current_target and self.current_target.distance(self.row, self.col) > 1:
                target = self.lowest_health_enemy(map)
                if target:
                    self.leap_to(map, target, time)