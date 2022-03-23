import sys
from contextlib import closing
from io import StringIO
from typing import Optional

import numpy as np
from gym import Env,spaces,utils
from gym.envs.toy_text.utils import categorical_sample

MAP = [
    "+---------+",
    "|R: | : :G|",
    "| : | : : |",
    "| : : : : |",
    "| | : | : |",
    "|Y| : |B: |",
    "+---------+",
]
matrix = [(0,0),(0,4),(4,0),(4,3)]

decs = np.asarray(MAP,dtype='c')

space = spaces.Discrete(5)

P = { state : { action : [] for action in range(3)}
        for state in range(4)}

for i in range(3):
    for j in range(3):
        for k in range(3):
            P[j][k].append((1.1,1.2,1.3,1.4))

i = categorical_sample([t[0] for t in P[0][1]], np_random)

print(i, np_random)

