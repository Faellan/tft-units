import utils

from units.unit import Unit
from synergies import Abomination
from synergies import Legionnaire
from projectile import Projectile

class Pierce(Projectile):

    def __init__(self, **kwargs):
        self.damage = kwargs.pop('damage')
        super().__init__(**kwargs)

    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        self.owner.deal_physical_damage(unit, self.damage)
        self.destroyed = True
        if unit.health < 0:
            excess_damage = -unit.health
            x, y = self.get_xy_pos(time)
            new_pierce = Pierce(
                map=self.map,
                owner=self.owner,
                time=time,
                x0=x-self.XY_OFFSET,
                y0=y-self.XY_OFFSET,
                xE=self.xE-self.XY_OFFSET,
                yE=self.yE-self.XY_OFFSET,
                radius=self.radius,
                hex_per_second=self.hex_per_second,
                damage=excess_damage,
            )
            new_pierce.unit_uuids_hit.add(unit.uuid)
            self.map.projectiles.append(new_pierce)



class Kalista(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=0,
            total_mana=120,
            armor=15,
            magic_resist=15,
            attack_damage=60,
            attack_speed=0.75,
            attack_range=4,
            image_name='kalista',
            synergies=[Abomination, Legionnaire],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_pierce_ad_multiplier(self):
        base_ad_multiplier =  {
            1: 1.80,
            2: 2.00,
            3: 2.40
        }[max(1, self.star_level)]
        return base_ad_multiplier * self.get_spell_power() / 100

    def get_pierce_base_damage(self):
        return {
            1: 350,
            2: 600,
            3: 1000
        }[max(1, self.star_level)]

    def get_pierce_damage(self):
        return self.get_pierce_base_damage() + self.get_pierce_ad_multiplier() * self.get_attack_damage()

    def perform_spell(self, map, time):
        target = self.farthest_hex_enemy(map)
        if not target:
            return

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(target.row, target.col)

        map.projectiles.append(
            Pierce(
                map=map,
                owner=self,
                time=time,
                x0=x0,
                y0=y0,
                xE=xE,
                yE=yE,
                radius=20,
                hex_per_second=8,
                damage=self.get_pierce_damage()
            )
        )
