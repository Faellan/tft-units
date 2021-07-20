from units.unit import Unit
from synergies import Hellion
from synergies import Spellweaver

class Ziggs(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=0,
            total_mana=40,
            armor=15,
            magic_resist=15,
            attack_damage=40,
            attack_speed=0.75,
            attack_range=4,
            image_name='ziggs',
            synergies=[Hellion, Spellweaver],
            **kwargs,
        )
        self.cast_time = 0.5

    def get_arcane_bomb_damage(self):
        base_damage = {
            1: 250,
            2: 350,
            3: 450
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        if not self.current_target:
            return
        self.deal_magic_damage(self.current_target, self.get_arcane_bomb_damage())