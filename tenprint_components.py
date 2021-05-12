#!/usr/bin/env python3

from lib.tenprint import Maze
from lib.color import ANSIColors

import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", type=int, default=0, help="seed for the maze")
    args = parser.parse_args()
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
