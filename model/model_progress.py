


import model_checker
from basic import Util
from basic import context_operator
import itertools



def poss(action_str, model):

	feature =  Util.generate_function_feature(action_str)
	lambda_function, para_selected_list= context_operator.find_axiom_with_feature('poss', feature)
	#print '----', lambda_function, para_selected_list
	formula = lambda_function if  isinstance(lambda_function, str) else lambda_function(para_selected_list)

	return model_checker.sat_formula(model, formula)




def __model_ssa(fluent, action_str, model):

	feature = Util.generate_function_feature(fluent)+'_'+Util.generate_function_feature(action_str)
	lambda_function, para_selected_list= context_operator.find_axiom_with_feature("ssa", feature)
	#print '----', lambda_function, para_selected_list
	formula = lambda_function if  isinstance(lambda_function, str) else lambda_function(para_selected_list)

	#print 'ffff', formula
	return model_checker.sat_formula(model, formula)#eval(__replace_model(ground_formula, model))





def progress(action_str, model):     # here action is a ground term
	
	universe, assignment, default_value = model
	fluent_sorts = context_operator.get_functions_sorts()
	fluents = context_operator.get_fluents()
	predicates = context_operator.get_predicates()
	predicate_sorts = context_operator.get_predicate_sorts()

	fun_fluents_sorts = [(fluent, sorts) for fluent, sorts in fluent_sorts.iteritems() if fluent not in predicates and fluent in fluents]
	pred_fluents_sorts = [(fluent, sorts) for fluent, sorts in predicate_sorts.iteritems()]

	#print fluents, fun_fluents_sorts, pred_fluents_sorts

	new_model_list = list()
	#model_elem_set = set(assignment.keys())
	for fluent_name, sorts in fun_fluents_sorts:
		#print sorts
		consts = [universe[sort] for e, sort in enumerate(sorts) ]
		f_fluent_tuples = [(fluent_name+"("+",".join(list(elem)[0:len(elem)-1]) + ")", elem[len(elem)-1]) for elem in list(itertools.product(*consts))]
		f_fluents = [ '%s=%s'%(fun,value) for fun, value in f_fluent_tuples]
		#add_list.extend([fun for fun,value in f_fluent_tuples if fun not in model_elem_set])
		new_model_list.extend([f_fluent for f_fluent in f_fluents if __model_ssa(f_fluent, action_str,  model)])


	for fluent_name, sorts in pred_fluents_sorts:
		#print fluent_name, sorts
		consts = [universe[sort] for e, sort in enumerate(sorts) ]
		#print consts
		p_fluents = [fluent_name+"("+",".join(list(elem)[0:len(elem)]) + ")" for elem in list(itertools.product(*consts))]
		new_model_list.extend([p_fluent+"="+str(__model_ssa(p_fluent, action_str, model)) for p_fluent in p_fluents  ])

	new_assignment = { fluent.split("=")[0]: fluent.split("=")[1] for fluent in new_model_list}

	return (universe, new_assignment, default_value)


