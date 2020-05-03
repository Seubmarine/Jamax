import pyxel as px
from vector import Vector2
from utilities import get_cell, cell_list, detect_collision
from time import time


class Player:
    def __init__(self, position: Vector2, dimension: Vector2):
        self.position = position
        self.dimension = dimension

        self.sprite_front = (0, 16, 12, 12)
        self.sprite_back = (12, 16, 12, 12)
        self.sprite_left = (24, 16, 12, 12)
        self.sprite_right = (24, 16, -12, 12)
        self.current_sprite = self.sprite_front

        self.debug_mode = False

        self.cell_around_player = [Vector2(-1, -1), Vector2(0, -1), Vector2(1, -1), Vector2(2, -1),
                                   Vector2(-1, 0), Vector2(2, 0),
                                   Vector2(-1, 1), Vector2(2, 1),
                                   Vector2(-1, 2), Vector2(0, 2), Vector2(1, 2), Vector2(2, 2)]

    def get_input_velocity(self):
        direction = Vector2.ZERO
        if px.btn(px.KEY_UP):
            direction += Vector2.UP
        if px.btn(px.KEY_RIGHT):
            direction += Vector2.RIGHT
        if px.btn(px.KEY_DOWN):
            direction += Vector2.DOWN
        if px.btn(px.KEY_LEFT):
            direction += Vector2.LEFT
        if px.btnp(px.KEY_A):
            self.debug_mode = not self.debug_mode
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

    def find_wall_around_player(self):
        self.player_position_in_cell = self.position // 8
        self.cell_to_check = []
        for cell_pos in self.cell_around_player:
            cell_type = get_cell(self.player_position_in_cell + cell_pos)
            if cell_type != None:
                if cell_list[cell_type] == "wall":
                    self.cell_to_check.append(self.player_position_in_cell + cell_pos)
        self.player_position_in_cell *= 8


    def collide_with_wall(self, test_pos):
        for cell in self.cell_to_check:
            if detect_collision(test_pos, self.dimension, cell*8, Vector2(8,8)):
                return True
        return False

    def slide_along_wall(self):
        #collision is done her too
        if self.direction.x != 0:
            self.newdir = Vector2(self.direction.x, 0)
            if self.collide_with_wall(self.newdir + self.position):
                self.position -= self.newdir

        if self.direction.y != 0:
            self.newdir = Vector2(0, self.direction.y)
            if self.collide_with_wall(self.newdir + self.position):
                self.position -= self.newdir

    def update(self):
        self.direction = self.get_input_velocity()
        self.sprite_change(self.direction)
        self.find_wall_around_player()
        self.slide_along_wall()
        self.position += self.direction


    def draw(self):
        px.blt(self.position.x, self.position.y, 0, *self.current_sprite, 0)
        if self.debug_mode:
            for i in self.cell_to_check:
                px.rectb(i.x * 8, i.y* 8, 8, 8, 6)
            px.rectb(self.position.x, self.position.y, self.dimension.x, self.dimension.y, 6)


class Main:
    def __init__(self):
        px.init(256, 256, caption='Jamax', border_color=0xCDC6C0)
        px.load("assets/assetpack1.pyxres")
        self.player = Player(Vector2(50,50), Vector2(12, 12))
        self.time_since_app_is_open = time()
        px.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        px.cls(0)
        px.bltm(0, 0, 0, 0, 0, 32, 32, 0)
        self.player.draw()


if __name__ == "__main__":
    Main()
