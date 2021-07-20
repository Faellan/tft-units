from units.unit import Unit
from synergies import Nightbringer
from synergies import Renewer

class Vladimir(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=0,
            total_mana=85,
            armor=35,
            magic_resist=35,
            attack_damage=45,
            attack_speed=0.65,
            attack_range=2,
            image_name='vladimir',
            synergies=[Nightbringer, Renewer],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_transfusion_damage(self):
        base_damage = {
            1: 300,
            2: 420,
            3: 540
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_transfusion_healing(self):
        base_heal = {
            1: 200,
            2: 250,
            3: 350
        }[max(1, self.star_level)]
        return base_heal * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        self.deal_magic_damage(self.current_target, self.get_transfusion_damage())
        self.heal(self.get_transfusion_healing())