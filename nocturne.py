import uuid

from units.unit import Unit
from synergies import Assassin
from synergies import Revenant

class Nocturne(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=0,
            total_mana=0,
            armor=30,
            magic_resist=30,
            attack_damage=80,
            attack_speed=0.85,
            attack_range=1,
            image_name='nocturne',
            synergies=[Revenant, Assassin],
            **kwargs,
        )

    def get_umbra_blades_healing_ratio(self):
        return {
            1: 0.9,
            2: 0.95,
            3: 1.0
        }[max(1, self.star_level)]

    def get_umbra_blades_bonus_attack_speed_ratio(self):
        base_ad_ratio = {
            1: 0.3,
            2: 0.35,
            3: 4
        }[max(1, self.star_level)]
        return base_ad_ratio * self.get_spell_power() / 100

    def umbra_blades(self, map, time):
        damage_dealt = 0
        units_hit = 0
        for unit in map.units:
            if unit.team != self.team and unit.distance(self.row, self.col) <= 1:
                _, post_mitigation_damage = self.deal_physical_damage(unit, 1.25 * self.get_attack_damage())
                damage_dealt += post_mitigation_damage
                units_hit += 1
        self.heal(damage_dealt * self.get_umbra_blades_healing_ratio())
        if units_hit == 1:
            self.base_attack_speed_bonus_ratio_modifiers.add_component(self.uuid, time, 3, self.get_umbra_blades_bonus_attack_speed_ratio())

    def auto_attack(self, target, map, time, ad_ratio=1.0, apply_on_hit=True, apply_mana_increase=True, is_from_runaan=False, bonus_damage=0):
        if not is_from_runaan and self.aa_count % 3 == 1:
            self.umbra_blades(map, time)
        else:
            super().auto_attack(target, map, time, ad_ratio, apply_on_hit, apply_mana_increase, is_from_runaan, bonus_damage)
