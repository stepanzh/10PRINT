import sys
from lib.utils import Size


class Screen(object):
    pos:list = None  # i, j position of cursor
    size:Size = None

    def __init__(self, width:int, height:int):
        self._set_size(width, height)
        self._init_screen()

    def _set_size(self, width, height):
        assert width > 0, 'Negative screen width'
        assert height > 0, 'Negative screen height'
        self.size = Size(width=width, height=height)

    def _init_screen(self):
        w, h = self.size.width, self.size.height
        sys.stdout.write(((' ' * w) + '\n')* h)
        self.pos = [h, 0]
        self._cursor_move_up(h)

    def write_char(self, char:str, at=None):
        "Writes single char at position `at`. If `at` is `None`, writes at current cursors' position."

        assert len(char) == 1, '`char` string must be len of 1'
        if at is not None:
            self._cursor_move_to(*at)
        sys.stdout.write(char)
        self._incr_j_pos()

    def write_ansi_markup(self, ansi, at=None):
        """Writes `ansi` escape codes (or sequence of codes).
        (!) Use it only for writing markup codes.
        Any cursor-moving ansi-es would cause inappropiate output.
        """
        if at is not None:
            self._cursor_move_to(*at)
        sys.stdout.write(ansi)

    def _incr_j_pos(self, step=1):
        self.pos[1] += step

    def _cursor_move_up(self, step):
        ci = self.pos[0]
        self.pos[0] = max(0, ci - step)
        sys.stdout.write('\u001b[{}A'.format(ci - self.pos[0]))

    def _cursor_move_down(self, step):
        ci = self.pos[0]
        self.pos[0] = min(self.size.height-1, ci + step)
        sys.stdout.write('\u001b[{}B'.format(self.pos[0] - ci))
    
    def _cursor_move_left(self, step):
        cj = self.pos[1]
        self.pos[1] = max(0, cj - step)
        sys.stdout.write('\u001b[{}D'.format(cj - self.pos[1]))

    def _cursor_move_right(self, step):
        cj = self.pos[1]
        self.pos[1] = min(self.size.width-1, cj + step)
        sys.stdout.write('\u001b[{}C'.format(self.pos[1] - cj))

    def _cursor_move_to(self, i, j):
        ci, cj = self.pos

        if i > ci:
            self._cursor_move_down(i - ci)
        elif i < ci:
            self._cursor_move_up(ci - i)

        if j > cj:
            self._cursor_move_right(j - cj)
        elif j < cj:
            self._cursor_move_left(cj - j)

    def cursor_move(self, i, j):
        "Moves cursor to `i`, `j` 0-based position. The moving is bounded by `size` of `Screen`."
        self._cursor_move_to(i, j)

    def cursor_move_outside(self):
        """Moves cursor just after the `Screen` (start of line with y = `Screen.size.height`.
        Useful for ending."""
        self._cursor_move_to(self.size.height, 0)
        sys.stdout.write('\u001b[{}B'.format(1))


if __name__ == '__main__':
    scr = Screen(width=10, height=20)
    scr.write_ansi_markup('\u001b[38;5;100m', (0, 0))
    scr.write_char('a', (0, 0))
    scr.write_ansi_markup('\u001b[0m', (0, 0))
    scr.write_char('b', (0, 1))
    scr.write_char('c', (2, 3))
    scr.cursor_move_outside()
