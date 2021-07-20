from units.unit import Unit
from synergies import Knight
from synergies import Redeemed

class Leona(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=700,
            starting_mana=0,
            total_mana=80,
            armor=40,
            magic_resist=40,
            attack_damage=80,
            attack_speed=0.55,
            attack_range=1,
            image_name='leona',
            synergies=[Knight, Redeemed],
            **kwargs,
        )
        self.mana_lock_time = 4

    def perform_spell(self, map, time):
        self.flat_damage_reduction_modifiers.add_component(self.uuid, time, 4, self.get_damage_reduction())

    def get_damage_reduction(self):
        base_reduction = {
            1: 40,
            2: 80,
            3: 400
        }[max(1, self.star_level)]
        return base_reduction * self.get_spell_power() / 100