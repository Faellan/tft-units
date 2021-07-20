from units.unit import Unit
from synergies import Forgotten
from synergies import Legionnaire


class Draven(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=700,
            starting_mana=0,
            total_mana=40,
            armor=30,
            magic_resist=30,
            attack_damage=90,
            attack_speed=0.75,
            attack_range=3,
            image_name='draven',
            synergies=[Forgotten, Legionnaire],
            **kwargs,
        )
        self.cast_time = 0.01
        self.nb_axes_in_hand = 0
        self.axe_travel_time = 1
        self.axes_back_at = []
        self.add_axe_next_auto = False

    def get_spinning_axes_bonus_damage(self):
        base_damage = {
            1: 150,
            2: 200,
            3: 800
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_spinning_axes_ad_ratio(self):
        return {
            1: 1.7,
            2: 1.8,
            3: 3.4
        }[max(1, self.star_level)]

    def get_spinning_axes_damage(self):
        return self.get_spinning_axes_bonus_damage() + self.get_attack_damage() * self.get_spinning_axes_ad_ratio()

    def perform_spell(self, map, time):
        self.add_axe_next_auto = True

    def auto_attack(self, target, map, time, ad_ratio=1.0, apply_on_hit=True, apply_mana_increase=True, is_from_runaan=False, bonus_damage=0):
        if self.add_axe_next_auto or self.nb_axes_in_hand > 0:
            if not self.add_axe_next_auto:
                self.nb_axes_in_hand -= 1
            self.add_axe_next_auto = False
            ad_ratio = self.get_spinning_axes_ad_ratio()
            bonus_damage += self.get_spinning_axes_bonus_damage()
            self.axes_back_at.append({
                'time': time + self.axe_travel_time,
                'row': self.row,
                'col': self.col,
            })

        super().auto_attack(target, map, time, ad_ratio, apply_on_hit, apply_mana_increase, is_from_runaan, bonus_damage)

    def tick(self, map, time):
        super().tick(map, time)
        if self.axes_back_at and time >= self.axes_back_at[0]['time']:
            if self.nb_axes_in_hand < 2 and self.row == self.axes_back_at[0]['row'] and self.col == self.axes_back_at[0]['col']:
                self.nb_axes_in_hand += 1
            self.axes_back_at.pop(0)