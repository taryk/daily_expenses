#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from dailyexpenses import DailyExpenses

if __name__ == '__main__':
    sys.exit(DailyExpenses(sys.argv).run())
