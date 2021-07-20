from units.unit import Unit
from synergies import Forgotten
from synergies import Cannoneer

class MissFortune(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=700,
            starting_mana=0,
            total_mana=70,
            armor=25,
            magic_resist=25,
            attack_damage=55,
            attack_speed=0.8,
            attack_range=4,
            image_name='miss_fortune',
            synergies=[Forgotten, Cannoneer],
            **kwargs,
        )
        self.cast_time = 0.1
        self.make_it_rain_range = 1
        self.spell_row = None
        self.spell_col = None
        self.spell_period = 0.5
        self.nb_procs = 0
        self.last_proc_at = None

    def get_make_it_rain_damage(self):
        base_damage = {
            1: 250,
            2: 400,
            3: 750
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def proc_make_it_rain(self, map, time):
        for unit in map.units:
            if unit.team != self.team and unit.distance(self.spell_row, self.spell_col) <= self.make_it_rain_range:
                self.deal_magic_damage(unit, self.get_make_it_rain_damage()/4, is_multitarget=True)
                unit.apply_hemoragy(time, 6)

        self.nb_procs += 1
        self.last_proc_at = None if self.nb_procs >= 4 else time

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return
        self.nb_procs = 0
        self.spell_row = target.row
        self.spell_col = target.col
        self.proc_make_it_rain(map, time)


    def tick(self, map, time):
        super().tick(map, time)
        if self.last_proc_at and time >= self.last_proc_at + self.spell_period:
            self.proc_make_it_rain(map, time)