#!/usr/bin/env python3


import sys
from lib.color import ANSIColors


for i in range(16):
    for j in range(16):
        code = i * 16 + j
        sys.stdout.write(ANSIColors.from_code(code) + str(code).ljust(4))
    print(ANSIColors.reset)
