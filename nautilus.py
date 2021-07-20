from units.unit import Unit
from synergies import Knight
from synergies import Ironclad

class Nautilus(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=750,
            starting_mana=50,
            total_mana=120,
            armor=45,
            magic_resist=45,
            attack_damage=65,
            attack_speed=0.55,
            attack_range=1,
            image_name='nautilus',
            synergies=[Knight, Ironclad],
            **kwargs,
        )
        self.cast_time = 0.3

    def get_anchor_slam_damage(self):
        base_damage = {
            1: 260,
            2: 280,
            3: 360
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_anchor_slam_stun_duration(self):
        return {
            1: 3,
            2: 4,
            3: 6
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        if not self.current_target:
            return
        self.deal_magic_damage(self.current_target, self.get_anchor_slam_damage(), is_multitarget=True)
        self.current_target.stun(time, self.get_anchor_slam_stun_duration())
        for unit in map.units:
            if unit.team == self.team:
                continue
            if self.current_target.distance(unit.row, unit.col) > 1:
                continue
            self.deal_magic_damage(unit, self.get_anchor_slam_damage()/2, is_multitarget=True)
            unit.stun(time, self.get_anchor_slam_stun_duration()/2)
