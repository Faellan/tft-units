from units.unit import Unit
from synergies import Nightbringer
from synergies import Skirmisher

class LeeSin(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=850,
            starting_mana=30,
            total_mana=70,
            armor=35,
            magic_resist=35,
            attack_damage=60,
            attack_speed=0.75,
            attack_range=1,
            image_name='lee_sin',
            synergies=[Nightbringer, Skirmisher],
            **kwargs,
        )
        self.cast_time = 0.2
        self.cripple_hex_range = 2
        self.cripple_duration = 4
        self.cripple_multiplier = 0.5

    def get_cripple_damage(self):
        base_damage = {
            1: 250,
            2: 350,
            3: 750
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        for unit in map.units:
            if unit.team == self.team:
                continue
            if unit.distance(self.row, self.col) > self.cripple_hex_range:
                continue
            self.deal_magic_damage(unit, self.get_cripple_damage(), is_multitarget=True)
            unit.attack_speed_multiplier_modifiers.add_component(self.uuid, time, self.cripple_duration, self.cripple_multiplier)
