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
DEFAULT_MARGIN = ','.join(map(str, [0, 0]))
DEFAULT_COLORS = ','.join(map(str, [4, 6, 12, 218, 21, 26, 27, 127, 81, 225]))

CLI_EPILOG = '''{bold}Maze pattern manual (-c, -f, -p options).{reset}
  
 Maze characters: -c option.
  Maze consists of set of two characters. They are defined by -c option.
  For example, if you want a maze from circles '●' and spaces ' ' you should specify -c '● '.
  Tip: to avoid conflicts with terminal characters, use '=' argument formatting -c='● '.

 Fill character: -f option.
  Fill character is supplementary character for defining connectivity pattern.
  You must specify it when default fill character '{fill}' is one of your maze character.
  You may specify it when default fill character '{fill}' is not suitable for defining connectivity pattern.

 Connectivity pattern: -p option.
  This option defines adjacent cells of maze.
  As maze is two-dimensional, each character is supposed to be connected with at most 8 characters.
  To specify which character connects to which, following matrices are used.
  For example, in standard 10PRINT '\\' and '/' were used, and the connectivity matrices are
    for '\\': \\/{fill}      for '/': {fill}\\/
             /\\/               \\/\\
             {fill}/\\               /\\{fill}
    Center of matrix is character which connectivity behavior you want to define.
    This center is surrounded by
      a. Maze characters which center relatively connects to;
      b. Fill characters. They are used to define absence of connection with any of characters.
  To define connectivity pattern, do the following
    1. Concatenate rows of matrix for first maze character:    '\\/{fill}/\\/{fill}/\\'         ;
    2. Concatenate rows of matrix for second maze character:            '{fill}\\/\\/\\/\\{fill}';
    3. Concatenate string from step 1 with string from step 2: '\\/{fill}/\\/{fill}/\\{fill}\\/\\/\\/\\{fill}'.

  So, the following command generates colored 10PRINT maze consists of '\\/' with original connectivity pattern
    ./tenprint_components.py -c '\\/' -p '\\/{fill}/\\/{fill}/\\{fill}\\/\\/\\/\\{fill}'
'''.format(bold='\u001b[1m', underline='\u001b[4m', reset=ANSIColors.reset, fill=DEFAULT_FILL)

def parse_args():
    parser = argparse.ArgumentParser(
        description='10PRINT maze generator with colored connectivity components.',
        epilog=CLI_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-s", "--seed", default=None,         # default is None for random.seed()
        help='Seed for maze (int). Default is random maze.'
    )
    parser.add_argument('-S', '--size', type=str, default=DEFAULT_SIZE,
        help='Size of maze in characters. Format is \'width,height\'. Default is \'{}\''.format(DEFAULT_SIZE)
    )
    parser.add_argument('-M', '--margin', type=str, default=DEFAULT_MARGIN,
        help='Top (=bottom) and left margin in characters for maze printing. Format is \'top_margin,left_margin\'.'
    )

    parser.add_argument('-c', '--chars', type=str, default=DEFAULT_CHARS,
        help='Two characters which maze consists of. Default is \'{}\''.format(DEFAULT_CHARS)
    )
    parser.add_argument('-f', '--fill', type=str, default=DEFAULT_FILL,
        help='Fill character of connectivity pattern. Default is \'{}\'.'.format(DEFAULT_FILL)
    )
    parser.add_argument('-p', '--pattern', type=str, default=DEFAULT_PATTERN,
        help='Connectivity pattern (string of 18 characters). Default is \'{}\'.'.format(DEFAULT_PATTERN)
    )

    parser.add_argument('-C', '--colors', type=str, default=DEFAULT_COLORS,
        help='Color set for components. Format is \'c1,c2,c3,...\' where ci is int (0..255) representing ansi color code. Run ansi_pallette.py for full list of codes. Default is \'{}\'.'.format(DEFAULT_COLORS)
    )

    args = parser.parse_args()

    if args.seed is not None:
        args.seed = int(args.seed)

    args.size = tuple(map(int, args.size.split(',')))
    if len(args.size) != 2:
        raise ValueError('Specified `size` is not two comma separated integers.')

    args.margin = tuple(map(int, args.margin.split(',')))
    if len(args.margin) != 2:
        raise ValueError('Specified `margin` is not two comma separated integers.')


    assert len(args.chars) == 2, '--chars must be two-character string.'
    args.chars = tuple(args.chars)

    assert len(args.fill) == 1, '--fill must be one-character string.'

    assert len(args.pattern) == 18, '--pattern must be 18-character string.'
    args.pattern = (args.pattern[:9], args.pattern[9:])

    args.colors = list(map(int, args.colors.split(',')))

    return args


def scene_colored_components(maze_size, pattern=None, seed=None, colors=None, margin=None):
    margintop, marginleft = margin

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
    scene_colored_components(maze_size=args.size, seed=args.seed, pattern=mp, colors=args.colors, margin=args.margin)
