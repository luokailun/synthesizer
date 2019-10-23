"""

	Intuitively, a strategy is a "sub" transition system which is generate from a situation calculus model

	-- key: domain (universe)
	-- key: init_model 
	-- key: strategy (strategy tree)

		nodes {1: model, 2: model}
		structure {1: [1,2,3], 3:[4,5,6]}
		win nodes [0,1,3,4]

"""




from model import util_model
from prover import ispl_translator
from basic import context_operator
from formula import Formula
from basic import format_output
from prover import z3prover
from model import model_interpretor
from basic import format_output
import strategy_translator
import re
import os



################################################################################################################################################

def __check_win_strategy(model, goal, player):
	"""
		get the winning strategy (mcmas representation) under the model  
	"""
	init = util_model.to_formula(model)
	with open("./input_mcmas/win.ispl","write") as input_file:
		input_file.writelines(ispl_translator.to_ispl(model, init, goal, [player], 'G'))
		input_file.close()
		cmd = "./input_mcmas/mcmas -c 1 -l 1 -f 1 ./input_mcmas/win.ispl"
		return os.popen(cmd).readlines()


def check_and_get_strategy(model, goal, player):
	"""
		get the winning strategy (strategy structure representation) under the model  
	"""
	result = __check_win_strategy(model, goal, player)
	strategy_structure = strategy_translator.construct_strategy(result, model)
	return strategy_structure



################################################################################################################################################


def get_init_models_with_universe(universe):
	"""
		(light implementation) Get all the initial models under the universe of the model M
	"""
	Init_formula = context_operator.get_axioms()['init']['']
	Init_formula = Formula.grounding(Init_formula, (universe, dict(), dict()))

	# 	get domain constraints such that every sort (except) has finite objects in the universe
	domain_constraint = '&' + '&'.join(["forall(X:%s)[%s]"%(sort, ' or '.join(['X=%s'%elem for elem in constants])) \
				for sort, constants in universe.items() if sort!='Int' and sort!='Bool'])

	'''
		for integer fluent (whose value is integer) 
		we only set the value of those fluent less than maximal number in the universe
		
	'''
	max_num = max([ int(e) for e in universe['Int'] ])
	fun_sorts_dict = context_operator.get_functions_sorts()
	
	int_fluent_list = [ (fun, paras_value[0:len(paras_value)-1]) for fun, paras_value in fun_sorts_dict.items() if paras_value[-1] == 'Int' ] 
	ini_fluent_constraints = list()

	for fun, para_sorts in int_fluent_list:
		if para_sorts!= list():
			para_vars = ['X%s'%e for e in range(0,len(para_sorts))]
			para_var_sort_str = ';'.join(["%s:%s"%(var,sort) for var, sort in zip(para_vars, para_sorts)])
			fun_body_srt = "%s(%s)"%(fun, ','.join(para_vars))
			constraint = "forall(%s)[%s<=%s]"%(para_var_sort_str, fun_body_srt, max_num)
		else:
			constraint = '%s()<=%s'%(fun, str(max_num))
		ini_fluent_constraints.append(constraint)

	interger_constraint = "&" + "&".join(ini_fluent_constraints) if int_fluent_list !=list() else ""

	# generate models with these constraints.
	model_formula = Init_formula + domain_constraint + interger_constraint
	new_model_list = list()

	while True:
		result = z3prover.imply(model_formula,'false')
		if model_interpretor.interpret_result(result) is False:

			flag, new_model = model_interpretor.interpret_model(result, universe=universe)
			new_model_list.append(new_model)
			new_model_formula = util_model.to_formula(new_model)
			model_formula = model_formula + '&!(%s)'%new_model_formula
			#print format_output.format_output(new_model, 'Ch')
		else:
			break 

	if new_model_list!=list():
		return new_model_list
	else:
		print('ERROR')
		exit(0)

################################################################################################################################################


def find_model_in_strategys(strategy_list, model):
	"""
		find whether a model's universe has been generated strategies before
	"""
	universe, assignment, default_value = model
	for strategy in strategy_list:
		if cmp(strategy['domain'], universe) == 0:
			return True
	return False


################################################################################################################################################
# below are main procedure
################################################################################################################################################






