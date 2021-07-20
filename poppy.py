from units.unit import Unit
from synergies import Hellion
from synergies import Knight

class Poppy(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=600,
            starting_mana=40,
            total_mana=80,
            armor=40,
            magic_resist=40,
            attack_damage=80,
            attack_speed=0.55,
            attack_range=1,
            image_name='poppy',
            synergies=[Hellion, Knight],
            **kwargs,
        )
        self.cast_time = 0.5
        self.shield_at = None
        # TODO: mana lock during shield ?

    def get_buckler_toss_damage(self):
        base_damage = {
            1: 150,
            2: 250,
            3: 400
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_buckler_toss_shield(self):
        base_damage = {
            1: 250,
            2: 375,
            3: 525
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        self.deal_magic_damage(self.current_target, self.get_buckler_toss_damage())
        self.shield_at = time + 0.5  # TODO: depends on distance ?

    def tick(self, map, time):
        super().tick(map, time)
        if self.shield_at and time >= self.shield_at:
            self.shield_at = None
            self.add_shield_effect(self.get_buckler_toss_shield(), 999999)