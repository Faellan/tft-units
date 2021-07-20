from units.unit import Unit
from synergies import Sentinel
from synergies import Legionnaire
from synergies import Skirmisher

class Irelia(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=40,
            total_mana=80,
            armor=40,
            magic_resist=40,
            attack_damage=70,
            attack_speed=0.8,
            attack_range=1,
            image_name='irelia',
            synergies=[Sentinel, Legionnaire, Skirmisher],
            **kwargs,
        )
        self.cast_time = 0.2
        self.spell_performed_at = None
        self.mana_lock_time = 4
        self.current_percent_damage_reduction = None

    def get_defiant_dance_damage(self):
        base_damage = {
            1: 250,
            2: 400,
            3: 650
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_defiant_dance_percent_damage_reduction(self):
        return {
            1: 40,
            2: 50,
            3: 60
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        self.spell_performed_at = time
        self.current_percent_damage_reduction = self.get_defiant_dance_percent_damage_reduction()
        self.percent_damage_reduction_modifiers.add_component(self.uuid, time, 4, self.current_percent_damage_reduction, keep_highest_value=True)

    def before_auto_attack(self, target, map, time):
        super().before_auto_attack(target, map, time)
        if self.current_percent_damage_reduction and self.current_percent_damage_reduction < 90:
            self.current_percent_damage_reduction += 10
            self.percent_damage_reduction_modifiers.add_component(self.uuid, time, self.spell_performed_at + 4 - time, self.current_percent_damage_reduction, keep_highest_value=True)

    def tick(self, map, time):
        super().tick(map, time)
        if self.spell_performed_at and time >= self.spell_performed_at + 4:
            if self.current_target:
                self.deal_magic_damage(self.current_target, self.get_defiant_dance_damage())
                self.current_percent_damage_reduction = None
                self.spell_performed_at = None
