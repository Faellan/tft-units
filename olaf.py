from units.unit import Unit
from synergies import Skirmisher
from synergies import Sentinel

class Olaf(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=650,
            starting_mana=0,
            total_mana=0,
            armor=35,
            magic_resist=35,
            attack_damage=65,
            attack_speed=0.7,
            attack_range=1,
            image_name='olaf',
            synergies=[Sentinel, Skirmisher],
            **kwargs,
        )
        self.mana_lock_time = 4

    def get_berserker_rage_healing(self):
        base_healing = {
            1: 25,
            2: 35,
            3: 75
        }[max(1, self.star_level)]
        return base_healing * self.get_spell_power() / 100

    def get_berserker_rage_bonus_as(self):
        base_as = {
            1: 0.02,
            2: 0.03,
            3: 0.04
        }[max(1, self.star_level)]
        return base_as * self.get_spell_power() / 100

    def get_olaf_bonus_as(self):
        missing_health = self.total_health - self.health
        missing_health_percent = 100 * missing_health / self.total_health
        return self.get_berserker_rage_bonus_as() * missing_health_percent

    def before_auto_attack(self, target, map, time):
        super().before_auto_attack(target, map, time)
        self.heal(self.get_berserker_rage_healing())