#!/usr/bin/env python
import os, sys
from django.core.management import execute_manager

HERE = os.path.dirname(__file__)
sys.path.append(HERE)

import settings

if __name__ == "__main__":
    execute_manager(settings)
