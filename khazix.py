from units.unit import Unit
from synergies import Dawnbringer
from synergies import Assassin

class Khazix(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=0,
            total_mana=60,
            armor=25,
            magic_resist=25,
            attack_damage=55,
            attack_speed=0.7,
            attack_range=1,
            image_name='khazix',
            synergies=[Dawnbringer, Assassin],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_taste_their_fear_damage(self):
        return {
            1: 250,
            2: 350,
            3: 550
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def get_taste_their_fear_isolation_damage(self):
        return {
            1: 750,
            2: 1050,
            3: 1650
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def is_target_isolated(self, map):
        if self.current_target:
            u = self.current_target.closest_hex_ally(map)
            return u is None or self.current_target.distance(u.row, u.col) > 1

    def perform_spell(self, map, time):
        if self.is_target_isolated(map):
            damage = self.get_taste_their_fear_isolation_damage()
        else:
            damage = self.get_taste_their_fear_damage()
        if self.current_target:
            self.deal_magic_damage(self.current_target, damage)