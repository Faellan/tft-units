from units.unit import Unit

class Voidspawn(Unit):
    def __init__(self, **kwargs):
        super().__init__(
            cost=0,
            health=1500,
            starting_mana=0,
            total_mana=0,
            armor=20,
            magic_resist=20,
            attack_damage=100,
            attack_speed=0.8,
            attack_range=1,
            image_name='voidspawn',
            scale_hp_with_star_level=False,
            scale_ad_with_star_level=False,
            star_level=0,
            **kwargs,
        )
        self.has_ticked = False

    def tick(self, board, time):
        super().tick(board, time)
        if not self.has_ticked:
            self.has_ticked = True
            for enemy in self.targetable_enemies(board):
                if enemy.distance(self.row, self.col) <= 2:
                    enemy.current_target = self