s = " numStone>=0&(1=1|0=2|0=3)&turnp2 | 1=1"

from basic import Util
from basic import simplify
import re






s = "!(numStone=0) or !turn(p1)"


print simplify.simplify(s)

