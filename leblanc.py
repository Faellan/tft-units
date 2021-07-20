from units.unit import Unit
from synergies import Assassin

# DEPRECATED
class Leblanc(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=550,
            starting_mana=20,
            total_mana=60,
            armor=20,
            magic_resist=20,
            attack_damage=55,
            attack_speed=0.75,
            attack_range=3,
            image_name='leblanc',
            synergies=[Assassin],
            **kwargs,
        )
        self.damage_at = None
        self.mana_lock_time = 1.5
        self.cast_time = 0.1
        self.targets = []

    def get_etheral_chains_damage(self):
        base_damage = {
            1: 200,
            2: 250,
            3: 500
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_etheral_chains_stun_duration(self):
        return {
            1: 2,
            2: 2,
            3: 2
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        self.targets = sorted(
            [u for u in map.units if u.team != self.team],
            key=lambda u: self.distance(u.row, u.col)
        )[:2]
        self.damage_at = time + 1.00

    def tick(self, map, time):
        super().tick(map, time)
        if self.damage_at and time >= self.damage_at:
            self.damage_at = None
            for target in self.targets:
                self.deal_magic_damage(target, self.get_etheral_chains_damage())
                target.stun(time, self.get_etheral_chains_stun_duration())