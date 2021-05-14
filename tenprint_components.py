#!/usr/bin/env python3

from lib.tenprint import Maze
from lib.mazepattern import MazePattern
from lib.color import ANSIColors

import lib.config as config

import argparse


DEFAULT_CHARS = ''.join(config.DEFAULT_MAZE_CHARS)
DEFAULT_FILL = config.DEFAULT_MAZE_CONNECTIVITY_PATTERN_FILL
DEFAULT_PATTERN = ''.join(config.DEFAULT_MAZE_CONNECTIVITY_PATTERN)


def parse_args():
    parser = argparse.ArgumentParser(
        description='10PRINT maze generator with colored connectivity components.'
    )
    parser.add_argument("-s", "--seed", default=None,
        help="Seed for maze (int). Default is python's None, so maze shall be random."
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

    args = parser.parse_args()

    if args.seed is not None:
        args.seed = int(args.seed)

    return args


def scene_colored_components(maze_size=(80, 28), seed=None):
    # terminal window size 100 x 40

    "window height, top margin equal bottom margin and 2 lines for prompt string"
    margintop = (40 - maze_size[1]) // 2 - 2
    marginleft = (100 - maze_size[0]) // 2

    maze = Maze(size=maze_size, seed=seed)
    vertex_belong = maze.vertex_belong()
    colors = ANSIColors.reds + ANSIColors.yellows
    
    print(margintop * '\n', end='')
    for i in range(maze_size[1]):
        print(marginleft * ' ', end='')
        for j in range(maze_size[0]):
            color = colors[vertex_belong[i][j] % len(colors)]
            print(color + maze.maze[i][j], end='')
        print(ANSIColors.reset)
    print(margintop * '\n', end='')


if __name__ == '__main__':
    args = parse_args()
    scene_colored_components(maze_size=(80, 28), seed=args.seed)
