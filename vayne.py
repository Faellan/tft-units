from units.unit import Unit
from synergies import Ranger
from synergies import Forgotten

class Vayne(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=500,
            starting_mana=0,
            total_mana=0,
            armor=15,
            magic_resist=15,
            attack_damage=30,
            attack_speed=0.8,
            attack_range=4,
            image_name='vayne',
            synergies=[Ranger, Forgotten],
            **kwargs,
        )

    def get_silver_bolt_damage(self):
        base_damage = {
            1: 70,
            2: 100,
            3: 140
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def after_auto_attack(self, target, map, time):
        super().after_auto_attack(target, map, time)
        target.put_stack('silver_bolt', 1)
        if target.stacks['silver_bolt'] == 3:
            target.stacks['silver_bolt'] = 0
            self.deal_true_damage(target, self.get_silver_bolt_damage())