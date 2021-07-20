from units.unit import Unit
from synergies import Dawnbringer
from synergies import Renewer

class Soraka(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=550,
            starting_mana=30,
            total_mana=70,
            armor=25,
            magic_resist=25,
            attack_damage=40,
            attack_speed=0.6,
            attack_range=3,
            image_name='soraka',
            synergies=[Dawnbringer, Renewer],
            **kwargs,
        )
        self.cast_time = 0.2
        self.equinox_range = 1
        self.equinox_percent_mana_increase = 35

    def get_equinox_damage(self):
        base_damage = {
            1: 150,
            2: 250,
            3: 400
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        enemies = [u for u in map.units if u.team != self.team and u.is_targetable]
        if not enemies:
            return
        target = sorted(
            enemies,
            key=lambda e: e.mana / e.get_effective_total_mana() if e.total_mana else 0,
            reverse=True
        )[0]
        for unit in map.units:
            if unit.team == self.team:
                continue
            if unit.distance(target.row, target.col) > self.equinox_range:
                continue
            self.deal_magic_damage(unit, self.get_equinox_damage(), is_multitarget=True)
            unit.shroud(self.equinox_percent_mana_increase)
