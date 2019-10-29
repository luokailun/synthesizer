


import ispl_translator
import os
import re
from model import util_model
from basic import context_operator
from formula import Formula
import z3prover
from model import model_interpretor

################################################################################################################################################

result_string = r"Formula number 1:.+?, is (.+?) in the model"
result_pattern = re.compile(result_string)

def interpret_result(result):
	the_result = result_pattern.search(' '.join(result))
	if the_result is None:
		print 'ERROR'
		exit(0)
	elif the_result.group(1).replace(' ','') == 'TRUE':
		return True
	elif the_result.group(1).replace(' ','') == 'FALSE':
		return False
	else:
		print 'unmatch---:', the_result.group(1)
		exit(0)


################################################################################################################################################

def check_win(model, goal, player):
	init = util_model.to_formula(model)
	with open("./input_mcmas/win.ispl","write") as input_file:
		input_file.writelines(ispl_translator.to_ispl(model, init, goal, [player], 'G'))
		input_file.close()
		cmd = "./input_mcmas/mcmas ./input_mcmas/win.ispl"
		return os.popen(cmd).readlines()




################################################################################################################################################


'''

from basic import context_operator
from formula import Formula
from basic import format_output
from prover import z3prover
from model import model_interpretor
from basic import format_output
import re


def __get_init_models_with_universe(model):
	"""
		(light implementation) Get all the initial models under the universe of the model M
	"""
	universe, assignment, default_value = model
	Init_formula = context_operator.get_axioms()['init']['']
	Init_formula = Formula.grounding(Init_formula, model)

	#	get rigid function restrictions such that the initial models has the same valuation with the model M 
	rigid_function_list = context_operator.get_rigid_functions()
	if rigid_function_list!=list():
		rigid_function_pattern = re.compile('|'.join([r'\b%s\b'%(fun) for fun in rigid_function_list]))
		rigid_constraint = '&%s'%('&'.join(['%s=%s'%(key,value) for key, value in assignment.items() if rigid_function_pattern.search(key)]))
	else:
		rigid_constraint = ""

	# 	get domain constraints such that every sort (except) has finite objects in the universe
	domain_constraint = '&' + '&'.join(["forall(X:%s)[%s]"%(sort, ' or '.join(['X=%s'%elem for elem in constants])) \
				for sort, constants in universe.items() if sort!='Int' and sort!='Bool'])

	
	#	for integer we only set the value of those fluent less than maximal number in the universe
	#	 	(for light implementation we only set 0-arity fluent)
	
	max_num = max([ int(e) for e in universe['Int'] ])
	fun_sorts_dict = context_operator.get_functions_sorts()
	
	zero_fluent_list = [fun for fun in context_operator.get_zero_fluents()\
		if fun not in rigid_function_list and fun_sorts_dict[fun] == ['Int'] ] 

	if zero_fluent_list !=list():
		interger_constraint = "&" + "&".join(['%s()<=%s'%(fun, str(max_num)) for fun in zero_fluent_list])
	else:
		interger_constraint = ""


	model_formula = Init_formula + rigid_constraint + domain_constraint + interger_constraint
	new_model_list = list()

	n = 0
	while n<5:
		result = z3prover.imply(model_formula,'false')
		if model_interpretor.interpret_result(result) is False:
			#for simplicity we just get 5 models (light implementation)
			flag, new_model = model_interpretor.interpret_model(result, universe=universe)
			new_model_list.append(new_model)
			new_model_formula = util_model.to_formula(new_model)
			model_formula = model_formula + '&!(%s)'%new_model_formula
			n=n+1
			#print format_output.format_output(new_model, 'Ch')
		else:
			break 

	if new_model_list!=list():
		return new_model_list
	else:
		print('ERROR')
		exit(0)




def check_reachability(model):
	
	init_model_list = __get_init_models_with_universe(model)
	Init_formula = ' or '.join([util_model.to_formula(m) for m in init_model_list])
	State_formula = util_model.to_formula(model)
	#exit(0)
	with open("./input_mcmas/reachability.ispl","write") as input_file:
		input_file.writelines(ispl_translator.to_ispl(model, Init_formula, State_formula, ['p1','p2'], 'F'))
		input_file.close()
		cmd = "./input_mcmas/mcmas ./input_mcmas/reachability.ispl"
		return os.popen(cmd).readlines()


'''



#M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': True, 'numStone()': 1, 'turn(p2)': False})

#Goal = "numStone()=0 => !turn(p1)"


