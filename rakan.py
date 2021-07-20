import math
import utils

from units.unit import Unit
from synergies import Sentinel
from synergies import Renewer
from projectile import Projectile

class GleamingQuell(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        self.owner.deal_magic_damage(unit, self.owner.get_gleaming_quill_damage())
        healing_radius = 3 if unit.health <= 0 and not unit.revive_with else 2  # TODO: check values

        for u in self.map.units:
            if u.team == self.owner.team and u.distance(unit.row, unit.col) <= healing_radius:
                u.heal(self.owner.get_gleaming_quill_healing_ratio() * u.total_health)

        self.destroyed = True


class Rakan(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=3,
            health=800,
            starting_mana=40,
            total_mana=80,
            armor=35,
            magic_resist=35,
            attack_damage=50,
            attack_speed=0.6,
            attack_range=2,
            image_name='rakan',
            synergies=[Sentinel, Renewer],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_gleaming_quill_damage(self):
        base_damage =  {
            1: 300,
            2: 450,
            3: 650
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_gleaming_quill_healing_ratio(self):
        return {
            1: 0.35,
            2: 0.50,
            3: 0.80
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(target.row, target.col)

        map.projectiles.append(
            GleamingQuell(
                map=map,
                owner=self,
                time=time,
                x0=x0,
                y0=y0,
                xE=xE,
                yE=yE,
                radius=20,
                hex_per_second=8,
            )
        )
