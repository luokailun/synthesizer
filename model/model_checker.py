from basic import Util
from basic import context_operator
from formula import Formula
import re
import itertools
import evaluation




##############################################################################################################################################################
# because we need to assignment formula like cell(len(),1) with {len(): 2, cell(2,1): 1}

def __assignment(formula, assignment):
	replace_list = [ (r'\b%s'%(fluent.replace('(','\(').replace(')','\)')), str(value)) for fluent, value in assignment.iteritems()]
	#print replace_list
	while True:
		new_formula = Util.repeat_do_function(Util.sub_lambda_exp, replace_list, formula)
		if new_formula == formula:
			return formula
		else:
			formula = new_formula



def __assignment_light(formula, assignment):
	#print replace_list
	return Util.repeat_do_function(Util.replace_lambda_exp, list(assignment.items()), formula)




def __grounding_conjunct(var_list, sorts, formula, universe, var_constraint_dict=None):

	#vars_consts = [ (var, var_constraint_dict[var]) if var in var_constraint_dict else (var, universe[sorts[e]]) for e, var in enumerate(var_list) ]
	#print '~~~~', var_list, sorts, formula, universe
	vars_consts = [ (var, universe[sorts[e]]) for e, var in enumerate(var_list) ]
	#print vars_consts
	consts_list = list(itertools.product(*zip(*vars_consts)[1]))
	#print consts_list
	instances = [ Util.endecode_string(formula, var_list, list(consts)) for consts in consts_list]
	return '|'.join(instances)




'''
encode_pair_logic = (['>=', '<=','=<', '=>'],['@','#','$','~'])

def __to_python_equivalent(formula):
	formula =Util.endecode_string(formula, encode_pair_logic[0], encode_pair_logic[1])
	formula = formula.replace('=','==')
	formula =Util.endecode_string(formula, encode_pair_logic[1], encode_pair_logic[0])
	return formula
'''



def sat_conjunct_by_model(model, conjunct):
	#print '!',model
	#print '@',conjunct
	var_list, sort_list, pred_list= conjunct
	universe, assignment = model

	#var_constraint_dict = context_operator.get_pred_constraint_dict()
	#var_constraint_dict = var_constraint_dict[formula] if formula in var_constraint_dict else dict()
	#formula = __to_python_equivalent(' & '.join(pred_list))
	formula = ' & '.join(pred_list)
	#print '--------formula',formula
	#print var_list, sorts, formula, universe, var_constraint_dict
	ground_formula = formula if var_list == [] else __grounding_conjunct(var_list, sort_list, formula, universe)
	#print '--------ground formula',ground_formula
	logical_formula = __assignment_light(ground_formula, assignment)
	#logical_formula = unknown_pattern.sub(__mrepl_unknown,logical_formula)
	#print '--------logical',logical_formula
	if var_list == []:
		return evaluation.eval_expression(logical_formula, {'True':True, 'False':False})
	instance_list = logical_formula.split('|')
	m_dict = {'True':True, 'False':False}
	for instance in instance_list:
		if evaluation.eval_expression(instance, m_dict) is True:
			return True
	return False



##############################################################################################################################################################



def sat_conjunct(model_list, conjunct):
	for model in model_list:
		#print preds_sat_model_org(model, [pred])
		if sat_conjunct_by_model(model, conjunct) is False :
			return False
	return True



def unsat_conjunct(model_list, conjunct):
	for model in model_list:
		#print preds_sat_model_org(model, [pred])
		if sat_conjunct_by_model(model, conjunct) is True:
			return False
	return True


##############################################################################################################################################################

# math checking is just approximated. We only expand the Int range


def sat_conjunct_by_model_math(model, conjunct, MIN=0, INC=6):
	#print '!',model
	#print '@',conjunct
	var_list, sort_list, pred_list= conjunct
	universe, assignment = model
	MAX = INC + max([int(e) for e in universe['Int']])
	temp_list = universe['Int']
	universe['Int'] = [str(e) for e in list(range(MIN,MAX))]
	#var_constraint_dict = context_operator.get_pred_constraint_dict()
	#var_constraint_dict = var_constraint_dict[formula] if formula in var_constraint_dict else dict()
	formula = ' & '.join(pred_list)
	#print '--------formula',formula
	#print var_list, sorts, formula, universe, var_constraint_dict
	ground_formula = formula if var_list == [] else __grounding_conjunct(var_list, sort_list, formula, universe)
	universe['Int'] = temp_list
	#print '--------ground formula',ground_formula
	logical_formula = __assignment(ground_formula, assignment)
	#logical_formula = unknown_pattern.sub(__mrepl_unknown,logical_formula)
	#print '--------logical',logical_formula
	if var_list == []:
		return evaluation.eval_expression(logical_formula, {'True':True, 'False':False})
	instance_list = logical_formula.split('|')
	m_dict = {'True':True, 'False':False}
	for instance in instance_list:
		if evaluation.eval_expression(instance, m_dict) is True:
			return True
	return False


def unsat_conjunct_math(model_list, conjunct):
	
	for model in model_list:
		if sat_conjunct_by_model_math(model, conjunct) is True:
			return False
	return True



##############################################################################################################################################################


def get_unsat_models(model_list, conjunct):
	return [model for model in model_list if sat_conjunct_by_model(model, conjunct) is False]


def get_sat_models(model_list, conjunct):
	return [model for model in model_list if sat_conjunct_by_model(model, conjunct) is True]



##############################################################################################################################################################


def __get_const_value(universe, fluents, assignment):

	consts = sum([ const_list for sort, const_list in universe.iteritems() if sort!="Int" and sort!="Bool" ],[])
	consts = [elem for elem in consts if elem not in fluents]
	#const_fluents = ["%s()"%fluent for fluent in fluents]
	const_value = [ (fluent,assignment["%s()"%fluent]) for fluent in fluents if "%s()"%fluent in assignment.keys()]
	for e, elem in enumerate(consts):
		const_value.append((elem,e))
	const_value_statement = [ "%s=%s"%(const,value) for (const,value) in const_value ]
	#print const_value_statement
	scope =dict()
	for statement in const_value_statement:
		exec(statement,scope)
	return scope


encode_pair_logic = (['>=', '<=','=<', '=>'],['@','#','$','~'])

def __to_python_formula(formula):
	formula =Util.endecode_string(formula, encode_pair_logic[0], encode_pair_logic[1])
	formula = formula.replace('=','==')
	formula =Util.endecode_string(formula, encode_pair_logic[1], encode_pair_logic[0])
	return formula.replace('!',' not ').replace('&', ' and ').replace('|', ' or ')


def sat_formula(model, formula):

	universe, assignment = model
	formula = __to_python_formula(formula)
	#print '1,---------',formula
	formula = Formula.transform_entailment(formula)
	#print '2,---------',formula
	ground_formula = Formula.grounding(formula, model)
	#print '3,--------',ground_formula
	logical_formula = __assignment(ground_formula, assignment)
	#print '4,--------model replace',logical_formula
	#print 'kkkk',context_operator.get_sort_symbols_dict()
	#logger.debug("Checking formula %s with model %s \n formula after grounding: %s \n after model_replace %s"%(formula,model,ground_formula,logical_formula))
	scope = __get_const_value(context_operator.get_sort_symbols_dict(), context_operator.get_fluents(), assignment)
	flag = eval(logical_formula,scope)
	#logger.debug('sat?: \n%s'%flag)
	return flag



##############################################################################################################################################################


