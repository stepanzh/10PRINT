#!/usr/bin/env python3

from lib.tenprint import Maze
from lib.color import ANSIColors
from lib.screen import Screen

import time, sys, random


class ColoredMazeComponents(Maze):
    colors = None
    color_matrix = None

    def __init__(self, size, seed=1, colors=[ANSIColors.white]):
        super().__init__(size, seed=seed)
        
        self.colors = colors
        self._init_color_matrix()

    def _init_color_matrix(self):
        self.color_matrix = self.fill_matrix(None)
        for i in range(self.size.height):
            for j in range(self.size.width):
                self.color_matrix[i][j] = self.colors[self._vertex_belong[i][j] % len(self.colors)]

def translate(ij, didj):
    return (ij[0] + didj[0], ij[1] + didj[1])

def display_column(maze, scr, j, trans=(0, 0)):
    for i in range(maze.size.height):
        color = maze.color_matrix[i][j]
        scr.write_ansi_markup(color, at=translate((i, j), trans))
        scr.write_char(maze.maze[i][j], at=translate((i, j), trans))

def hide_column(maze, scr, j, trans=(0, 0)):
    for i in range(maze.size.height):
        scr.write_ansi_markup(ANSIColors.from_code(237), at=(i, j))
        scr.write_char(maze.maze[i][j], at=translate((i, j), trans))

def pause(sec):
    sys.stdout.flush()
    time.sleep(sec)

def anim_intro(maze, scr, thick, dt, trans):
    for j in range(thick):
        display_column(maze, scr, j, trans=trans)
        pause(dt)

def anim_outro(maze, scr, thick, dt, trans):
    for j in range(maze.size.width-thick, maze.size.width):
        hide_column(maze, scr, j, trans=trans)
        pause(dt)

def anim_go_right(maze, scr, thick, dt, trans):
    for j in range(thick, maze.size.width):
        display_column(maze, scr, j, trans=trans)
        hide_column(maze, scr, j - thick, trans=trans)
        pause(dt)

def anim_go_left(maze, scr, thick, dt, trans):
    for j in range(maze.size.width-thick-1, -1, -1):
        display_column(maze, scr, j, trans=trans)
        hide_column(maze, scr, j + thick, trans=trans)
        pause(dt)

def bounce(maze, scr, thick, dt, trans, times=1):
    t = 0
    while t <= times:
        if t % 2 == 1:
            anim_go_left(maze, scr, thick, dt, trans)
        else:
            anim_go_right(maze, scr, thick, dt, trans)
        t += 1
        pause(dt)


def colored_components(maze_size=(80, 28), seed=None):
    random.seed(seed)
    
    colors = ANSIColors.blues + ANSIColors.pinks
    random.shuffle(colors)

    maze = ColoredMazeComponents(size=maze_size, seed=seed, colors=colors) 

    margintop = (40 - maze_size[1]) // 2 - 2
    marginleft = (100 - maze_size[0]) // 2
    margin = (margintop, marginleft)

    scr = Screen(width=maze.size.width + 2*marginleft, height=maze.size.height + 2*margintop)

    for j in range(maze.size.width):
        hide_column(maze, scr, j, trans=margin)

    pause(1)

    thick = 3
    dt = 0.03

    for t in range(3):
        thick = min(10 + 5*t**2, maze.size.width)
        anim_intro(maze, scr, thick, dt, margin)
        anim_go_right(maze, scr, thick, dt, margin)
        anim_outro(maze, scr, thick, dt, margin)
        dt *= 0.8

    anim_intro(maze, scr, 80, 0.03, margin)

    scr.cursor_move_outside()
    scr.write_ansi_markup(ANSIColors.reset)
    pause(1)

colored_components(seed=0)
