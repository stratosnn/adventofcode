import unittest
from pprint import pprint
import itertools
import math
import re


def read_data(filename):
    with open(filename) as f:
        tiles = dict()
        for l in f:
            m = re.match(r'Tile (\d+):', l)
            if m:
                tile_id = int(m.group(1))
                line = next(f).strip()
                tile = []
                while line:
                    tile.append(line)
                    try:
                        line = next(f).strip()
                    except StopIteration:
                        line = ''
                tiles[tile_id] = tile
        return tiles


def map_borders(tile_id, tile, db={}):
    borders = []
    borders.append(tile[0])
    borders.append(tile[0][::-1])
    borders.append(tile[-1])
    borders.append(tile[-1][::-1])

    l = ''.join([t[0] for t in tile])
    r = ''.join([t[-1] for t in tile])

    borders.append(l)
    borders.append(l[::-1])
    borders.append(r)
    borders.append(r[::-1])

    for b in borders:
        db.setdefault(b, []).append(tile_id)


def rotate(tile):
    return list(map("".join, zip(*reversed(tile))))


def flip(tile):  # vertical flip
    return [''.join(reversed(l)) for l in tile]


def hflip(tile):  # horizontal flip
    return tile[::-1]


def map_borders2(tile_id, tile, db={}):
    # rotation
    t = tile
    for i in range(4):
        t = rotate(t)
        db.setdefault(t[0], {}).update({tile_id: t})

    # vertical flip
    t = flip(tile)
    for i in range(4):
        t = rotate(t)
        db.setdefault(t[0], {}).update({tile_id: t})


def create_hases(tiles={}):
    db = dict()
    for tile_id, tile in tiles.items():
        map_borders(tile_id, tile, db)
    return db


def create_hashes2(tiles={}):
    db = dict()
    for tile_id, tile in tiles.items():
        map_borders2(tile_id, tile, db)
    return db



def get_other(h, ours, db):
    keys = db[h].keys()
    try:
        other = next(filter(lambda x: x not in ours, keys))
        return other, db[h][other]
    except StopIteration:
        return None, None


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class MyTestCase(unittest.TestCase):
    def test_part1(self):
        data = read_data('input20.txt')
        db = create_hases(data)
        #pprint(db)
        print(len(data))
        singles = set()
        for tid in db.values():
            if len(tid) == 1:
                singles.add(tid[0])
        #pprint(singles)

        neighbours = dict()
        for t in db.values():
            if len(t) == 2:
                neighbours.setdefault(t[0], set()).add(t[1])
                neighbours.setdefault(t[1], set()).add(t[0])
        pprint(neighbours)

        sm = 1
        for tid, n in neighbours.items():
            if len(n) == 2:
                print(f'corener {tid}')
                sm *= tid
        print(sm)
        #print(len(neighbours))


    def test_part2(self):
        data = read_data('test20.txt')
        db = create_hases(data)

        singles = set()
        for tid in db.values():
            if len(tid) == 1:
                singles.add(tid[0])

        neighbours = dict()
        for t in db.values():
            if len(t) == 2:
                neighbours.setdefault(t[0], set()).add(t[1])
                neighbours.setdefault(t[1], set()).add(t[0])

        # pprint(neighbours)
        print(f'len data {len(data)}')

        db2 = create_hashes2(data)
        # pprint(db2)
        corners = dict(filter(lambda p: len(p[1]) == 2, neighbours.items()))
        print(corners)

        corner = list(corners.keys())[-1] # TODO change to 0
        #for corner in corners.keys():
        result = []

        print(f'corner {corner} out of {len(corners)}')

        done = False
        last_id = corner
        round_id = last_id
        used = []
        result.append(data[last_id])

        while round_id:
            cnt = 1
            used.append(last_id)
            while last_id:
                h = result[-1][-1]
                last_id, t = get_other(h, used, db2)
                if last_id:
                    result.append(t)
                    used.append(last_id)
                    cnt += 1

            tile = result[-cnt]
            r = ''.join([t[-1] for t in tile])
            last_id, tile = get_other(r, used, db2)
            round_id = last_id
            if tile:
                result.append(tile)
                #used.append(last_id)

            # pprint(result)
        print(len(result))

        no_borders = []
        for t in result:
            nt = [x[1:-1] for x in t]
            nt = nt[1:-1]
            no_borders.append(nt)

        print(len(no_borders), len(no_borders[0]))

        sz = int(math.sqrt(len(result)))

        pre_image = []
        for t in no_borders:
            pre_image += t

        #pprint(pre_image)
        image = []
        for ix in range(len(pre_image)):
            l = pre_image[ix]
            pos = ix % (sz*8)
            if ix < sz*8:
                image.append(l)
            else:
                image[pos] = image[pos] + l
        pprint(rotate(rotate(flip(image))))










if __name__ == '__main__':
    unittest.main()
