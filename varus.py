from units.unit import Unit
from synergies import Redeemed
from synergies import Ranger
from on_hit_effect import OnHitEffect

class HolyArrows(OnHitEffect):
    def proc(self, target):
        self.source.deal_magic_damage(target, self.source.get_holy_arrows_on_hit_damage())

class Varus(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=600,
            starting_mana=0,
            total_mana=60,
            armor=20,
            magic_resist=20,
            attack_damage=60,
            attack_speed=0.75,
            attack_range=4,
            image_name='varus',
            synergies=[Redeemed, Ranger],
            **kwargs,
        )
        self.cast_time = 0.3
        self.holy_arrows_range = 2

    def get_holy_arrows_ad_ratio_damage(self):
        return {
            1: 1.5,
            2: 1.55,
            3: 1.65
        }[max(1, self.star_level)]

    def get_holy_arrows_on_hit_damage(self):
        base_on_hit_damage = {
            1: 40,
            2: 60,
            3: 90
        }[max(1, self.star_level)]
        return base_on_hit_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        for unit in map.units:
            if unit.distance(target.row, target.col) > self.holy_arrows_range:
                continue
            if unit.team == self.team:
                unit.on_hit_effects.append(HolyArrows(source=self, attached_to=unit, expires_at=time + 6))
            else:
                self.deal_physical_damage(
                    unit,
                    self.get_holy_arrows_ad_ratio_damage() * self.get_attack_damage(),
                    is_multitarget=True
                )
        self.on_hit_effects.append(HolyArrows(source=self, attached_to=self, expires_at=time + 6))
