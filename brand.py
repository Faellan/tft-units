import uuid

from units.unit import Unit
from synergies import Spellweaver
from synergies import Abomination
from dot import Dot

class Sear(Dot):
    def __init__(self, **kwargs):
        self.damage_per_tick = kwargs.pop('damage_per_tick')
        super().__init__(**kwargs)

    def trigger(self, map, time):
        self.owner.deal_magic_damage(self.unit, self.damage_per_tick)


class Brand(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=1,
            health=600,
            starting_mana=0,
            total_mana=20,
            armor=20,
            magic_resist=20,
            attack_damage=45,
            attack_speed=0.65,
            attack_range=3,
            image_name='brand',
            synergies=[Abomination, Spellweaver],
            **kwargs,
        )
        self.cast_time = 0.3
        self.mana_lock_time = 1.5

    def get_sear_total_damage(self):
        base_damage = {
            1: 600,
            2: 900,
            3: 1500
        }[max(1, self.star_level)]
        return base_damage * self.get_spell_power() / 100

    def get_sear_shred_ratio(self):
        return {
            1: 0.4,
            2: 0.5,
            3: 0.7
        }[max(1, self.star_level)]

    def perform_spell(self, board, time):
        targets_without_sear = [
            u for u in self.targetable_enemies(board)
            if not any([isinstance(dot, Sear) for dot in u.dots])
        ]
        targets = targets_without_sear if targets_without_sear else self.targetable_enemies(board)
        if not targets:
            return

        target = sorted(targets, key=lambda u: u.distance(self.row, self.col))[0]
        target.magic_resist_shred_percentage_modifiers.add_component(self.uuid, time, 12, self.get_sear_shred_ratio())

        for dot in target.dots:
            if isinstance(dot, Sear):
                dot.refresh(time)
                break
        else:
            target.dots.append(
                Sear(
                    owner=self,
                    unit=target,
                    time=time,
                    trigger_delay=1,
                    trigger_duration=12,
                    damage_per_tick=self.get_sear_total_damage()/12
                )
            )
