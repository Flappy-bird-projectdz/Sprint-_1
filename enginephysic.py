from utilis import GameConfig

class PhysicsEngine:
    def __init__(self):
        self.gravity = GameConfig.GRAVITY
        self.jump_power = 6

    def ap_dung_trong_luc(self, character):
        character.update(self.gravity)

    def ap_dung_luc_day(self, character):
        character.flap(self.jump_power)
