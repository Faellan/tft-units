from units.unit import Unit
from synergies import Cavalier
from synergies import Hellion

class Kled(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=400,
            starting_mana=0,
            total_mana=0,
            armor=30,
            magic_resist=30,
            attack_damage=65,
            attack_speed=0.75,
            attack_range=1,
            image_name='kled',
            synergies=[Cavalier, Hellion],
            **kwargs,
        )
        self.has_ticked = False
        self.aa = 0
        self.dismounted_at = None

    def get_violent_tendencies_bonus_as(self):
        return {
            1: 0.7,
            2: 0.8,
            3: 1.0
        }[max(1, self.star_level)]

    def get_innate_shield_percentage(self):
        return 80

    def auto_attack(self, target, map, time, ad_ratio=1.0, apply_on_hit=True, apply_mana_increase=True, is_from_runaan=False, bonus_damage=0):
        if not is_from_runaan:
            if self.aa_count % 4 == 0:
                ad_ratio *= 2
        super().auto_attack(target, map, time, ad_ratio, apply_on_hit, apply_mana_increase, is_from_runaan, bonus_damage)

    def tick(self, map, time):
        if not self.has_ticked:
            self.has_ticked = True
            self.add_shield_effect(self.get_innate_shield_percentage() / 100 * self.total_health, 99999, identifier='kled_shield')
        if not self.shield_manager.has_shield('kled_shield') and not self.dismounted_at:
            self.dismounted_at = time
            self.untargetable_until = max(self.untargetable_until, time + 0.7)
            self.base_attack_speed_bonus_ratio_modifiers.add_component(self.uuid, time, 9999, self.get_violent_tendencies_bonus_as())
        super().tick(map, time)