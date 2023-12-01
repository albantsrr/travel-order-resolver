# generation.py
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Confidential file
# Copyright (C) Epitech - All rights reserved
# -----------------------------------------------------------------------------
#
#  
#
# -----------------------------------------------------------------------------
# History
# 03/10/2023 N. Laurens : creation
# 16/10/2023 N. Laurens : add --p option (proportion of town names)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------
from src.classFile import *

import random
import time
import csv
import os
import argparse


if __name__ == "__main__":
    generation = cGenerateSentence()
    generation.generate_by_number(2000)
