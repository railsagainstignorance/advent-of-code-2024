import sys
sys.path.append('../')
sys.path.append('../../')

import re
import math
import pprint

from utils import *

instances = [
    {
        'input': '''\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############''',
    'num_cheats_by_picoseconds_saved': {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
        },
    'min_time_saved_by_cheats': 40,
    'total_num_cheats_saving_more_than_min_time': 2
    },    
    {
        'input': "../puzzle1/input.txt",
        'min_time_saved_by_cheats': 100

    },
]

attrs = [
    'num_cheats_by_picoseconds_saved',
    'total_num_cheats_saving_more_than_min_time',
    ]

def solve( instance ):

    s_char = 'S'
    e_char = 'E'
    wall_char = '#'
    track_char = '.'
    min_time_saved_by_cheats = instance['min_time_saved_by_cheats']

    def parse_input( input ):
        char_yx_grid = get_char_yx_array_from_input( input )
        s_coord = None
        e_coord = None
        max_x = len(char_yx_grid[0]) -1
        max_y = len(char_yx_grid) -1

        for y in range( 1, max_y ):
            for x in range( 1, max_x ):
                char = char_yx_grid[y][x]
                if char == s_char:
                    s_coord = (x,y)
                elif char == e_char:
                    e_coord = (x,y)

        return char_yx_grid, max_x, max_y, s_coord, e_coord

    def construct_path_sequence( char_yx_grid, max_x, max_y, s_coord, e_coord ):
        path_sequence = [s_coord]
        while path_sequence[-1] != e_coord:
            x, y = path_sequence[-1]
            for d in coord_delta_by_direction:
                dx, dy = coord_delta_by_direction[d]
                new_x = x + dx
                new_y = y + dy
                if char_yx_grid[new_y][new_x] != wall_char:
                    new_coord = (new_x, new_y)
                    if not new_coord in path_sequence:
                        path_sequence.append( new_coord )
                        break

        return path_sequence
    
    def find_all_cheats( char_yx_grid, max_x, max_y ):
        cheats = []
        for y in range(1, max_y ):
            for x in range( 1, max_x ):
                if char_yx_grid[y][x] == wall_char:
                    for d in [0,1]:
                        dx, dy = coord_delta_by_direction[d]
                        new_x1 = x-dx
                        new_x2 = x+dx
                        new_y1 = y-dy
                        new_y2 = y+dy
                        if char_yx_grid[new_y1][new_x1] != wall_char:
                            if char_yx_grid[new_y2][new_x2] != wall_char:
                                cheats.append( ((new_x1, new_y1), (new_x2, new_y2)) )
        
        return cheats
    
    def assess_cheats( path_sequence, cheats, min_time_saved_by_cheats ):
        num_cheats_by_picoseconds_saved = {}

        for cheat in cheats:
            coord1, coord2 = cheat
            p1 = path_sequence.index( coord1 )
            p2 = path_sequence.index( coord2 )
            delta_p = abs(p1-p2) -2
            if not delta_p in num_cheats_by_picoseconds_saved:
                num_cheats_by_picoseconds_saved[delta_p] = 0
            
            num_cheats_by_picoseconds_saved[delta_p] += 1

        delta_ps = list(num_cheats_by_picoseconds_saved.keys())
        delta_ps.sort()

        total_num_cheats_saving_more_than_min_time = 0
        sorted_num_cheats_by_picoseconds_saved = {}
        for delta_p in delta_ps:
            num_cheats = num_cheats_by_picoseconds_saved[delta_p]
            sorted_num_cheats_by_picoseconds_saved[delta_p] = num_cheats
            if delta_p >= min_time_saved_by_cheats:
                total_num_cheats_saving_more_than_min_time += num_cheats

        return sorted_num_cheats_by_picoseconds_saved, total_num_cheats_saving_more_than_min_time

    # construct sequence of coords for initial path from s to e
    # construct list of all possible cheats: all ".#." horiz and vert
    ## convert each cheat into a start/end coord pair (from "." to ".")
    # lookup each cheat in the main sequence and calc the time saved

    char_yx_grid, max_x, max_y, s_coord, e_coord = parse_input( instance['input'] )
    # print( f"DEBUG: max_x={max_x}, max_y={max_y}, s_coord={s_coord}, e_coord={e_coord}")

    path_sequence = construct_path_sequence( char_yx_grid, max_x, max_y, s_coord, e_coord )
    cheats = find_all_cheats( char_yx_grid, max_x, max_y )

    # print( f"DEBUG: path_sequence={path_sequence}\ncheats={cheats}")

    num_cheats_by_picoseconds_saved, total_num_cheats_saving_more_than_min_time = assess_cheats( path_sequence, cheats, min_time_saved_by_cheats )

    return {
        'num_cheats_by_picoseconds_saved': num_cheats_by_picoseconds_saved,
        'total_num_cheats_saving_more_than_min_time': total_num_cheats_saving_more_than_min_time,
    }

def run():
    print_here()
    verbose = True
    response = exercise_fn_with_cases( solve, instances, attrs, verbose )
    if verbose:
        pprint.pp( response )
    else:
        print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2025-01-01: day20/puzzle1/..
# [{'elapsed_time_s': 0.00020808400586247444},
#  {'num_cheats_by_picoseconds_saved': {2: 1003,
#                                       4: 1003,
#                                       6: 300,
#                                       8: 446,
#                                       10: 195,
#                                       12: 326,
#                                       14: 152,
#                                       16: 244,
#                                       18: 121,
#                                       20: 195,
#                                       22: 83,
#                                       24: 156,
#                                       26: 56,
#                                       28: 133,
#                                       30: 63,
#                                       32: 106,
#                                       34: 40,
#                                       36: 83,
#                                       38: 38,
#                                       40: 83,
#                                       42: 34,
#                                       44: 72,
#                                       46: 29,
#                                       48: 65,
#                                       50: 23,
#                                       52: 57,
#                                       54: 25,
#                                       56: 59,
#                                       58: 34,
#                                       60: 52,
#                                       62: 24,
#                                       64: 48,
#                                       66: 19,
#                                       68: 40,
#                                       70: 16,
#                                       72: 41,
#                                       74: 17,
#                                       76: 40,
#                                       78: 12,
#                                       80: 21,
#                                       82: 8,
#                                       84: 24,
#                                       86: 10,
#                                       88: 25,
#                                       90: 12,
#                                       92: 27,
#                                       94: 10,
#                                       96: 27,
#                                       98: 14,
#                                       100: 30,
#                                       102: 13,
#                                       104: 22,
#                                       106: 8,
#                                       108: 19,
#                                       110: 7,
#                                       112: 17,
#                                       114: 9,
#                                       116: 20,
#                                       118: 7,
#                                       120: 11,
#                                       122: 3,
#                                       124: 16,
#                                       126: 9,
#                                       128: 14,
#                                       130: 5,
#                                       132: 16,
#                                       134: 6,
#                                       136: 22,
#                                       138: 12,
#                                       140: 19,
#                                       142: 8,
#                                       144: 21,
#                                       146: 12,
#                                       148: 17,
#                                       150: 6,
#                                       152: 12,
#                                       154: 7,
#                                       156: 13,
#                                       158: 3,
#                                       160: 11,
#                                       162: 7,
#                                       164: 12,
#                                       166: 4,
#                                       168: 12,
#                                       170: 5,
#                                       172: 17,
#                                       174: 7,
#                                       176: 15,
#                                       178: 9,
#                                       180: 13,
#                                       182: 4,
#                                       184: 13,
#                                       186: 1,
#                                       188: 6,
#                                       190: 1,
#                                       192: 7,
#                                       194: 2,
#                                       196: 8,
#                                       198: 3,
#                                       200: 7,
#                                       202: 1,
#                                       204: 4,
#                                       206: 2,
#                                       208: 6,
#                                       210: 2,
#                                       212: 10,
#                                       214: 4,
#                                       216: 13,
#                                       218: 4,
#                                       220: 12,
#                                       222: 5,
#                                       224: 10,
#                                       226: 3,
#                                       228: 8,
#                                       230: 4,
#                                       232: 11,
#                                       234: 8,
#                                       236: 12,
#                                       238: 3,
#                                       240: 10,
#                                       242: 4,
#                                       244: 9,
#                                       246: 4,
#                                       248: 12,
#                                       250: 7,
#                                       252: 10,
#                                       254: 4,
#                                       256: 8,
#                                       258: 3,
#                                       260: 7,
#                                       262: 4,
#                                       264: 9,
#                                       266: 4,
#                                       268: 4,
#                                       270: 2,
#                                       272: 4,
#                                       274: 3,
#                                       276: 7,
#                                       278: 3,
#                                       280: 7,
#                                       282: 3,
#                                       284: 4,
#                                       286: 1,
#                                       288: 4,
#                                       290: 1,
#                                       292: 5,
#                                       294: 4,
#                                       296: 5,
#                                       298: 1,
#                                       300: 8,
#                                       302: 5,
#                                       304: 7,
#                                       306: 2,
#                                       308: 4,
#                                       312: 4,
#                                       314: 3,
#                                       316: 4,
#                                       318: 1,
#                                       320: 6,
#                                       322: 5,
#                                       324: 7,
#                                       326: 2,
#                                       328: 3,
#                                       330: 1,
#                                       332: 3,
#                                       336: 4,
#                                       338: 2,
#                                       340: 5,
#                                       342: 2,
#                                       344: 6,
#                                       346: 1,
#                                       348: 4,
#                                       350: 2,
#                                       352: 7,
#                                       354: 2,
#                                       356: 4,
#                                       360: 3,
#                                       364: 2,
#                                       366: 2,
#                                       368: 4,
#                                       370: 1,
#                                       372: 3,
#                                       376: 1,
#                                       378: 1,
#                                       380: 3,
#                                       382: 1,
#                                       384: 3,
#                                       388: 2,
#                                       392: 3,
#                                       394: 2,
#                                       396: 5,
#                                       398: 1,
#                                       400: 3,
#                                       402: 2,
#                                       404: 5,
#                                       406: 2,
#                                       408: 6,
#                                       410: 3,
#                                       412: 4,
#                                       414: 1,
#                                       416: 3,
#                                       418: 2,
#                                       420: 4,
#                                       422: 1,
#                                       424: 3,
#                                       426: 1,
#                                       428: 1,
#                                       440: 3,
#                                       442: 2,
#                                       444: 4,
#                                       446: 3,
#                                       448: 3,
#                                       450: 1,
#                                       452: 3,
#                                       460: 2,
#                                       464: 1,
#                                       468: 2,
#                                       470: 1,
#                                       472: 3,
#                                       476: 1,
#                                       480: 2,
#                                       482: 1,
#                                       484: 1,
#                                       488: 1,
#                                       490: 1,
#                                       492: 2,
#                                       494: 1,
#                                       496: 1,
#                                       504: 1,
#                                       508: 2,
#                                       532: 1,
#                                       534: 1,
#                                       536: 1,
#                                       560: 1,
#                                       562: 1,
#                                       564: 1,
#                                       566: 1,
#                                       568: 2,
#                                       570: 1,
#                                       572: 2,
#                                       574: 1,
#                                       576: 2,
#                                       580: 1,
#                                       582: 1,
#                                       584: 1,
#                                       608: 1,
#                                       612: 1,
#                                       614: 1,
#                                       616: 1,
#                                       652: 2,
#                                       654: 1,
#                                       656: 1,
#                                       660: 1,
#                                       664: 1,
#                                       668: 1,
#                                       684: 1,
#                                       688: 2,
#                                       690: 2,
#                                       692: 2,
#                                       696: 1,
#                                       708: 1,
#                                       710: 1,
#                                       712: 1,
#                                       720: 2,
#                                       722: 2,
#                                       724: 2,
#                                       726: 1,
#                                       728: 1,
#                                       732: 1,
#                                       736: 1,
#                                       738: 1,
#                                       740: 1,
#                                       742: 1,
#                                       744: 1,
#                                       748: 1,
#                                       750: 1,
#                                       752: 2,
#                                       754: 1,
#                                       756: 3,
#                                       758: 1,
#                                       760: 3,
#                                       762: 1,
#                                       764: 1,
#                                       768: 1,
#                                       770: 1,
#                                       772: 1,
#                                       804: 1,
#                                       806: 1,
#                                       808: 1,
#                                       810: 1,
#                                       812: 2,
#                                       814: 1,
#                                       816: 1,
#                                       818: 1,
#                                       820: 1,
#                                       822: 1,
#                                       824: 1,
#                                       860: 1,
#                                       862: 1,
#                                       864: 1,
#                                       868: 1,
#                                       872: 1,
#                                       876: 2,
#                                       878: 2,
#                                       880: 2,
#                                       904: 1,
#                                       906: 1,
#                                       908: 1,
#                                       912: 1,
#                                       914: 1,
#                                       916: 1,
#                                       924: 1,
#                                       928: 1,
#                                       930: 1,
#                                       932: 2,
#                                       934: 1,
#                                       936: 3,
#                                       940: 1,
#                                       960: 2,
#                                       964: 1,
#                                       966: 1,
#                                       968: 1,
#                                       984: 1,
#                                       986: 1,
#                                       988: 1,
#                                       992: 1,
#                                       996: 1,
#                                       1020: 1,
#                                       1032: 1,
#                                       1034: 1,
#                                       1036: 1,
#                                       1038: 1,
#                                       1040: 1,
#                                       1068: 1,
#                                       1070: 1,
#                                       1072: 1,
#                                       1076: 1,
#                                       1080: 1,
#                                       1082: 1,
#                                       1084: 1,
#                                       1100: 1,
#                                       1102: 1,
#                                       1104: 1,
#                                       1120: 1,
#                                       1122: 1,
#                                       1124: 1,
#                                       1280: 1,
#                                       1284: 1,
#                                       1288: 1,
#                                       1290: 1,
#                                       1292: 1,
#                                       1294: 1,
#                                       1296: 1,
#                                       1298: 1,
#                                       1300: 1,
#                                       1302: 1,
#                                       1304: 1,
#                                       1344: 1,
#                                       1346: 1,
#                                       1348: 1,
#                                       1364: 1,
#                                       1366: 1,
#                                       1368: 1,
#                                       1380: 1,
#                                       1400: 1,
#                                       1402: 1,
#                                       1404: 1,
#                                       1408: 1,
#                                       1410: 1,
#                                       1412: 1,
#                                       1416: 1,
#                                       1420: 1,
#                                       1424: 1,
#                                       1426: 1,
#                                       1428: 1,
#                                       1430: 1,
#                                       1432: 1,
#                                       1434: 1,
#                                       1436: 1,
#                                       1448: 1,
#                                       1480: 1,
#                                       1482: 1,
#                                       1484: 1,
#                                       1588: 1,
#                                       1590: 1,
#                                       1592: 1,
#                                       1608: 1,
#                                       1610: 1,
#                                       1612: 1,
#                                       1636: 1,
#                                       1638: 1,
#                                       1640: 1,
#                                       1792: 1,
#                                       1796: 1,
#                                       1808: 1,
#                                       1812: 1,
#                                       1814: 1,
#                                       1816: 1,
#                                       1820: 1,
#                                       1824: 2,
#                                       1844: 1,
#                                       1846: 1,
#                                       1848: 1,
#                                       1868: 1,
#                                       1870: 1,
#                                       1872: 1,
#                                       1896: 1,
#                                       1904: 1,
#                                       1906: 1,
#                                       1908: 1,
#                                       1944: 1,
#                                       1948: 1,
#                                       1952: 1,
#                                       1954: 1,
#                                       1956: 1,
#                                       1960: 1,
#                                       1962: 1,
#                                       1964: 1,
#                                       2012: 1,
#                                       2014: 1,
#                                       2016: 1,
#                                       2024: 1,
#                                       2436: 1,
#                                       2452: 1,
#                                       2454: 1,
#                                       2456: 1,
#                                       2460: 1,
#                                       2462: 1,
#                                       2464: 1,
#                                       2500: 1,
#                                       2502: 1,
#                                       2504: 1,
#                                       2584: 1,
#                                       2588: 1,
#                                       2590: 1,
#                                       2592: 1,
#                                       2596: 1,
#                                       2598: 1,
#                                       2600: 1,
#                                       2602: 1,
#                                       2604: 1,
#                                       3992: 1,
#                                       3996: 1,
#                                       3998: 1,
#                                       4000: 1,
#                                       4028: 1,
#                                       4048: 1,
#                                       4056: 1,
#                                       4058: 1,
#                                       4060: 1,
#                                       4062: 1,
#                                       4064: 1,
#                                       4066: 1,
#                                       4068: 1,
#                                       4084: 1,
#                                       4088: 1,
#                                       4432: 1,
#                                       4434: 1,
#                                       4436: 1,
#                                       8848: 1,
#                                       8852: 1,
#                                       8854: 1,
#                                       8856: 1,
#                                       8860: 1,
#                                       8862: 1,
#                                       8864: 1,
#                                       8876: 1,
#                                       8920: 1,
#                                       8922: 1,
#                                       8924: 1,
#                                       9188: 1,
#                                       9204: 1,
#                                       9216: 1,
#                                       9218: 1,
#                                       9220: 1,
#                                       9224: 1,
#                                       9236: 1,
#                                       9238: 1,
#                                       9240: 1,
#                                       9248: 1,
#                                       9250: 1,
#                                       9252: 1,
#                                       9260: 1,
#                                       9276: 1,
#                                       9278: 1,
#                                       9280: 1},
#   'total_num_cheats_saving_more_than_min_time': 1327,
#   'elapsed_time_s': 1.631898958934471}]