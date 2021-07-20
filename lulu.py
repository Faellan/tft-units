from units.unit import Unit
from synergies import Mystic
from synergies import Hellion

class Lulu(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=40,
            total_mana=100,
            armor=25,
            magic_resist=25,
            attack_damage=40,
            attack_speed=0.60,
            attack_range=3,
            image_name='lulu',
            synergies=[Mystic, Hellion],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_whimsy_bonus_attack_speed_ratio(self):
        base_bonus_as = {
            1: 0.7,
            2: 0.8,
            3: 1.2
        }[max(1, self.star_level)]
        return base_bonus_as * self.get_spell_power() / 100

    def get_whimsy_number_of_targets(self):
        return {
            1: 3,
            2: 4,
            3: 6
        }[max(1, self.star_level)]

    def get_whimsy_stun_duration(self):
        return {
            1: 1.5,
            2: 2,
            3: 2.5
        }[max(1, self.star_level)]

    def apply_spell_on_target(self, target, time):
        if target.team == self.team:
            target.base_attack_speed_bonus_ratio_modifiers.add_component(
                self.uuid, time, 4, self.get_whimsy_bonus_attack_speed_ratio()
            )
        else:
            target.stun(time, self.get_whimsy_stun_duration())
            target.percent_damage_reduction_modifiers.add_component(self.uuid, time, self.get_whimsy_stun_duration(), -20)

    def perform_spell(self, map, time):
        other_units = sorted([u for u in map.units if u != self], key=lambda u: self.distance(u.row, u.col))
        for unit in other_units[:self.get_whimsy_number_of_targets()]:
            self.apply_spell_on_target(unit, time)
        if len(other_units) < self.get_whimsy_number_of_targets():
            self.apply_spell_on_target(self, time)
