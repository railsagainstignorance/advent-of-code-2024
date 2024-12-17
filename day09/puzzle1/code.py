import sys
sys.path.append('../')
sys.path.append('../../')

import re

from utils import *

cases = [
    {
        'input': '''\
2333133121414131402''',
        'num_files': 10,
        'blocks_str': '0099811188827773336446555566..............',
        'filesystem_checksum': 1928,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'num_files',
    'blocks_str',
    'filesystem_checksum',
    ]

def solve( case ):

    int_yx_array = get_int_yx_array_from_input( case['input'] ) 
    disk_map = int_yx_array[0]
    num_files = int((len(disk_map) +1) / 2)
    space_file_id = -1

    blocks = [] # [file_id, ...]
    for id in range(0, num_files):
        num_file_blocks  = disk_map[id*2]

        for i in range(0, num_file_blocks):
            blocks.append(id)

        if id < num_files-1:        
            num_space_blocks = disk_map[id*2+1]
            for i in range(0, num_space_blocks):
                blocks.append(space_file_id)

    num_blocks = len(blocks)

    liminal_empty_block_ids = [i for i, x in enumerate(blocks) if x == space_file_id]

    # iterate over all blocks, from last to first
    # 0..111....22222

    for i in range(num_blocks-1, -1, -1):
        if len(liminal_empty_block_ids) == 0:
            break
        file_id = blocks[i]
        if file_id == space_file_id:
            liminal_empty_block_ids.pop()
            continue
        left_most_space_block_id = liminal_empty_block_ids.pop(0)
        blocks[i] = space_file_id
        blocks[left_most_space_block_id] = file_id

    # construct string visualisation of blocks, with '.' for space_file_id
    blocks_str = ''.join([str(x) if x != space_file_id else '.' for x in blocks])

    filesystem_checksum = 0
    for i in range(0, num_blocks):
        if blocks[i] == space_file_id:
            break
        filesystem_checksum += blocks[i] * i

    return {
        'num_files': num_files,
        'blocks_str': blocks_str,
        'filesystem_checksum': filesystem_checksum
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-17: day09/puzzle1/..
# [{'filesystem_checksum': 6331212425418, 'elapsed_time_s': 0.09756908298004419}]