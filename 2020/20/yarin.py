import sys
from collections import defaultdict
from operator import neg
import re

MONSTER = """
..................#.
#....##....##....###
.#..#..#..#..#..#...
""".strip().split("\n")

tiles = [t.split("\n") for t in sys.stdin.read().split("\n\n") if t != ""]
tiles = {int(re.search('\d+', t[0])[0]): t[1:] for t in tiles}

offset2d = lambda pos, iterable: {tuple(map(sum, zip(pos, i))) for i in iterable}
center2d = lambda iterable: offset2d(tuple(map(neg, next(iter(iterable)))), iterable)
enumerate2d = lambda m: (((x, y), i) for y, r in enumerate(m) for x, i in enumerate(r))
to_sparse = lambda tile: {p for p, i in enumerate2d(tile) if i=="#"}
transpose_oriented_tile = lambda ot: (ot[0], ot[1]^4)

def flip(tile, orientation):
    if orientation & 1: tile = tile[::-1] # vertical
    if orientation & 2: tile = [row[::-1] for row in tile] # horizontal
    if orientation & 4: tile = ["".join(row) for row in zip(*tile)] # transpose
    return tile

# build edge map
edges = defaultdict(list)
for tid, tile in tiles.items():
    for o in range(8):
        edges[flip(tile, o)[0]].append((tid, o))

def get_tile(tid, orientation):
    return flip(tiles[tid], orientation)

def find_next_line(oriented_tile, flip_ot=lambda x:x):
    row = []
    while oriented_tile:
        row.append(oriented_tile)
        edge = get_tile(*flip_ot(oriented_tile))[-1]
        oriented_tile = next((flip_ot(ot) for ot in edges[edge] if ot[0] != oriented_tile[0]), None)
    return row

def find_upper_left():
    for tid, tile in tiles.items():
        for o in range(4):
            top, left = flip(tile, o)[0], flip(tile, o|4)[0]
            if len(edges[top]) == 1 and len(edges[left]) == 1:
                return tid, o

sea = [
    find_next_line(oriented_tile, transpose_oriented_tile)
    for oriented_tile in find_next_line(find_upper_left())]

print(sea[0][0][0] * sea[0][-1][0] * sea[-1][-1][0] * sea[-1][0][0])

land_locations = set()
for (v, u), oriented_tile in enumerate2d(sea):
    sparse_tile = ((x,y) for x,y in to_sparse(get_tile(*oriented_tile)) if 1<=x<=8 and 1<=y<=8)
    land_locations |= offset2d((v*8, u*8), sparse_tile)

for orientation in range(8):
    monster = center2d(to_sparse(flip(MONSTER, orientation)))
    occupied = set()
    for location in land_locations:
        placed_monster = offset2d(location, monster)
        if len(land_locations&placed_monster) == len(placed_monster):
            occupied |= placed_monster
    if len(occupied):
        print(len(land_locations-occupied))