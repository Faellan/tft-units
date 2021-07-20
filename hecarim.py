from units.unit import Unit
from synergies import Cavalier
from synergies import Forgotten

class Hecarim(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=75,
            total_mana=125,
            armor=45,
            magic_resist=45,
            attack_damage=55,
            attack_speed=0.55,
            attack_range=1,
            image_name='hecarim',
            synergies=[Cavalier, Forgotten],
            **kwargs,
        )
        self.damage_at = None
        self.cast_time = 0.01
        self.ticks_remaining = 0
        self.next_tick_at = None

    def get_spirit_of_dread_damage(self):
        base_damage = {
            1: 200,
            2: 400,
            3: 600
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_spirit_of_dread_heal(self):
        base_heal = {
            1: 350,
            2: 350,
            3: 350
        }[max(1, self.star_level)]
        return base_heal * self.get_spell_power() / 100

    def perform_spell(self, map, time):
        self.next_tick_at = time + 0.01
        self.ticks_remaining = 4

    def tick(self, map, time):
        super().tick(map, time)
        if self.ticks_remaining and self.next_tick_at and time >= self.next_tick_at:
            self.ticks_remaining -= 1
            self.next_tick_at += 1.0
            self.heal(self.get_spirit_of_dread_heal()/4)
            for unit in map.units:
                if unit.team == self.team:
                    continue
                if unit.distance(self.row, self.col) > 1:
                    continue
                self.deal_magic_damage(unit, self.get_spirit_of_dread_damage()/4, is_multitarget=True)
