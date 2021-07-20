from units.unit import Unit
from synergies import Nightbringer
from synergies import Legionnaire
from on_hit_effect import OnHitEffect

class BurningBlade(OnHitEffect):
    def proc(self, target):
        if self.source.burning_blade_stacks:
            self.source.deal_true_damage(target, self.source.get_burning_blade_on_hit_damage())

class Yasuo(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=3,
            health=800,
            starting_mana=0,
            total_mana=40,
            armor=35,
            magic_resist=35,
            attack_damage=60,
            attack_speed=1,
            attack_range=1,
            image_name='yasuo',
            synergies=[Nightbringer, Legionnaire],
            **kwargs,
        )
        self.cast_time = 0.5
        self.burning_blade_stacks = 0
        self.on_hit_effects.append(BurningBlade(source=self, attached_to=self, expires_at=9999))

    def get_burning_blade_magic_damage(self):
        return {
            1: 250,
            2: 350,
            3: 650
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def get_burning_blade_on_hit_damage_per_stack(self):
        base_on_hit_damage = {
            1: 25,
            2: 35,
            3: 65
        }[max(1, self.star_level)]
        return base_on_hit_damage * self.get_spell_power() / 100

    def get_burning_blade_on_hit_damage(self):
        return self.burning_blade_stacks * self.get_burning_blade_on_hit_damage_per_stack()

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        self.burning_blade_stacks += 1
        self.deal_magic_damage(target, self.get_burning_blade_magic_damage())
