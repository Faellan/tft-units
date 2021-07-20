import utils
from units.unit import Unit
from synergies import Brawler
from synergies import Revenant

class Volibear(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=1100,
            starting_mana=110,
            total_mana=200,
            armor=60,
            magic_resist=60,
            attack_damage=80,
            attack_speed=0.765,
            attack_range=1,
            image_name='volibear',
            synergies=[Brawler, Revenant],
            **kwargs,
        )
        self.cast_time = 0.1
        self.stun_at = None

    def get_doombringer_damage(self):
        base_damage = {
            1: 150,
            2: 300,
            3: 5000
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_doombringer_stun_duration(self):
        return {
            1: 2.5,
            2: 3.5,
            3: 10
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        self.move_to(target.row, target.col, time, 1)
        self.stun_at = time + 0.9

    def tick(self, map, time):
        super().tick(map, time)
        if self.stun_at and time >= self.stun_at:
            self.stun_at = None
            for unit in self.enemies(map):
                if unit.distance(self.row, self.col) <= 2:
                    self.deal_magic_damage(unit, self.get_doombringer_damage())
                    unit.stun(time, self.get_doombringer_stun_duration())