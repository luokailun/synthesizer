#######################################################################################################################################

from basic import Util
from basic import context_operator
import re

quantifier_pattern = re.compile(r"(?:(forall|exists))\s*\(([\w:,\s\d_]+)\)\[([^\[\]]+)\]")
most_inner_pattern = re.compile(r'\(([^\(\)]+)\)')
entailment_pattern = re.compile(r'(?P<head>.+?)=>(?P<body>(?:.(?!=>))+.)')
encode_pair = (['(',')','[',']'],['#','$','{','}'])

def ____eliminate_entailment(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		formula = re.sub(entailment_pattern,"!#\g<head>$ or \g<body>",old_formula, 1)
	#print '---return',formula
	return formula


def ____mrepl_entailment_inner(mathched):
	#print mathched.groups()
	return "#%s$"%____eliminate_entailment(mathched.group(1))


def __eliminate_bracket(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		#print '1',formula
		formula = Util.repeat_replace_inner_with_pattern(most_inner_pattern, ____mrepl_entailment_inner, old_formula) 
		#print '2',formula
	return ____eliminate_entailment(formula)



def __mrepl_entailment_quantifier(matched):
	#print matched.groups()
	formula = __eliminate_bracket(matched.group(3))
	return Util.endecode_string("%s(%s)[%s]"%(matched.group(1),matched.group(2),formula), encode_pair[0], encode_pair[1])


def transform_entailment(formula):
	old_formula = ""
	while old_formula!=formula:
		old_formula = formula
		formula = Util.repeat_replace_inner_with_pattern(quantifier_pattern, __mrepl_entailment_quantifier, old_formula)
	return Util.endecode_string(__eliminate_bracket(formula),encode_pair[1],encode_pair[0])


#######################################################################################################################################



grounding_pattern_str = r"(?P<head>(?:forall|exists))\((?P<var>[\w\:\s\d,_]+?)\)\[(?P<body>[^\[\]]+)\]"
grounding_pattern = re.compile(grounding_pattern_str)


def __mrepl_ground(match):
	logical_connector = "&" if match.group('head') =='forall' else '|'
	
	#universe = {'Int': ['1', '0', '3', '2'], '_S1': [], '_S2': ['p2', 'p1'], 'Bool': ['True', 'False']}
	universe, assignment, default_value = context_operator.get_current_model()

	vars_sorts = { elem.split(':')[0]: elem.split(':')[1] for elem in  match.group('var').split(',') }
	var_list = vars_sorts.keys()
	#var_constraint_dict = __get_constraint_var_dict(var_list, match.group('body'))
	
	#vars_consts = [ (var, var_constraint_dict[var])if var in var_constraint_dict else (var, universe[sort]) for var, sort in vars_sorts.iteritems()]
	vars_consts = [ (var, universe[sort]) for var, sort in vars_sorts.iteritems()]
	vars_list = [ r'\b'+var+r'\b' for var in zip(*vars_consts)[0] ]
	consts_list = list(itertools.product(*zip(*vars_consts)[1]))

	instances = [ Util.repeat_do_function(Util.sub_lambda_exp, zip(vars_list,list(consts)), match.group('body')) for consts in consts_list ]

	return "(%s)"%logical_connector.join(["(%s)"%ins for ins in instances ])


def grounding(formula, model):
	context_operator.set_current_model(model)
	return Util.repeat_replace_inner_with_pattern(grounding_pattern, __mrepl_ground, formula)

#######################################################################################################################################
