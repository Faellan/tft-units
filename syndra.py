from units.unit import Unit
from synergies import Invoker
from synergies import Redeemed

class Syndra(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=600,
            starting_mana=50,
            total_mana=90,
            armor=20,
            magic_resist=20,
            attack_damage=40,
            attack_speed=0.65,
            attack_range=4,
            image_name='syndra',
            synergies=[Invoker, Redeemed],
            **kwargs,
        )
        self.cast_time = 0.2
        self.throw_at = None
        self.throw_target = None
        self.throw_row = None
        self.throw_col = None

    def get_force_of_will_damage(self):
        base_damage = {
            1: 300,
            2: 400,
            3: 600
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_force_of_will_stun_duration(self):
        return {
            1: 2,
            2: 2.5,
            3: 4
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        self.throw_target = self.closest_hex_enemy(map)
        if self.throw_target:
            self.throw_at = time + 0.5
            throw_pos = self.farthest_hex_enemy(map).closest_empty_tile(map, farthest_from_row=self.row, farthest_from_col=self.col)
            self.throw_row = throw_pos[0]
            self.throw_col = throw_pos[1]

    def tick(self, map, time):
        super().tick(map, time)
        if self.throw_at and time >= self.throw_at:
            self.throw_at = None
            self.throw(map, time)

    def throw(self, map, time):
        if self.throw_target.is_dead:
            return  # snif
        self.throw_target.stun(time, self.get_force_of_will_stun_duration())
        self.throw_target.move_to(self.throw_row, self.throw_col, time, 0.1)
        for unit in map.units:
            if unit.team == self.team:
                continue
            if unit.distance(self.throw_row, self.throw_col) <= 1:
                self.deal_magic_damage(unit, self.get_force_of_will_damage(), is_multitarget=True)