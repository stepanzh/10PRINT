import random
from collections import deque
from lib.utils import Size
import lib.config as config

DEFAULT_SEED = config.DEFAULT_MAZE_SEED
DEFAULT_CHARS = config.DEFAULT_MAZE_CHARS


class Maze(object):
    size:Size = None
    maze = None
    _components = None
    chars = DEFAULT_CHARS
    _vertex_belong = None
    _neighbours = None

    def __init__(self, size, seed=DEFAULT_SEED, chars=DEFAULT_CHARS):
        "Creates `Maze` object from `size = (width, height)`, `seed` for `random.seed`, and pair of `chars`."

        self.size = Size(width=size[0], height=size[1])
        self.maze = Maze.generate(size, seed)
        
        self._calc_neighbours()     # self._neighbours
        self._calc_components()     # self._components
        self._calc_vertex_belong()  # self._vertex_belong
        
        self.chars = tuple(chars)

    @classmethod
    def generate(cls, size, seed=DEFAULT_SEED, chars=DEFAULT_CHARS):
        "Returns matrix of `size[0] x size[1]` with `chars`. Sets globally `seed`."
        random.seed(seed)
        maze = tuple( tuple( chars[int(0.5 + random.random())] for _ in range(size[0]) ) for _ in range(size[1]))
        return maze

    def _calc_neighbours(self):
        "Returns list of neighbours (i^, j^) vertex `v = (i, j)` for maze of chars '╱╲'."
        
        self._neighbours = self.fill_matrix()
        
        maze = self.maze
        w, h = self.size.width, self.size.height

        for i in range(h):
            for j in range(w):
                neigh = set()
                for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    ii, jj = i + di, j + dj
                    if 0 <= ii < h and 0 <= jj < w and maze[ii][jj] != maze[i][j]:
                        neigh.add((ii, jj))
                if maze[i][j] == self.chars[0]:  # /
                    for di, dj in ((-1, 1),  (1, -1)):  # di + dj == 0
                        ii, jj = i + di, j + dj
                        if 0 <= ii < h and 0 <= jj < w and maze[ii][jj] == maze[i][j]:
                            neigh.add((ii, jj))
                if maze[i][j] == self.chars[1]:  # \
                    for di, dj in ((-1, -1), (1, 1)):
                        ii, jj = i + di, j + dj
                        if 0 <= ii < h and 0 <= jj < w and maze[ii][jj] == maze[i][j]:
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
