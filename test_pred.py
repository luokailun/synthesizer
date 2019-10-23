


from parser import BATparser
#BATparser.parser('new_chompNN.sc')
#BATparser.parser('new_chomp2N.sc')

'''
BATparser.parser('chompNN.sc')
from formula import Predicate
math_preds, fluent_preds = Predicate.generate_preds('chompNN.sc')

from model import model_interpretor
from basic import Util
from model import util_z3_model
from basic import context_operator

'''

import re

m = "Ch_0_0=True"

fluent_pattern = re.compile(r"(?P<fluent>[\w\d]+?)_(?P<para>[\w\d_]+?)=(?P<value>[\w\d]+)")

print fluent_pattern.findall(m)



