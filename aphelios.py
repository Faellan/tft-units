from units.unit import Unit
from synergies import Nightbringer
from synergies import Ranger

class Aphelios(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=650,
            starting_mana=0,
            total_mana=150,
            armor=25,
            magic_resist=25,
            attack_damage=65,
            attack_speed=0.85,
            attack_range=4,
            image_name='aphelios',
            synergies=[Nightbringer, Ranger],
            **kwargs,
        )
        self.cast_time = 0.5

    def get_dark_vigil_bonus_damage(self):
        base_damage = {
            1: 150,
            2: 200,
            3: 400
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_dark_vigil_number_of_targets(self):
        return {
            1: 5,
            2: 5,
            3: 10
        }[max(1, self.star_level)]

    def get_dark_vigil_ad_ratio(self):
        return {
            1: 3.5,
            2: 3.75,
            3: 4.75
        }[max(1, self.star_level)]

    def get_dark_vigil_damage(self):
        return self.get_dark_vigil_bonus_damage() + self.get_attack_damage() * self.get_dark_vigil_ad_ratio()

    def perform_spell(self, map, time):
        main_target = self.current_target or self.closest_hex_enemy(map)
        enemies = [u for u in map.units if u.team != self.team and u.is_targetable]
        if not enemies or not main_target:
            return
        targets = sorted(
            enemies,
            key=lambda u: main_target.distance(u.row, u.col)
        )[:self.get_dark_vigil_number_of_targets()]
        for target in targets:
            self.deal_physical_damage(target, self.get_dark_vigil_damage())
