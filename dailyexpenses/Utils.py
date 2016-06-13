# -*- coding: utf-8 -*-

import sys


def _log(*args):
    print('log:', *args, file=sys.stderr)
