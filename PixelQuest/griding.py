from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
import json


def write_map():
    level = []
    row = SCREEN_WIDTH // TILE_SIZE
    column = SCREEN_HEIGHT // TILE_SIZE
    for y in range(column):
        level.append('')
        for x in range(row):
            level[y] += '.'

    with open("map.json", 'w') as f:
        json.dump(level, f, indent=4)


def read_map(filename):
    with open(filename, 'r') as f:
        return json.load(f)



