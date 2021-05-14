import lib.config as config
import logging


class MazePattern(object):
    "Describes connectivity pattern of maze."
    
    def __init__(self,
        chars=config.DEFAULT_MAZE_CHARS,
        fill=config.DEFAULT_MAZE_CONNECTIVITY_PATTERN_FILL,
        pattern=config.DEFAULT_MAZE_CONNECTIVITY_PATTERN):

        if fill in chars: logging.warning('Fill character matches maze character.')

        self._chars = chars
        self._fill = fill
        self._pattern = pattern

    def __str__(self):
        return '{}(chars={}, fill=\'{}\', pattern=\'{}\')'.format(
            type(self).__name__,
            self._chars,
            self._fill,
            self._pattern
        )

    def adjacent(self, window, is_matrix=False):
        """
        Calculates connected positions relative to center of `window`.
        `window` must be 3x3 matrix-like object of chars or string of 9 characters (row-major).
        This behaviour defined by `is_matrix`.

        Tip: for outside cells of global maze fill `window` with `self.fill()` character.
        """
        if is_matrix:
            window = self._join_matrix_to_str(window)

        adj = []
        pattern = self._pattern[ self._chars.index(window[4]) ]

        for n, char in enumerate(window):
            if n == 4 or window[n] == self._fill:  # skipping center and fill chars
                continue
            if window[n] == pattern[n]:
                di, dj = n // 3 - 1, n % 3 - 1  # relative position to center (1, 1)
                adj.append((di, dj))
        return adj

    @classmethod
    def _join_matrix_to_str(cls, matrix):
        s = ''.join(''.join(row) for row in matrix)
        return s

    def chars(self):
        return self._chars

    def fill(self):
        return self._fill
