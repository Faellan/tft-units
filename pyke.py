import utils
from units.unit import Unit
from synergies import Sentinel
from synergies import Assassin
from projectile import Projectile

class PhantomUndertow(Projectile):
    def on_unit_hit(self, time, unit):
        if unit.team == self.owner.team:
            return

        unit.stun(time, self.owner.get_phantom_undertow_stun_duration())
        self.owner.deal_magic_damage(unit, self.owner.get_phantom_undertow_damage())

class Pyke(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=60,
            total_mana=120,
            armor=30,
            magic_resist=30,
            attack_damage=50,
            attack_speed=0.6,
            attack_range=1,
            image_name='pyke',
            synergies=[Sentinel, Assassin],
            **kwargs,
        )
        self.cast_time = 0.05
        self.x0 = None
        self.y0 = None
        self.stun_at = None

    def get_phantom_undertow_damage(self):
        base_damage = {
            1: 150,
            2: 225,
            3: 325
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_phantom_undertow_stun_duration(self):
        return {
            1: 1.5,
            2: 2,
            3: 3
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        jump_pos = self.farthest_hex_enemy(map).closest_empty_tile(map, farthest_from_row=self.row, farthest_from_col=self.col)
        self.x0, self.y0 = utils.xy_pos_from_ij_tile(self.row, self.col)
        self.move_to(jump_pos[0], jump_pos[1], time, 0.5)
        self.current_target = None
        self.stun_at = time + 1

    def tick(self, map, time):
        super().tick(map, time)
        if self.stun_at and time >= self.stun_at:
            self.stun_at = None
            self.launch_stun(map, time)

    def launch_stun(self, map, time):
        xE, yE = utils.xy_pos_from_ij_tile(self.row, self.col)
        map.projectiles.append(
            PhantomUndertow(
                map=map,
                owner=self,
                time=time,
                x0=self.x0,
                y0=self.y0,
                xE=xE,
                yE=yE,
                radius=25,
                hex_per_second=20,
            )
        )
