#!/usr/bin/env python3

from lib.tenprint import Maze
from lib.mazepattern import MazePattern
from lib.color import ANSIColors, Palette

import lib.config as config

import argparse


DEFAULT_CHARS = ''.join(config.DEFAULT_MAZE_CHARS)
DEFAULT_FILL = config.DEFAULT_MAZE_CONNECTIVITY_PATTERN_FILL
DEFAULT_PATTERN = ''.join(config.DEFAULT_MAZE_CONNECTIVITY_PATTERN)
DEFAULT_SIZE = ','.join(map(str, config.DEFAULT_MAZE_SIZE))
DEFAULT_COLORS = ','.join(map(str, [4, 6, 12, 17, 21, 26, 27, 32, 81]))


def parse_args():
    parser = argparse.ArgumentParser(
        description='10PRINT maze generator with colored connectivity components.'
    )
    parser.add_argument("-s", "--seed", default=None,
        help="Seed for maze (int). Default is python's None, so maze shall be random."
    )
    parser.add_argument('-S', '--size', type=str, default=DEFAULT_SIZE,
        help='Size of the maze in characters. Format is \'width,height\'. Default is \'{}\''.format(DEFAULT_SIZE)
    )

    parser.add_argument('-c', '--chars', type=str, default=DEFAULT_CHARS,
        help='Two characters which maze consists of.'
    )
    parser.add_argument('-f', '--fill', type=str, default=DEFAULT_FILL,
        help='Fill character of connectivity pattern. Default is \'{}\'.'.format(DEFAULT_FILL)
    )
    parser.add_argument('-p', '--pattern', type=str, default=DEFAULT_PATTERN,
        help='Connectivity pattern (string of 18 characters). Default is \'{}\'.'.format(DEFAULT_PATTERN)
    )

    parser.add_argument('-C', '--colors', type=str, default=DEFAULT_COLORS,
        help='Color set for components. Format is \'c1,c2,c3,...\' where ci is int (0..255) representing ansi color code. Run ansi_pallette.py for full list of codes.'
    )

    args = parser.parse_args()

    if args.seed is not None:
        args.seed = int(args.seed)

    args.size = tuple(map(int, args.size.split(',')))
    if len(args.size) != 2:
        raise ValueError('Specified `size` is not two comma separated integers.')
    
    assert len(args.chars) == 2, '--chars must be two-character string.'
    args.chars = tuple(args.chars)

    assert len(args.fill) == 1, '--fill must be one-character string.'

    assert len(args.pattern) == 18, '--pattern must be 18-character string.'
    args.pattern = (args.pattern[:9], args.pattern[9:])

    args.colors = list(map(int, args.colors.split(',')))

    return args


def scene_colored_components(maze_size, pattern=None, seed=None, colors=None):
    # terminal window size 100 x 40

    "window height, top margin equal bottom margin and 2 lines for prompt string"
    margintop = (40 - maze_size[1]) // 2 - 2
    marginleft = (100 - maze_size[0]) // 2

    maze = Maze(size=maze_size, seed=seed, pattern=pattern)
    vertex_belong = maze.vertex_belong()
    colors = Palette(colors)
    
    print(margintop * '\n', end='')
    for i in range(maze.size.height):
        print(marginleft * ' ', end='')
        for j in range(maze.size.width):
            color = colors[vertex_belong[i][j] % len(colors)]
            print(color + maze.maze[i][j], end='')
        print(ANSIColors.reset)
    print(margintop * '\n', end='')


if __name__ == '__main__':
    args = parse_args()
    mp = MazePattern(
        chars=args.chars,
        fill=args.fill,
        pattern=args.pattern
    )
    scene_colored_components(maze_size=args.size, seed=args.seed, pattern=mp, colors=args.colors)
