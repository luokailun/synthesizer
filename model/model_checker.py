







#grounding_pattern_str = r"(?P<head>(?:forall|exists))\((?P<var>[\w\:\s\d,]+?)\)\[(?P<body>[^\[\]]+)\]"
#grounding_pattern = re.compile(grounding_pattern_str)
#p = "x>=5 and ! x=6"



##############################################################################################################################################################


#print to_pyFormula(p)
'''
universe = {'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}
formula  ="not  len() == X1 and  not  row(X11) == X1"
var_list = ['X1','X11']
sorts = ['Int','Int']
'''





##print __grounding_formula(var_list, sorts, formula, universe)

'''

def pred_sat_model(model, pred, universe, new_preds_dict):
	#print '--------model',model
	#print '--------pred',pred
	#print '--------universe',universe
	var_list, sorts = new_preds_dict[pred]
	formula = pred
	#var_list = [r"\b%s\b"%var for var in var_list]
	formula = __to_pyFormula(formula)
	#print '--------formula',formula
	var_constraint_dict = context_operator.get_pred_constraint_dict()
	var_constraint_dict = var_constraint_dict[pred] if pred in var_constraint_dict else dict()

	ground_formula = formula if var_list == [] else __grounding_formula(var_list, sorts, formula, universe, var_constraint_dict)
	#print '--------ground formula:',ground_formula
	logical_formula = __replace_model(ground_formula, model)
	#print '--------logical',logical_formula
	if var_list == []:
		return evaluation.eval_expression(logical_formula, {'True':True, 'False':False})
	instance_list = logical_formula.split('|')
	m_dict = {'True':True, 'False':False}
	for instance in instance_list:
		if evaluation.eval_expression(instance, m_dict) is True:
			return True
	return False

	#print '--------ground',ground_formula
	#print


def preds_sat_model(model, pred_list, new_preds_dict):
	universe = dict(context_operator.get_sort_symbols_dict())
	#scope = progress.__get_const_value(universe, context_operator.get_fluents(), model)

	bound = context_operator.get_bound()
	if len(bound)==1:
		feature = ' '.join([ '%s %s'%(key,value) for key,value in model.iteritems()])
		max_num =  max([ int(num) for num in re.findall(r'\b\d+\b',feature)])
		if bound[0].find('>=')!=-1:
			universe['Int'] = [ str(e) for e in range(0, max_num+1)]
		else:
			universe['Int'] = [ str(e) for e in range(1, max_num+1)]
	else:
		max_num =  int(model['len()'])
		universe['Int'] = [ str(e) for e in range(1, max_num+1)]

	#print '---------preds_sat_model'
	#print model
	#print universe
	#print pred_list
	#print  [pred for pred in pred_list if pred_sat_model(model, pred, universe, scope) is True]
	return [pred for pred in pred_list if pred_sat_model(model, pred, universe, new_preds_dict) is True]



def preds_unsat_model(model, pred_list, new_preds_dict):
	universe = dict(context_operator.get_sort_symbols_dict())
	#scope = progress.__get_const_value(universe, context_operator.get_fluents(), model)

	bound = context_operator.get_bound()
	if len(bound)==1:
		feature = ' '.join([ '%s %s'%(key,value) for key,value in model.iteritems()])
		max_num =  max([ int(num) for num in re.findall(r'\b\d+\b',feature)])
		if bound[0].find('>=')!=-1:
			universe['Int'] = [ str(e) for e in range(0, max_num+1)]
		else:
			universe['Int'] = [ str(e) for e in range(1, max_num+1)]
	else:
		max_num =  int(model['len()'])
		universe['Int'] = [ str(e) for e in range(1, max_num+1)]
	#max_num =  int(model['len()'])
	#universe['Int'] = [ str(e) for e in range(1, max_num+1)]
	#print model
	return [pred for pred in pred_list if pred_sat_model(model, pred, universe, new_preds_dict) is False]



def get_models_sat_pred(models, com_pred):
	var_list, sorts, pred = com_pred
	pred_dict = {pred: (var_list, sorts)}

	model_list = list()
	for model in models:
		universe = __get_universe(model)
		if pred_sat_model(model, pred, universe, pred_dict):
			model_list.append(model)
	return model_list


def count_models_sat_pred(models, var_list, sorts, pred):
	pred_dict = {pred: (var_list, sorts)}
	num = 0
	for model in models:
		universe = __get_universe(model)
		if pred_sat_model(model, pred, universe, pred_dict):
			num +=1
	return num


##############################################################################################################################################################


unknown_str = r'(?P<fun>\w+)\([\d,\w]+\)'
unknown_pattern = re.compile(unknown_str)

def __mrepl_unknown(matched):
	fluent_name = matched.group('fun')
	if fluent_name in context_operator.get_predicates():
		return 'False'
	else:
		return context_operator.get_unknown()
		#return 'unknown'
		#return '#'

def math_pred_sat_model(model, pred, universe):
	var_list, sorts, formula= pred

	#var_constraint_dict = context_operator.get_pred_constraint_dict()
	#var_constraint_dict = var_constraint_dict[formula] if formula in var_constraint_dict else dict()
	var_constraint_dict = dict()

	formula = __to_pyFormula(formula)
	ground_formula = formula if var_list == [] else __grounding_formula(var_list, sorts, formula, universe, var_constraint_dict)
	#print '---------111212',ground_formula
	logical_formula = __replace_model(ground_formula, model)
	#print '---------111212',logical_formula
	logical_formula = unknown_pattern.sub(__mrepl_unknown,logical_formula)
	#print '---------333333',logical_formula
	if var_list == []:
		return evaluation.eval_expression(logical_formula, {'True':True, 'False':False})
	#instance_list = logical_formula.split('|')
	instance_list = [ins for ins in logical_formula.split('|') if ins.find("#")==-1]
	m_dict = {'True':True, 'False':False}
	for instance in instance_list:
		if evaluation.eval_expression(instance, m_dict) is True:
			return True
	return False

def models_sat_math_pred(model_list, pred, universe):
	for model in model_list:
		if math_pred_sat_model(model, pred, universe) is False:
			return False
	return True

def models_unsat_math_pred(model_list, pred, universe):
	for model in model_list:
		if math_pred_sat_model(model, pred, universe) is True:
			return False
	return True

'''





##############################################################################################################################################################

from basic import Util
from basic import context_operator
from formula import Formula
import re
import itertools
import evaluation






def __assignment(formula, assignment):

	replace_list = [ (r'\b%s'%(fluent.replace('(','\(').replace(')','\)')), str(value)) for fluent, value in assignment.iteritems()]
	#print replace_list
	while True:
		new_formula = Util.repeat_do_function(Util.sub_lambda_exp, replace_list, formula)
		if new_formula == formula:
			return formula
		else:
			formula = new_formula





def __grounding_conjunct(var_list, sorts, formula, universe, var_constraint_dict=None):

	#vars_consts = [ (var, var_constraint_dict[var]) if var in var_constraint_dict else (var, universe[sorts[e]]) for e, var in enumerate(var_list) ]
	#print '~~~~', var_list, sorts, formula, universe
	vars_consts = [ (var, universe[sorts[e]]) for e, var in enumerate(var_list) ]
	#print vars_consts
	consts_list = list(itertools.product(*zip(*vars_consts)[1]))
	#print consts_list
	instances = [ Util.endecode_string(formula, var_list, list(consts)) for consts in consts_list]
	return '|'.join(instances)





encode_pair_logic = (['>=', '<=','=<', '=>'],['@','#','$','~'])

def __to_python_equivalent(formula):
	formula =Util.endecode_string(formula, encode_pair_logic[0], encode_pair_logic[1])
	formula = formula.replace('=','==')
	formula =Util.endecode_string(formula, encode_pair_logic[1], encode_pair_logic[0])
	return formula



def sat_conjunct_by_model(model, conjunct):
	#print '!',model
	#print '@',conjunct
	var_list, sort_list, pred_list= conjunct
	universe, assignment = model

	#var_constraint_dict = context_operator.get_pred_constraint_dict()
	#var_constraint_dict = var_constraint_dict[formula] if formula in var_constraint_dict else dict()
	formula = __to_python_equivalent(' & '.join(pred_list))
	#print '--------formula',formula
	#print var_list, sorts, formula, universe, var_constraint_dict
	ground_formula = formula if var_list == [] else __grounding_conjunct(var_list, sort_list, formula, universe)
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


def get_unsat_models(model_list, conjunct):
	return [model for model in model_list if sat_conjunct_by_model(model, conjunct) is False]


def get_sat_models(model_list, conjunct):
	return [model for model in model_list if sat_conjunct_by_model(model, conjunct) is True]


##############################################################################################################################################################

# model is a tuple (U, S) where U is universe and S is an assignment

def to_formula(model):
	universe, assignment = model
	formula_list = list()
	for key,value in assignment.iteritems():
		if value is True:
			formula_list.append(key)
		elif value is False:
			formula_list.append('!%s'%key)
		else:
			formula_list.append('%s=%s'%(key,value))
	return '&'.join(formula_list)

##############################################################################################################################################################



grounding_pattern_str = r"(?P<head>(?:forall|exists))\((?P<var>[\w\:\s\d,_]+?)\)\[(?P<body>[^\[\]]+)\]"
grounding_pattern = re.compile(grounding_pattern_str)




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


def ____mrepl_ground(match):
	logical_connector = "&" if match.group('head') =='forall' else '|'
	
	#universe = {'Int': ['1', '0', '3', '2'], '_S1': [], '_S2': ['p2', 'p1'], 'Bool': ['True', 'False']}

	universe, assignment = context_operator.get_current_model()

	vars_sorts = { elem.split(':')[0]: elem.split(':')[1] for elem in  match.group('var').split(',') }
	var_list = vars_sorts.keys()
	#var_constraint_dict = __get_constraint_var_dict(var_list, match.group('body'))
	
	#vars_consts = [ (var, var_constraint_dict[var])if var in var_constraint_dict else (var, universe[sort]) for var, sort in vars_sorts.iteritems()]
	vars_consts = [ (var, universe[sort]) for var, sort in vars_sorts.iteritems()]
	vars_list = [ r'\b'+var+r'\b' for var in zip(*vars_consts)[0] ]
	consts_list = list(itertools.product(*zip(*vars_consts)[1]))

	instances = [ Util.repeat_do_function(Util.sub_lambda_exp, zip(vars_list,list(consts)), match.group('body')) for consts in consts_list ]

	return "(%s)"%logical_connector.join(["(%s)"%ins for ins in instances ])


def __grounding_formula(formula, model):
	context_operator.set_current_model(model)
	return Util.repeat_replace_inner_with_pattern(grounding_pattern, ____mrepl_ground, formula)


def __to_python_formula(formula):
	formula = __to_python_equivalent(formula)
	return formula.replace('!',' not ').replace('&', ' and ').replace('|', ' or ')


def sat_formula(model, formula):

	universe, assignment = model
	formula = __to_python_formula(formula)
	#print '1,---------',formula
	formula = Formula.entailment_eliminate(formula)
	#print '2,---------',formula
	ground_formula = __grounding_formula(formula, model)
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


