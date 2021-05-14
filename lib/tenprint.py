import random
from collections import deque
from lib.utils import Size
from lib.mazepattern import MazePattern

import lib.config as config

DEFAULT_SEED = config.DEFAULT_MAZE_SEED
DEFAULT_SIZE = config.DEFAULT_MAZE_SIZE
DEFAULT_PATTERN = MazePattern()


class Maze(object):
    size:Size = None
    maze = None
    _components = None
    _vertex_belong = None
    _neighbours = None

    def __init__(self, size=DEFAULT_SIZE, seed=DEFAULT_SEED, pattern=DEFAULT_PATTERN):
        "Creates `Maze` object from `size = (width, height)`, `seed` for `random.seed`, and pair of `chars`."

        self.size = Size(width=size[0], height=size[1])
        self.maze = Maze.generate(size, seed, pattern)
        self._pattern = pattern
        
        self._calc_neighbours()     # self._neighbours
        self._calc_components()     # self._components
        self._calc_vertex_belong()  # self._vertex_belong

    @classmethod
    def generate(cls, size=DEFAULT_SIZE, seed=DEFAULT_SEED, pattern=DEFAULT_PATTERN):
        "Returns matrix of `size[0] x size[1]` with `chars`. Sets globally `seed`."
        random.seed(seed)
        chars = pattern.chars()
        maze = tuple( tuple( chars[int(0.5 + random.random())] for _ in range(size[0]) ) for _ in range(size[1]))
        return maze

    def _calc_neighbours(self):
        """
        self._neighbours:
        Calculates list of neighbours (i^, j^) vertex `v = (i, j)` for maze of chars '╱╲'.
        """
        
        self._neighbours = self.fill_matrix()
        
        maze = self.maze
        w, h = self.size.width, self.size.height

        # ghost_maze is the same maze with additional empty-char boundaries on each side
        ghost_maze = []
        fill = self._pattern.fill()
        ghost_maze.append([fill] * (self.size.width + 2))  # top
        for i in range(h):
            ghost_maze.append(
                [fill] + list(self.maze[i][:]) + [fill]    # inner
            )
        ghost_maze.append([fill] * (self.size.width + 2))  # bottom

        # cycle goes over positions in original maze
        for i in range(h):
            for j in range(w):
                # i_ghost = i + 1, j_ghost = j + 1
                # need to create window from (i-1, j-1) up to (i+1, j+1)
                window = [
                    ghost_maze[i][j:j+3],    # row above: [i-1] -> [i-1+1] = [i]
                    ghost_maze[i+1][j:j+3],  # [j-1:j+2] -> [j-1+1:j+2+1] = [j:j+3]
                    ghost_maze[i+2][j:j+3]
                ]
                adj = self._pattern.adjacent(window, is_matrix=True)
                neigh = set()
                for di, dj in adj:
                    ii, jj = i + di, j + dj
                    if 0 <= ii < h and 0 <= jj < w:
                        neigh.add((ii, jj))
                self._neighbours[i][j] = frozenset(neigh)

    def neighbours(self, v):
        "Returns `set` of neighbours of vertex `v = (i, j).`"
        return self._neighbours[v[0]][v[1]]

    def _component(self, start, visited=None):
        "Returns connectivity component (set) which vertex `start` belongs to."

        # wave algorithm
        q = deque([start])
        maze = self.maze
        visited = self.fill_matrix(False) if visited is None else visited
        component = set()
        component.add(start)
        while q:
            u = q.pop()
            for i, j in self.neighbours(u):
                if not visited[i][j]:
                    visited[i][j] = True
                    q.appendleft((i, j))
                    component.add((i, j))
        return component

    def components(self):
        "Returns connectivity components."
        return [set(comp) for comp in self._components]

    def fill_matrix(self, val=None, size=None):
        """
        Utility function.
        Returns matrix of `size` (width, height) filled with `val`. Default `size` is size of the maze.
        """
        if size is None:
            size = self.size
        w, h = size
        return [[val] * w for _ in range(h)]

    def _calc_components(self):
        "Calculates connectivity components of `self.maze`."
        self._components = []
        visited = self.fill_matrix(False)
        for i in range(self.size.height):
            for j in range(self.size.width):
                if not visited[i][j]:
                    component = self._component((i, j), visited)
                    self._components.append(component)

    def _calc_vertex_belong(self):
        "Returns matrix Aij = c, where c is index of `self._components` list which ij-vertex belongs to."
        self._vertex_belong = self.fill_matrix(0)
        for (i, comp) in enumerate(self._components):
            for ii, jj in comp:
                self._vertex_belong[ii][jj] = i

    def vertex_belong(self):
        "Returns matrix which ij-element equals index of connectivity component which (i, j)-vertex belongs to."
        return [list(row) for row in self._vertex_belong]  # copy
