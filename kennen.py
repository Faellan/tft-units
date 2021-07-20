import utils
from units.unit import Unit
from synergies import Hellion
from synergies import Skirmisher
from projectile import Projectile

class FlameRush(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        unit.stun(time, self.owner.get_flame_rush_stun_duration())
        self.owner.deal_magic_damage(unit, self.owner.get_flame_rush_damage())

class Kennen(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=600,
            starting_mana=60,
            total_mana=125,
            armor=30,
            magic_resist=30,
            attack_damage=50,
            attack_speed=0.7,
            attack_range=1,
            image_name='kennen',
            synergies=[Hellion, Skirmisher],
            **kwargs,
        )
        self.cast_time = 0.05
        self.x0 = None
        self.y0 = None
        self.second_rush_at = None

    def get_flame_rush_damage(self):
        base_damage = {
            1: 150,
            2: 225,
            3: 350
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_flame_rush_stun_duration(self):
        return {
            1: 1.5,
            2: 2,
            3: 2.5
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        self.launch_rush(map, time, target, 0.5)
        self.second_rush_at = time + 0.5

    def launch_rush(self, map, time, target, duration):
        x0, y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        second_rush_pos = target.closest_empty_tile(map, farthest_from_row=self.row, farthest_from_col=self.col)
        self.move_to(second_rush_pos[0], second_rush_pos[1], time, duration)
        xE, yE = utils.xy_pos_from_ij_tile(second_rush_pos[0], second_rush_pos[1])
        map.projectiles.append(
            FlameRush(
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

    def launch_second_rush(self, map, time):
        target = self.farthest_hex_enemy(map)
        if not target:
            return
        self.launch_rush(map, time, target, 1)

    def tick(self, map, time):
        super().tick(map, time)
        if self.second_rush_at and time >= self.second_rush_at:
            self.second_rush_at = None
            self.launch_second_rush(map, time)