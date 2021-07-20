from units.unit import Unit

class Daisy(Unit):
    def __init__(self, ivern, health, spell_base_damage, **kwargs):
        super().__init__(
            cost=4,
            health=health,
            starting_mana=0,
            total_mana=0,
            armor=60,
            magic_resist=60,
            attack_damage=80,
            attack_speed=0.8,
            attack_range=1,
            image_name='daisy',
            star_level=ivern.star_level,
            scale_hp_with_star_level=False,
            **kwargs,
        )
        self.spell_base_damage = spell_base_damage
        self.cast_time = 0.5
        self.ivern = ivern
        self.spell_power = self.ivern.spell_power

    def perform_spell(self, map, time):
        target = self.current_target or self.closest_hex_enemy(map)
        if not target:
            return

        for unit in self.enemies(map):
            if unit.distance(target.row, target.col) <= 1:
                self.deal_magic_damage(unit, self.spell_base_damage * self.get_spell_power() / 100)
                unit.stun(time, 2)