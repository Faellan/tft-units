import utils
import uuid

from units.unit import Unit
from units.set5.daisy import Daisy
from synergies import Revenant
from synergies import Invoker
from synergies import Renewer

class Ivern(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=950,
            starting_mana=100,
            total_mana=180,
            armor=50,
            magic_resist=50,
            attack_damage=40,
            attack_speed=0.75,
            attack_range=2,
            image_name='ivern',
            synergies=[Revenant, Invoker, Renewer],
            **kwargs,
        )
        self.cast_time = 0.3
        self.daisy = None
        self.cast_at = None

    def get_daisy_health(self):
        return {
            1: 1500,
            2: 2400,
            3: 10000
        }[max(1, self.star_level)]

    def get_shockwave_base_damage(self):
        # AP scaling is done on daisy
        return {
            1: 250,
            2: 350,
            3: 1200,
        }[max(1, self.star_level)]

    def get_daisy_ap_bonus_per_cast(self):
        return {
            1: 100,
            2: 150,
            3: 300
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def summon_daisy(self, board, time):
        target = self.current_target or self.closest_hex_enemy(board)
        if target:
            target_row, target_col = utils.closest_empty_tile_from_pos(
                target.row, target.col, board,
                closest_from_row=self.row,
                closest_from_col=self.col
            )
        else:
            target_row, target_col = utils.closest_empty_tile_from_pos(
                self.row, self.col, board,
            )
        self.daisy = Daisy(
            ivern=self,
            health=self.get_daisy_health(),
            spell_base_damage=self.get_shockwave_base_damage(),
            team=self.team,
            row=target_row,
            col=target_col,
        )
        board.spawn_unit(self.daisy)

    def perform_spell(self, board, time):
        if not self.daisy or self.daisy.is_dead:
            self.summon_daisy(board, time)
        else:
            self.daisy.flat_bonus_spell_power_modifiers.add_component(uuid.uuid4(), time, 9999, self.get_daisy_ap_bonus_per_cast())

        self.cast_at = time + self.cast_time

    def tick(self, board, time):
        super().tick(board, time)
        if self.cast_at and time >= self.cast_at:
            self.cast_at = None
            self.daisy.cast_spell(board, time)