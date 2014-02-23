# -*- coding: utf-8 -*-

import sys


def _log(*args):
    print(*args, file=sys.stderr)
