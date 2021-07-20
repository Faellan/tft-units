from units.unit import Unit
from synergies import Brawler
from synergies import Abomination

class Nunu(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=900,
            starting_mana=30,
            total_mana=90,
            armor=45,
            magic_resist=45,
            attack_damage=65,
            attack_speed=0.55,
            attack_range=1,
            image_name='nunu',
            synergies=[Brawler, Abomination],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_consume_damage(self):
        base_damage = {
            1: 500,
            2: 750,
            3: 1800
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100


    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        if target.health < self.health:
            self.deal_true_damage(target, self.get_consume_damage() * 1.5)
        else:
            self.deal_magic_damage(target, self.get_consume_damage())
