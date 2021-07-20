import math
import utils

from units.unit import Unit
from synergies import Ranger
from synergies import Draconic
from projectile import Projectile

class EnchantedArrow(Projectile):
    def has_travelled_5_hex_or_more(self, time):
        x, y = self.get_xy_pos(time)
        return math.sqrt((x-self.x0)**2 + (y-self.y0)**2) > 5 * self.HEX_TO_XY_DISTANCE_RATIO

    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        stun_duration = self.owner.get_enchanted_arrow_stun_duration()
        if self.has_travelled_5_hex_or_more(time):
            stun_duration *= 2
        unit.stun(time, stun_duration)
        self.owner.deal_magic_damage(unit, self.owner.get_enchanted_arrow_damage())

        for u in self.map.units:
            if u.team != unit.team:
                continue
            if u.distance(unit.row, unit.col) <= 1:
                self.owner.deal_magic_damage(u, self.owner.get_enchanted_arrow_damage()/2)
                u.stun(time, stun_duration/2)

        self.destroyed = True


class Ashe(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=3,
            health=550,
            starting_mana=50,
            total_mana=100,
            armor=20,
            magic_resist=20,
            attack_damage=60,
            attack_speed=0.75,
            attack_range=5,
            image_name='ashe',
            synergies=[Ranger, Draconic],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_enchanted_arrow_damage(self):
        base_damage =  {
            1: 300,
            2: 450,
            3: 650
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_enchanted_arrow_stun_duration(self):
        return {
            1: 1.5,
            2: 2,
            3: 2.5
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        target = self.farthest_hex_enemy(map)
        if not target:
            return

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(target.row, target.col)

        map.projectiles.append(
            EnchantedArrow(
                map=map,
                owner=self,
                time=time,
                x0=x0,
                y0=y0,
                xE=xE,
                yE=yE,
                radius=30,
                hex_per_second=8,
            )
        )
