import pyxel as px
from vector import Vector2

cell_list = {0: "ground", 1: "wall"}


def get_cell(position_on_tilemap: Vector2):
    if position_on_tilemap.x >= 0 and position_on_tilemap.y >= 0:
        return px.tilemap(0).get(position_on_tilemap.x, position_on_tilemap.y)
    else:
        return None


def detect_collision(r1, rd1, r2, rd2):
    return r1.x + rd1.x >= r2.x and r1.x <= r2.x + rd2.x and r1.y + rd1.y >= r2.y and r1.y <= r2.y + rd2.y
