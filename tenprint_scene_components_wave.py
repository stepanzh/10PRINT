#!/usr/bin/env python3

from collections import deque
import time, sys

from lib.tenprint import Maze
from lib.color import ANSIColors
from lib.screen import Screen


def write_char_colored(scr, char, at:tuple, color:str):
    scr.write_ansi_markup(color, at)
    scr.write_char(char, at)
    scr.write_ansi_markup(ANSIColors.reset, at)

def highlight(scr:Screen, maze, whom, color=ANSIColors.red):
    for i, j in whom:
        write_char_colored(scr, maze.maze[i][j], (i, j), color)

def neighbours_sequence_dfs(maze, u, p=-1, sequence=None, visited=None):
    visited = maze.fill_matrix(False) if visited is None else visited
    sequence = [] if sequence is None else sequence

    ui, uj = u
    visited[ui][uj] = True
    sequence.append(u)
    for v in maze.neighbours(u):
        vi, vj = v
        if not visited[vi][vj]:
            neighbours_sequence_dfs(maze, v, u, sequence, visited)
    return sequence


def neighbours_sequence_wave(maze:Maze, start:tuple):
    q = deque([start])
    visited = maze.fill_matrix(False)
    sequence = [{start}]
    while q:
        u = q.pop()
        neighbours = set()
        for i, j in maze.neighbours(u):
            if not visited[i][j]:
                visited[i][j] = True
                q.appendleft((i, j))
                neighbours.add((i, j))
        if neighbours:
            sequence.append(neighbours)
    return sequence

def scene(maze_size=(80, 28), seed=None):
    maze = Maze(size=maze_size, seed=seed)
    scr = Screen(*maze.size)
    
    components = sorted(maze.components(), key=len, reverse=True)

    colors = ANSIColors.blues + ANSIColors.pinks

    for (icomp, comp) in enumerate(components):
        start = comp.pop()
        comp.add(start)

        color = colors[icomp % len(colors)]
        sequence_wave = neighbours_sequence_wave(maze, start)
        for packet in sequence_wave:
            highlight(scr, maze, packet, color=color)
            sys.stdout.flush()
            time.sleep(3e-3)

    scr.cursor_move_outside()


if __name__ == "__main__":
    scene((80, 28), seed=1)
