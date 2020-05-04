import pyxel as px
from vector import Vector2
from utilities import get_cell, cell_list, detect_collision
from time import time
from random import randrange

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
                    self.cell_to_check.append(
                        self.player_position_in_cell + cell_pos)
        self.player_position_in_cell *= 8

    def collide_with_wall(self, test_pos):
        for cell in self.cell_to_check:
            if detect_collision(test_pos, self.dimension, cell*8, Vector2(8, 8)):
                return True
        return False

    def slide_along_wall(self):
        # collision is done her too
        if self.direction.x != 0:
            self.newdir = Vector2(self.direction.x, 0)
            if self.collide_with_wall(self.newdir + self.position):
                self.position -= self.newdir

        if self.direction.y != 0:
            self.newdir = Vector2(0, self.direction.y)
            if self.collide_with_wall(self.newdir + self.position):
                self.position -= self.newdir

    def update(self):
        self.direction = self.get_input_velocity() * 2
        self.sprite_change(self.direction)
        self.find_wall_around_player()
        self.slide_along_wall()
        self.position += self.direction

    def draw(self):
        px.blt(self.position.x, self.position.y, 0, *self.current_sprite, 0)
        if self.debug_mode:
            for i in self.cell_to_check:
                px.rectb(i.x * 8, i.y * 8, 8, 8, 6)
            px.rectb(self.position.x, self.position.y,
                     self.dimension.x, self.dimension.y, 6)


class Block:
    @staticmethod
    def replace_block(cell_position, tile_index):
        px.tilemap(0).set(cell_position.x, cell_position.y, tile_index)

    def __init__(self, cell_position: Vector2):
        self.cell_position = cell_position
        self.cell_position_on_screen = cell_position * 8


class Block_On_Fire(Block):
    def __init__(self, cell_position: Vector2):
        super().__init__(cell_position)
        self.firesprite = [
            (16, 0, 8, 8),
            (24, 0, 8, 8),
            (32, 0, 8, 8)
        ]
        self.current_sprite = self.firesprite[0]

    def update(self, time):
        modulo = time % 3
        if modulo < 1:
            self.current_sprite = self.firesprite[0]

        elif modulo < 2:
            self.current_sprite = self.firesprite[1]

        elif modulo < 3:
            self.current_sprite = self.firesprite[2]

    def draw(self):
        px.blt(self.cell_position_on_screen.x,
               self.cell_position_on_screen.y, 0, *self.current_sprite, 0)

def random_hazard(hazard_list:list):
    for _i in range(randrange(30, 40)):
        hazard_list.append(Block_On_Fire(Vector2(randrange(2,30),randrange(2,30))))
class Main:
    def __init__(self):
        px.init(256, 256, caption='Jamax')
        px.load("assets/assetpack1.pyxres")
        self.player = Player(Vector2(50, 50), Vector2(12, 12))
        self.hazard_list = []
        random_hazard(self.hazard_list)
        # print(self.hazard_list)
        self.TIME_WHEN_APP_OPEN = time()
        self.buffer_time = self.TIME_WHEN_APP_OPEN
        self.actual_time = 0
        self.score = 0
        self.highscore = 0
        self.you_die = False

        px.mouse(True)
        px.run(self.update, self.draw)
    
    def check_hazard(self):
        if px.btn(px.MOUSE_LEFT_BUTTON):
            for i in self.hazard_list:
                if i.cell_position == self.mouse // 8:
                    # print('bleu', i.cell_position_on_screen.distancefromvector(self.player.position))
                    if i.cell_position_on_screen.distancefromvector(self.player.position) < 600:
                        self.hazard_list.remove(i)
                        self.score += 1
        

    def check_time(self):
        self.t = time()
        self.actual_time = self.t - self.buffer_time
        # print(self.actual_time)
        if self.actual_time >= 30:
            # print('b')
            self.buffer_time = time()
            random_hazard(self.hazard_list)

    def update(self):
        self.mouse = Vector2(px.mouse_x, px.mouse_y)
        self.check_time()
        self.player.update()
        for i in self.hazard_list:
            i.update(self.actual_time)
        self.check_hazard()
        self.how_much_fire = len(self.hazard_list)
        if self.how_much_fire > 45:
            self.you_die = True

        if self.how_much_fire == 0:
            self.score += 15
            self.buffer_time = time()
            random_hazard(self.hazard_list)

        if self.you_die:
            # print('a')
            self.hazard_list.clear()
            random_hazard(self.hazard_list)
            if self.score > self.highscore:
                print('uui')
                self.highscore = self.score
            self.score = 0
            self.you_die = False


    def draw(self):
        px.cls(0)
        px.bltm(0, 0, 0, 0, 0, 32, 32, 0)
        self.player.draw()
        for i in self.hazard_list:
            i.draw()
        px.text(17,9,'score: '+ str(self.score), px.COLOR_WHITE)
        px.text(17, 18, 'Fire count: ' + str(self.how_much_fire), px.COLOR_WHITE)
        px.text(178, 9, 'time remaining: ' + str( 30 - int(self.actual_time)), px.COLOR_WHITE)
        px.text(178 , 18, 'highscore: '+ str(self.highscore), px.COLOR_WHITE )

if __name__ == "__main__":
    Main()
