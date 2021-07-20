from units.unit import Unit
from synergies import Forgotten
from synergies import Knight

class Thresh(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=800,
            starting_mana=40,
            total_mana=80,
            armor=40,
            magic_resist=40,
            attack_damage=75,
            attack_speed=0.6,
            attack_range=2,
            image_name='thresh',
            synergies=[Forgotten, Knight],
            **kwargs,
        )
        self.cast_time = 0.5
        self.pull_count = 0
        self.next_pull_at = None
        self.pull_target = None

    def get_death_sentence_damage(self):
        base_damage = {
            1: 200,
            2: 400,
            3: 1000
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_death_sentence_stun_duration(self):
        return {
            1: 2,
            2: 3,
            3: 4
        }[max(1, self.star_level)]

    def perform_spell(self, map, time):
        self.pull_target = self.farthest_hex_enemy(map)
        self.pull_count = 0
        if self.pull_target:
            self.next_pull_at = time + 1
            self.pull_target.stun(time, self.get_death_sentence_stun_duration())
            # hack so that thresh doesn't attack during hook
            # will need rework (same with viego)
            self.move_to(self.row, self.col, time, move_time=self.get_death_sentence_stun_duration())
            self.deal_magic_damage(self.pull_target, self.get_death_sentence_damage())

    def pull(self, map, time):
        if not self.pull_target:
            return
        cell = self.pull_target.closest_empty_tile(map, closest_from_row=self.row, closest_from_col=self.col)
        if self.pull_target.distance(cell[0], cell[1]) > 1:
            return
        if self.distance(cell[0], cell[1]) >= self.distance(self.pull_target.row, self.pull_target.col):
            return
        self.pull_target.move_to(cell[0], cell[1], time, move_time=0.01)

    def tick(self, map, time):
        super().tick(map, time)
        if self.pull_target and self.next_pull_at and time >= self.next_pull_at:
            self.pull_count += 1
            self.pull(map, time)

            if self.pull_count < self.get_death_sentence_stun_duration():
                self.next_pull_at = time + 1
            else:
                self.next_pull_at = None
                self.pull_count = 0
                self.pull_target = None
