def ansi_from_code(code:int):
    return "\u001b[38;5;" + str(code) + "m"

class ANSIColors:
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    reset = '\u001b[0m'

    palette8set = [black, red, green, yellow, blue, magenta, cyan, white]

    pinks = list(map(ansi_from_code,
        [5, 13, 162, 163, 168, 198, 199, 204, 205, 218, 219]
    ))
    blues = list(map(ansi_from_code,
        [4, 6, 12, 17, 18, 19, 20, 21, 26, 27, 32, 33, 38, 39, 44, 45, 80, 81]
    ))
    yellows = list(map(ansi_from_code, 
        [3, 11, 148, 154, 166, 172, 178, 184, 190, 208, 214, 220, 226, 227]
    ))
    reds = list(map(ansi_from_code,
        [1, 9, 52, 88, 124, 160, 196]
    ))

    @staticmethod
    def from_code(code:int):
        return ansi_from_code(code)

    @staticmethod
    def all():
        return list(map(ansi_from_code, range(256)))


class Palette(object):
    _palette = None

    def __init__(self, palette):
        """
        `palette` is finite iterable of ansi-escape sequences (str) or codes of 256 pallete (int)
        """
        self._init_palette(palette)  # self._palette

    def _init_palette(self, sequence):
        if type(sequence[0]) is str:
            self._palette = tuple(sequence)
        else:
            self._palette = tuple(map(ansi_from_code, sequence))
    
    def __getitem__(self, key):
        return self._palette[key]

    def __len__(self):
        return len(self._palette)

    def sequential(self):
        "Returns palette."
        return self._palette
