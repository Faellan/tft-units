from units.unit import Unit
from synergies import Dawnbringer
from synergies import Legionnaire

class Riven(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=850,
            starting_mana=0,
            total_mana=40,
            armor=35,
            magic_resist=35,
            attack_damage=85,
            attack_speed=0.8,
            attack_range=1,
            image_name='riven',
            synergies=[Dawnbringer, Legionnaire],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_blade_of_the_dawn_damage(self):
        base_damage = {
            1: 260,
            2: 280,
            3: 360
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_blade_of_the_dawn_ad_multiplier(self):
        return {
            1: 0.9,
            2: 1,
            3: 1.3
        }[max(1, self.star_level)]

    def get_blade_of_the_dawn_stun_duration(self):
        return 1.5

    def perform_spell(self, map, time):
        self.attack_damage_multiplier_modifiers.add_component(self.uuid, time, 8, self.get_blade_of_the_dawn_ad_multiplier())
        for unit in map.units:
            if unit.team == self.team:
                continue
            if unit.distance(self.row, self.col) <= 1:
                unit.stun(time, self.get_blade_of_the_dawn_stun_duration())
                self.deal_magic_damage(unit, self.get_blade_of_the_dawn_damage(), is_multitarget=True)