import utils

from units.unit import Unit
from synergies import Redeemed
from synergies import Mystic
from projectile import Projectile
from on_hit_effect import OnHitEffect

class PrismaticIlluminationSecond(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team != self.owner.team:
            return

        unit.add_shield_effect(self.owner.get_prismatic_illusion_shield(), 3)

class PrismaticIlluminationFirst(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team != self.owner.team:
            return

        unit.add_shield_effect(self.owner.get_prismatic_illusion_shield(), 3)

    def on_destroy(self, map, time):
        map.projectiles.append(
            PrismaticIlluminationSecond(
                map=map,
                owner=self.owner,
                time=time,
                x0=self.xE - self.XY_OFFSET,
                y0=self.yE - self.XY_OFFSET,
                xE=self.x0 - self.XY_OFFSET,
                yE=self.y0 - self.XY_OFFSET,
                radius=20,
                hex_per_second=7,
            )
        )

class PrismaticIlluminationOnHit(OnHitEffect):
    def proc(self, target):
        self.source.deal_magic_damage(target, self.source.get_prismatic_illusion_damage())
        self.force_expire()

class Lux(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=3,
            health=600,
            starting_mana=40,
            total_mana=80,
            armor=20,
            magic_resist=20,
            attack_damage=40,
            attack_speed=0.6,
            attack_range=4,
            image_name='lux',
            synergies=[Redeemed, Mystic],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_prismatic_illusion_shield(self):
        base_shield =  {
            1: 120,
            2: 180,
            3: 360
        }[max(1, self.star_level)]
        return base_shield * self.get_spell_power() / 100

    def get_prismatic_illusion_damage(self):
        base_damage =  {
            1: 400,
            2: 600,
            3: 1000
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        target = self.farthest_hex_ally(map)
        if target:
            target_row, target_col = target.row, target.col
        else:
            target_row, target_col = self.row - 1, self.col - 1

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(target_row, target_col)
        xE += (xE - x0) * 0.1
        yE += (yE - y0) * 0.1

        map.projectiles.append(
            PrismaticIlluminationFirst(
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
        self.on_hit_effects.append(PrismaticIlluminationOnHit(source=self, attached_to=self, expires_at=time + 9999))
