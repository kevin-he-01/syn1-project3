#! /usr/bin/env python3
# import PIL

from typing import BinaryIO, Dict, List, Tuple
from struct import unpack
from math import floor, ceil
from numpy import linspace


# FILE = 'n37_w122_1arc_v3.bil'
# SOUTH = 37
# WEST = -122
NROWS = 3601
NCOLS = 3601
STRIDE = 2

elevation_data: List[List[int]] = []

# MAX_ELEV = 1100
MAX_ELEV = 100
TILE_COUNT = 40
# INTERVAL = 0.05

files: Dict[Tuple[int, int], BinaryIO] = dict()

COORDS_INCLUDED = [(37, -122), (37, -123), (38, -122), (38, -123)]

# Nice parameter to use:
# Ideal:
# Top left: 38.5, -122.65
# Bottom right: 37.2, -121.1
# 1.3 x 1.55
# Actual (Square):
# Top left: 38.65, -122.65
# Bottom right: 37.1, -121.1
# 1.55 x 1.55

for lat, long in COORDS_INCLUDED:
    latcode = ('n' if lat > 0 else 's') + str(abs(lat))
    longcode = ('e' if long > 0 else 'w') + str(abs(long))
    files[(lat, long)] = open('{}_{}_1arc_v3.bil'.format(latcode, longcode), 'rb')

OUTPUT_FILE = '../docs/elevation.dat'

try:
    def get_elevation(lat: float, long: float) -> int:
        north = ceil(lat)
        west = floor(long)
        ef = files[(north - 1, west)]
        lat_coord = floor((north - lat) * NROWS)
        long_coord = floor((long - west) * NCOLS)
        # print(lat_coord, long_coord)
        ef.seek((lat_coord * NCOLS + long_coord) * STRIDE)
        return unpack('<h', ef.read(STRIDE))[0]
    
    # def print_elevation_map(latend: float, longstart: float, latstart: float, longend: float):
    #     assert latstart <= latend
    #     assert longstart <= longend
    #     for lat in linspace(latend, latstart, TILE_COUNT)[:-1]:
    #         for long in linspace(longstart, longend, TILE_COUNT)[:-1]:
    #             try:
    #                 elev = get_elevation(lat, long)
    #             except KeyError:
    #                 print('XX', end='')
    #             else:
    #                 print('##' if elev > 0 else '  ', end='')
    #             # print('\x1b[48;2;{0};{0};{0}m  \x1b[0m'.format(floor(max(0, min(MAX_ELEV, elev)) * 255 / MAX_ELEV)), end='')
    #         print()


    # for i in range(NROWS):
    #     row = []
    #     for j in range(NCOLS):
    #         row.append(unpack('<h', ef.read(STRIDE)))
    #     elevation_data.append(row)

    # while True:
    #     lat, long = map(float, input("Input coordinate: ").split(", "))
    #     print(lat, long)
    #     print('Elevation: {}'.format(get_elevation(lat, long)))

    # while True:
    #     lat1, long1 = map(float, input("Top left: ").split(", "))
    #     lat2, long2 = map(float, input("Bottom right: ").split(", "))
    #     if not (lat2 <= lat1 and long1 <= long2):
    #         print('Invalid!')
    #         continue
    #     print_elevation_map(lat1, long1, lat2, long2)

    # for lat_inv in arange(0, 1, INTERVAL):
    #     for long in arange(WEST, WEST + 1, INTERVAL):
    #         lat = SOUTH + 1 - lat_inv
    #         elev = get_elevation(lat, long)
    #         assert elev != None, 'Bad: {} {}'.format(lat, long)
    #         print('\x1b[48;2;{0};{0};{0}m  \x1b[0m'.format(floor(max(0, min(MAX_ELEV, elev)) * 255 / MAX_ELEV)), end='')
    #     print()

    with open(OUTPUT_FILE, 'wb') as of:
        def out_iter():
            for lat in linspace(38.65, 37.1, 600):
                for long in linspace(-122.65, -121.1, 600):
                    elev = get_elevation(lat, long)
                    # clamp to 1 byte elevation
                    elev = max(0, min(255, elev))
                    yield elev
        of.write(bytes(out_iter()))
finally:
    for file in files.values():
        file.close()
