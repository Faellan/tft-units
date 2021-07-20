import utils

from units.unit import Unit
from synergies import Sentinel
from synergies import Cannoneer
from projectile import Projectile

class LastEmbrace(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        self.owner.deal_magic_damage(unit, self.owner.get_last_embrace_damage())
        unit.stun(time, self.owner.get_last_embrace_stun_duration())
        for u in self.map.units:
            if u.team != unit.team:
                continue
            if u.distance(unit.row, unit.col) <= 1:
                self.owner.deal_magic_damage(u, self.owner.get_last_embrace_damage())
        self.destroyed = True


class Senna(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=40,
            total_mana=80,
            armor=15,
            magic_resist=15,
            attack_damage=55,
            attack_speed=0.7,
            attack_range=4,
            image_name='senna',
            synergies=[Sentinel, Cannoneer],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_last_embrace_damage(self):
        base_damage =  {
            1: 200,
            2: 300,
            3: 450
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_last_embrace_stun_duration(self):
        return 1.5

    def perform_spell(self, map, time):
        target = self.farthest_hex_enemy(map)
        if not target:
            return

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(target.row, target.col)

        map.projectiles.append(
            LastEmbrace(
                map=map,
                owner=self,
                time=time,
                x0=x0,
                y0=y0,
                xE=xE,
                yE=yE,
                radius=20,
                hex_per_second=7,
            )
        )
