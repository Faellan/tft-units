from units.unit import Unit
from synergies import Nightbringer
from synergies import Cavalier
from synergies import Brawler

class Sejuani(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=0,
            total_mana=60,
            armor=45,
            magic_resist=45,
            attack_damage=45,
            attack_speed=0.55,
            attack_range=1,
            image_name='sejuani',
            synergies=[Nightbringer, Cavalier, Brawler],
            **kwargs,
        )
        self.cast_time = 0.2

    def get_fury_of_the_north_damage(self):
        base_damage = {
            1: 300,
            2: 450,
            3: 750
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_fury_of_the_north_stun_duration(self):
        return {
            1: 2,
            2: 3,
            3: 4
        }[max(1, self.star_level)]

    def get_fury_of_the_north_bonus_resistances(self):
        return {
            1: 80,
            2: 125,
            3: 250
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if target:
            self.deal_magic_damage(target, self.get_fury_of_the_north_damage())
            target.stun(time, self.get_fury_of_the_north_stun_duration())
        self.flat_bonus_armor_modifiers.add_component(self.uuid, time, 4, self.get_fury_of_the_north_bonus_resistances())
        self.flat_bonus_magic_resist_modifiers.add_component(self.uuid, time, 4, self.get_fury_of_the_north_bonus_resistances())
