

import re
from basic import Util

encode_pair_logic = (['>=', '<=','=<', '=>'],['@','#','$','~'])



def __to_Pyformula(formula):
	formula =Util.endecode_string(formula, encode_pair_logic[0], encode_pair_logic[1])
	formula = formula.replace('=','==')
	return formula



#print __to_Pyformula(">= # =ehel <=")






conjunctA = (['X3'], ['Int'], ['X3>2'])
conjunctB = (['X1','X2'], ['Int','_S1'], ['X1+X2>1','X1<1'])

#vars_repl_tuple = (['X1'],['X3'])

#print __get_combined_conjunct(conjunctA, conjunctB, vars_repl_tuple)



#from formula import conjunct
import random

#print conjunct.rename((['X3'], ['Int'], ['X3>2']))

#print conjunct.combine_conjunct(conjunctA, conjunctB,3)

#print random.randint(0,0)






