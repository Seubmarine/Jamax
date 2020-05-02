import pyxel as px
from vector import Vector2


class Player:
    def __init__(self, positon: Vector2, dimension: Vector2):
        self.positon = positon
        self.dimension = dimension

        self.sprite_front = (0, 16, 12, 12)
        self.sprite_back = (12, 16, 12, 12)
        self.sprite_left = (24, 16, 12, 12)
        self.sprite_right = (24, 16, -12, 12)
        self.current_sprite = self.sprite_front

    @staticmethod
    def get_input_velocity():
        direction = Vector2.ZERO
        if px.btn(px.KEY_UP):
            direction += Vector2.UP
        if px.btn(px.KEY_RIGHT):
            direction += Vector2.RIGHT
        if px.btn(px.KEY_DOWN):
            direction += Vector2.DOWN
        if px.btn(px.KEY_LEFT):
            direction += Vector2.LEFT
        return direction

    def sprite_change(self, direction):
        if direction.y > 0:
            self.current_sprite = self.sprite_front
        elif direction.y < 0:
            self.current_sprite = self.sprite_back
        elif direction.x > 0:
            self.current_sprite = self.sprite_left
        elif direction.x < 0:
            self.current_sprite = self.sprite_right

    def update(self):
        self.direction = self.get_input_velocity()
        self.sprite_change(self.direction)
        self.positon += self.direction

    def draw(self):
        px.blt(self.positon.x, self.positon.y, 0, *self.current_sprite, 0)


class Main:
    def __init__(self):
        px.init(256, 256)
        px.load("assets/assetpack1.pyxres")
        self.player = Player(Vector2.ZERO, Vector2(16, 16))

        px.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        px.cls(0)
        px.bltm(0, 0, 0, 0, 0, 32, 32, 0)
        self.player.draw()

if __name__ == "__main__":
    Main()
