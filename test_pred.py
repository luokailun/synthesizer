


from parser import BATparser
BATparser.parser('new_chompNN.sc')
#BATparser.parser('new_chomp2N.sc')


from model import model_interpretor
from basic import Util


M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'True'})

F = "0 > 0 & ! True|1 > 0 & ! True|2 > 0 & ! True|3 > 0 & ! Ch(0,3)|4 > 0 & ! Ch(0,4)|5 > 0 & ! Ch(0,5)|6 > 0 & ! Ch(0,6)|7 > 0 & ! Ch(0,7)"

def __set_default_value(logical_formula, model):
	"""
		set the unknown fluent not in assignment with the default value
	"""
	#print logical_formula
	universe, assignment, default_value = model
	encode_pair_list = default_value.items()
	logical_formula = Util.repeat_do_function(Util.sub_lambda_exp, encode_pair_list, logical_formula)
	#print logical_formula
	#exit(0)
	return logical_formula


print __set_default_value(F, M)


