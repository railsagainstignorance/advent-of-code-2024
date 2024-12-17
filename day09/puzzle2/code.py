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
        'initial_blocks_str': '00...111...2...333.44.5555.6666.777.888899',
        'compacted_blocks_str': '00992111777.44.333....5555.6666.....8888..',
        'compacted_filesystem_checksum': 2858,
    },
    {
        'input': "../puzzle1/input.txt"
    }
]

attrs = [
    'num_files',
    'blocks_str',
    'filesystem_checksum',
    'initial_blocks_str',
    'compacted_blocks_str',
    'compacted_filesystem_checksum',
    ]

def solve( case ):

    int_yx_array = get_int_yx_array_from_input( case['input'] ) 
    disk_map = int_yx_array[0]
    num_files = int((len(disk_map) +1) / 2)
    space_file_id = -1

    def calc_checksum_from_blocks( blocks ):
        filesystem_checksum = 0
        for i in range(0, len(blocks) ):
            if blocks[i] == space_file_id:
                continue
            filesystem_checksum += blocks[i] * i
        return filesystem_checksum

    def calc_filesystem_checksum( disk_map ):
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

        filesystem_checksum = calc_checksum_from_blocks( blocks )

        return filesystem_checksum, blocks_str

    def calc_compacted_filesystem_checksum( disk_map ):
        spans = [] # [ [file_id or space_file_id, length], ]
        for i, num in enumerate(disk_map):
            if i % 2 == 0: # is a file
                file_id = int(i / 2)
                spans.append([file_id, num])
            else: # is a space
                spans.append([space_file_id, num])

        def construct_blocks_from_spans( spans ):
            blocks = []
            for span in spans:
                for i in range(0, span[1]):
                    if span[0] == space_file_id:
                        blocks.append(space_file_id)
                    else:
                        blocks.append(span[0])
            return blocks

        def construct_blocks_str_from_blocks( blocks ):
            # construct string visualisation of blocks, with '.' for space_file_id
            blocks_str = ''.join([str(x) if x != space_file_id else '.' for x in blocks])
            return blocks_str

        initial_blocks_str = construct_blocks_str_from_blocks(construct_blocks_from_spans(spans))  

        file_spans  = [span for span in spans if span[0] != space_file_id]

        # 00...111...2...333.44.5555.6666.777.888899
        # 0099.111...2...333.44.5555.6666.777.8888..

        for file_span in reversed(file_spans):
            for s, span in enumerate(spans):
                if span[0] == file_span[0]:
                    break
                if span[0] == space_file_id and span[1] >= file_span[1]:
                    # found big enough space

                    # shrink space remaining
                    span[1] = span[1] - file_span[1]

                    # clone file, insert before space
                    new_file_span = [file_span[0], file_span[1]]
                    spans.insert(s, new_file_span)
                    
                    # convert original file to space   
                    file_span[0] = space_file_id
                    break

        blocks = construct_blocks_from_spans(spans)
        num_blocks = len(blocks)
        blocks_str = construct_blocks_str_from_blocks(blocks)

        filesystem_checksum = calc_checksum_from_blocks( blocks )
        # print( blocks )
        # print( blocks_str )
        # print( filesystem_checksum )

        return initial_blocks_str, filesystem_checksum, blocks_str

    filesystem_checksum, blocks_str = calc_filesystem_checksum( disk_map )
    initial_blocks_str, compacted_filesystem_checksum, compacted_blocks_str = calc_compacted_filesystem_checksum( disk_map )

    return {
        'num_files': num_files,
        'blocks_str': blocks_str,
        'filesystem_checksum': filesystem_checksum,
        'initial_blocks_str': initial_blocks_str,
        'compacted_blocks_str': compacted_blocks_str,
        'compacted_filesystem_checksum': compacted_filesystem_checksum,
    }

def run():
    print_here()
    verbose = False
    response = exercise_fn_with_cases( solve, cases, attrs, verbose )
    print( response )

if __name__ == "__main__":
    run()

# AOC 2024: 2024-12-17: day09/puzzle2/..
# [{'compacted_filesystem_checksum': 6363268339304, 'elapsed_time_s': 3.759934375062585}]