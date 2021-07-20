from units.unit import Unit
from synergies import Skirmisher
from synergies import Draconic


class Udyr(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=700,
            starting_mana=30,
            total_mana=40,
            armor=30,
            magic_resist=30,
            attack_damage=55,
            attack_speed=0.75,
            attack_range=1,
            image_name='udyr',
            synergies=[Skirmisher, Draconic],
            **kwargs,
        )
        self.next_stance = 'turtle'
        self.is_next_aa_boosted = False

    def get_feral_instinct_shield(self):
        base_shield = {
            1: 250,
            2: 350,
            3: 550
        }[max(1, self.star_level)]
        return base_shield * self.get_spell_power() / 100

    def get_feral_instinct_ad_percentage_bonus(self):
        return {
            1: 1.2,
            2: 1.3,
            3: 1.8
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        if self.next_stance == 'turtle':
            self.next_stance = 'tiger'
            self.add_shield_effect(self.get_feral_instinct_shield(), 4)
        elif self.next_stance == 'tiger':
            self.next_stance = 'turtle'
            self.is_next_aa_boosted = True

    def auto_attack(self, target, map, time, ad_ratio=1.0, apply_on_hit=True, apply_mana_increase=True, is_from_runaan=False, bonus_damage=0):
        if self.is_next_aa_boosted:
            self.is_next_aa_boosted = False
            ad_ratio *= self.get_feral_instinct_ad_percentage_bonus()
        super().auto_attack(target, map, time, ad_ratio, apply_on_hit, apply_mana_increase, is_from_runaan, bonus_damage)


