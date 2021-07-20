from units.unit import Unit

from synergies import Dawnbringer
from synergies import Brawler
from on_hit_effect import OnHitEffect

class DrunkenRage(OnHitEffect):
    def proc(self, target):
        self.source.deal_magic_damage(target, self.source.get_bonus_damage_aa())
        self.force_expire()


class Gragas(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=40,
            total_mana=70,
            armor=40,
            magic_resist=40,
            attack_damage=50,
            attack_speed=0.50,
            attack_range=1,
            image_name='gragas',
            synergies=[Brawler, Dawnbringer],
            **kwargs,
        )
        self.mana_lock_time = 4
        self.cast_time = 1

    def get_damage_percent_reduction(self):
        return {
            1: 40,
            2: 50,
            3: 60
        }[max(1, self.star_level)]

    def get_bonus_damage_aa(self):
        return {
            1: 175,
            2: 250,
            3: 400
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        self.next_auto_is_empowered = True
        self.percent_damage_reduction_modifiers.add_component(self.uuid, time, 4, self.get_damage_percent_reduction())
        self.on_hit_effects.append(DrunkenRage(source=self, attached_to=self, expires_at=time + 9999))
