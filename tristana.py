from units.unit import Unit
from synergies import Hellion
from synergies import Cannoneer

class Tristana(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=550,
            starting_mana=75,
            total_mana=125,
            armor=20,
            magic_resist=20,
            attack_damage=65,
            attack_speed=0.8,
            attack_range=5,
            image_name='tristana',
            synergies=[Hellion, Cannoneer],
            **kwargs,
        )
        self.cast_time = 0.1
        self.jump_duration = 0.8

    def get_rocket_jump_bonus_as_ratio(self):
        base_as_ratio = {
            1: 1.25,
            2: 1.5,
            3: 1.75
        }[max(1, self.star_level)]
        return base_as_ratio * self.get_spell_power() / 100

    def get_best_tile_to_escape(self, map):
        best_tile = None
        best_tile_dist = None
        for row in range(8):
            for col in range(7):
                if not map.is_tile_empty(row, col):
                    continue
                closest_enemy = sorted(
                    [e for e in map.units if e.team != self.team],
                    key=lambda e: e.distance(row, col)
                )[0]
                tile_dist = closest_enemy.distance(row, col)
                if best_tile is None or tile_dist > best_tile_dist:
                    best_tile = (row, col)
                    best_tile_dist = tile_dist
        return best_tile

    def perform_spell(self, map, time):
        self.closest_enemy = self.closest_hex_enemy(map)
        if self.closest_enemy and self.closest_enemy.distance(self.row, self.col) <= 1:
            target_pos = self.get_best_tile_to_escape(map)
            self.move_to(target_pos[0], target_pos[1], time, self.jump_duration)
        else:
            farthest_enemy = self.farthest_hex_enemy(map)
            if farthest_enemy:
                target_pos = farthest_enemy.closest_empty_tile(map, farthest_from_row=self.row, farthest_from_col=self.col)
                self.move_to(target_pos[0], target_pos[1], time, self.jump_duration)
                self.current_target = farthest_enemy
        self.base_attack_speed_bonus_ratio_modifiers.add_component(self.uuid, time, 4, self.get_rocket_jump_bonus_as_ratio())
