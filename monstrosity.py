from units.unit import Unit

class Monstrosity(Unit):
    def __init__(self, health, armor, magic_resist, attack_damage, **kwargs):
        super().__init__(
            cost=0,
            health=health,
            starting_mana=100,
            total_mana=100,
            armor=armor,
            magic_resist=magic_resist,
            attack_damage=attack_damage,
            attack_speed=0.8,
            attack_range=1,
            image_name='monstrosity',
            scale_hp_with_star_level=False,
            scale_ad_with_star_level=False,
            star_level=0,
            **kwargs,
        )
        self.mana_lock_time = 5
        self.cast_time = 0.3
        self.cast_lifesteal = 0.6
        self.ability_duration = 5
        self.cast_at = None

    def get_bonus_as(self):
        return 2.00 * self.get_spell_power() / 100

    def perform_spell(self, board, time):
        self.base_attack_speed_bonus_ratio_modifiers.add_component('monstrosity_cast', time, self.ability_duration, self.get_bonus_as())
        self.attack_speed_multiplier_modifiers.reset()
        self.cast_at = time

    def trigger_damage_dealt_to_other(self, target, damage, post_mitigation_damage, type):
        super().trigger_damage_dealt_to_other(target, damage, post_mitigation_damage, type)
        if type == 'physical' and self.cast_at and self._TIME <= self.cast_at + self.ability_duration:
            self.heal(self.cast_lifesteal * damage)

    def has_stun_prevention_effect(self):
        if self.cast_at and self._TIME <= self.cast_at + self.ability_duration:
            return True
        return super().has_stun_prevention_effect()