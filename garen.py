from units.unit import Unit
from synergies import Dawnbringer
from synergies import Knight
from synergies import Victorious
from on_hit_effect import OnHitEffect

class VictoriousProc(OnHitEffect):
    def proc(self, target):
        self.source.deal_magic_damage(target, 0.4 * (target.total_health - target.health))
        self.force_expire()


class Garen(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=5,
            health=1050,
            starting_mana=100,
            total_mana=180,
            armor=60,
            magic_resist=60,
            attack_damage=80,
            attack_speed=0.75,
            attack_range=1,
            image_name='garen',
            synergies=[Dawnbringer, Knight, Victorious],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_god_lions_justice_maximum_health_ratio_damage(self):
        base_ratio = {
            1: 0.25,
            2: 0.30,
            3: 2.0
        }[max(1, self.star_level)]
        return base_ratio * self.get_spell_power() / 100

    def get_god_lions_justice_shield_ratio(self):
        base_shield = {
            1: 0.4,
            2: 0.55,
            3: 2.0
        }[max(1, self.star_level)]
        return base_shield * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        for unit in self.enemies(map):
            if unit.distance(self.row, self.col) <= 3:
                self.deal_magic_damage(unit, unit.total_health * self.get_god_lions_justice_maximum_health_ratio_damage(), is_multitarget=True)
                if unit.health <= 0 and not unit.revive_with:
                    self.on_hit_effects.append(VictoriousProc(source=self, attached_to=self, expires_at=time + 9999))
        self.add_shield_effect(self.total_health * self.get_god_lions_justice_shield_ratio(), 5)

    def auto_attack(self, target, map, time, ad_ratio=1.0, apply_on_hit=True, apply_mana_increase=True, is_from_runaan=False, bonus_damage=0):
        super().auto_attack(target, map, time, ad_ratio, apply_on_hit, apply_mana_increase, is_from_runaan, bonus_damage)
        if target.health <= 0 and not target.revive_with:
            self.on_hit_effects.append(VictoriousProc(source=self, attached_to=self, expires_at=time + 9999))
