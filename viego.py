import utils

from units.unit import Unit
from units.set5.daisy import Daisy
from units.set5.monstrosity import Monstrosity
from units.set5.voidspawn import Voidspawn
from synergies import Forgotten
from synergies import Assassin
from dot import Dot

class ViegoHealthLoss(Dot):
    def __init__(self, **kwargs):
        self.max_health_ratio_loss_per_second = kwargs.pop('max_health_ratio_loss_per_second')
        super().__init__(**kwargs)

    def trigger(self, map, time):
        self.unit.take_magic_damage(self.unit.total_health * self.max_health_ratio_loss_per_second, self.owner)

class Viego(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=4,
            health=1000,
            starting_mana=0,
            total_mana=40,
            armor=40,
            magic_resist=40,
            attack_damage=70,
            attack_speed=1,
            attack_range=1,
            image_name='viego',
            synergies=[Forgotten, Assassin],
            **kwargs,
        )
        self.cast_time = 0.1

        self.cast_at = None
        self.spell_target = None
        self.number_of_ticks = 10
        self.ticks_remaining = 0
        self.ticks_delay = 0.5
        self.next_tick_at = None

    def get_sovereigns_domination_base_damage(self):
        return {
            1: 180,
            2: 300,
            3: 1500
        }[max(1, self.star_level)] * self.get_spell_power() / 100

    def get_sovereigns_domination_health_loss_per_second(self):
        return {
            1: 0.15,
            2: 0.07,
            3: 0.00,
        }[max(1, self.star_level)]

    def summon_spell_target(self, board, time):
        row, col = self.spell_target.closest_empty_tile(board)
        kwargs = {
            'row': row,
            'col': col,
            'team': self.team,
            'star_level': self.spell_target.star_level,
            'items': self.spell_target.items,
        }
        if self.spell_target.__class__ is Daisy:
            kwargs.update({
                'ivern': self.spell_target.ivern,
                'health': self.spell_target.health,
                'spell_base_damage': self.spell_target.spell_base_damage
            })
            kwargs.pop('star_level')
        if self.spell_target.__class__ is Monstrosity:
            kwargs.update({
                'health': self.spell_target.total_health,
                'armor': self.spell_target.base_armor,
                'magic_resist': self.spell_target.base_magic_resist,
                'attack_damage': self.spell_target.base_attack_damage,
            })
            kwargs.pop('star_level')
        if self.spell_target.__class__ is Voidspawn:
            kwargs.pop('star_level')

        summoned_unit = self.spell_target.__class__(**kwargs)
        summoned_unit.dots.append(
            ViegoHealthLoss(
                owner=self,
                unit=summoned_unit,
                time=time,
                trigger_delay=1,
                trigger_duration=9999,
                max_health_ratio_loss_per_second=self.get_sovereigns_domination_health_loss_per_second()
            )
        )
        board.spawn_unit(summoned_unit)

    def perform_spell(self, board, time):
        self.spell_target = self.current_target or self.closest_hex_enemy(board)
        if not self.spell_target:
            return
        self.cast_at = time
        self.ticks_remaining = self.number_of_ticks
        self.next_tick_at = time + 0.01
        self.spell_target.stun(time, 5)
        # hack to make it enable to auto
        self.moves_until = time + 5

    def tick(self, board, time):
        super().tick(board, time)
        if self.next_tick_at and self.is_stunned:  # cancel cast
            self.spell_target.stunned_until = time
            self.moves_until = time
        elif self.next_tick_at and time >= self.next_tick_at:
            damage = self.get_sovereigns_domination_base_damage() * (1 + (self.number_of_ticks - self.ticks_remaining)//2)
            self.deal_magic_damage(self.spell_target, damage)
            if self.spell_target.health < 0:
                if not self.spell_target.revive_with:
                    self.summon_spell_target(board, time)
                self.next_tick_at = None
                self.ticks_remaining = 0
                self.moves_until = -1
            else:
                self.ticks_remaining -= 1
                if self.ticks_remaining:
                    self.next_tick_at = time + self.ticks_delay
                else:
                    self.next_tick_at = None
                    self.spell_target = None