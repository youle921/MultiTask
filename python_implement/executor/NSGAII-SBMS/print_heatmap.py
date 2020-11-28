# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:03:23 2020

@author: t.urita
"""

import pathlib
import pandas as pd

path = pathlib.Path(".")
csvs = path.glob("**/*.csv")

out = [*map(lambda x: pd.read_csv(x, header = None)[0][0], csvs)]