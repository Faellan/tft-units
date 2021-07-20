import utils

from units.unit import Unit
from synergies import Redeemed
from synergies import Spellweaver
from projectile import Projectile

class DisintegrationRay(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        self.owner.deal_magic_damage(unit, self.owner.get_disintegration_ray_total_damage() / self.owner.number_of_ticks)


class Velkoz(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=700,
            starting_mana=0,
            total_mana=80,
            armor=25,
            magic_resist=25,
            attack_damage=45,
            attack_speed=0.75,
            attack_range=4,
            image_name='velkoz',
            synergies=[Redeemed, Spellweaver],
            **kwargs,
        )
        self.cast_time = 0.02
        self.number_of_ticks = 8  # TODO: +/- 1 ?
        self.starting_radius = 20
        self.radius_increase_per_tick = 5

        self.spell_target = None
        self.ticks_remaining = 0
        self.next_tick_at = None
        self.tick_delay = 0.5

    def get_disintegration_ray_total_damage(self):
        base_damage =  {
            1: 900,
            2: 1150,
            3: 4000
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, board, time):
        self.next_tick_at = time + 0.01
        self.ticks_remaining = self.number_of_ticks
        self.change_first_spell_target(board, time)

    def change_first_spell_target(self, board, time):
        enemies = self.targetable_enemies(board)
        if enemies:
            x1, y1 = utils.xy_pos_from_ij_tile(3, 4)
            x2, y2 = utils.xy_pos_from_ij_tile(4, 4)
            xc, yc = (x1 + x2) / 2, (y1 + y2) / 2
            self.spell_target = sorted(enemies, key=lambda e: e.xydistance2_with_point(xc, yc))[0]

    def change_spell_target_mid_spell(self, board, time):
        if not self.spell_target:
            self.change_first_spell_target(board, time)
            return
        enemies = self.targetable_enemies(board)
        if enemies:
            self.spell_target = sorted(enemies, key=lambda e: e.xydistance2_with_unit(self.spell_target))[0]

    def launch_ray(self, board, time):
        if not self.spell_target or self.spell_target.is_dead or not self.spell_target.is_targetable:
            self.change_spell_target_mid_spell(board, time)

        if not self.spell_target:
            return

        multiply = 15 - self.distance(self.spell_target.row, self.spell_target.col)

        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        xE, yE = utils.xy_pos_from_ij_tile(self.spell_target.row, self.spell_target.col)

        xE += (xE - x0) * multiply
        yE += (yE - y0) * multiply
        radius = self.starting_radius + self.radius_increase_per_tick * (self.number_of_ticks - self.ticks_remaining)

        board.projectiles.append(
            DisintegrationRay(
                map=board,
                owner=self,
                time=time,
                x0=x0,
                y0=y0,
                xE=xE,
                yE=yE,
                radius=radius,
                hex_per_second=50,
            )
        )


    def tick(self, board, time):
        super().tick(board, time)

        if self.is_stunned:
            self.next_tick_at = None
            self.ticks_remaining = 0
            self.spell_target = None

        if self.ticks_remaining and self.next_tick_at and time >= self.next_tick_at:
            self.launch_ray(board, time)
            self.ticks_remaining -= 1
            if self.ticks_remaining:
                self.next_tick_at = time + self.tick_delay
            else:
                self.spell_target = None
                self.next_tick_at = None