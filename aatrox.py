from units.unit import Unit
from synergies import Legionnaire
from synergies import Redeemed

class Aatrox(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=0,
            total_mana=70,
            armor=35,
            magic_resist=35,
            attack_damage=60,
            attack_speed=0.65,
            attack_range=1,
            image_name='aatrox',
            synergies=[Legionnaire, Redeemed],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_deathbringer_strike_ad_percentage(self):
        return {
            1: 260,
            2: 280,
            3: 360
        }[max(1, self.star_level)]

    def get_deathbringer_strike_damage(self):
        return self.get_attack_damage() * self.get_deathbringer_strike_ad_percentage() / 100

    def get_deathbringer_strike_healing(self):
        base_heal = {
            1: 200,
            2: 300,
            3: 450
        }[max(1, self.star_level)]
        return base_heal * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        self.deal_physical_damage(self.current_target, self.get_deathbringer_strike_damage())
        self.heal(self.get_deathbringer_strike_healing())