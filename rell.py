import utils

from units.unit import Unit
from synergies import Redeemed
from synergies import Ironclad
from synergies import Cavalier
from projectile import Projectile

class AttractAndRepel(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            unit.add_shield_effect(self.owner.get_attract_and_repel_shield(), 4)
        else:
            unit.stun(time, self.owner.get_attract_and_repel_stun_duration())


class Rell(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=950,
            starting_mana=80,
            total_mana=150,
            armor=60,
            magic_resist=60,
            attack_damage=70,
            attack_speed=0.6,
            attack_range=1,
            image_name='rell',
            synergies=[Redeemed, Ironclad, Cavalier],
            **kwargs,
        )
        self.cast_time = 0.8

    def get_attract_and_repel_shield(self):
        base_shield =  {
            1: 350,
            2: 450,
            3: 3000
        }[max(1, self.star_level)]
        return base_shield * self.get_spell_power() / 100

    def get_attract_and_repel_stun_duration(self):
        return {
            1: 1.5,
            2: 2,
            3: 8
        }[max(1, self.star_level)]

    def apply_around(self, board, time, row, col):
        for unit in board.units:
            if unit.distance(row, col) > 2:
                continue
            if unit.team == self.team:
                unit.add_shield_effect(self.get_attract_and_repel_shield(), 4)
            else:
                unit.stun(time, self.get_attract_and_repel_stun_duration())

    def perform_spell(self, board, time):
        target = self.farthest_hex_ally(board)
        if target:
            self.apply_around(board, time, target.row, target.col)
            x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
            xE, yE = utils.xy_pos_from_ij_tile(target.row, target.col)
            board.projectiles.append(
                AttractAndRepel(
                    map=board,
                    owner=self,
                    time=time,
                    x0=x0,
                    y0=y0,
                    xE=xE,
                    yE=yE,
                    radius=25,
                    hex_per_second=15,
                )
            )

        self.apply_around(board, time, self.row, self.col)

