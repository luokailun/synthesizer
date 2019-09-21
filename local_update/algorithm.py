

from regression import program_regress
from prover import z3prover
from model import model_interpretor
from basic import context_operator
#from local_update import local_update
import local_update
from formula import Fstructure
import scoring


def ____get_vars(sorts):
	return [ (context_operator.get_new_var(), sort) for sort in sorts]


def __generate_pi_action():
	functions_sorts = context_operator.get_functions_sorts()

	actions_sorts = [ (fun, sorts) for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]
	action_vars_sorts = [ (action, ____get_vars(sorts[0:len(sorts)-1])) for action, sorts in actions_sorts]
	actions = "#".join([  "%s(%s)" % (action ,",".join(zip(*elem)[0])) for action, elem in action_vars_sorts])
	#print "---------",actions
	vars_sorts = ','.join([elem[0] + ":" + elem[1] for action, elem_list in action_vars_sorts for elem in elem_list])

	return "pi(" + vars_sorts + ")[" + actions +"]"



def __generate_small_model(formula1, formula2, results,  MAX_VALUE=2):
	#results = __interpret_model(__imply(formula1, formula2, "(set-option :timeout 10000)"), MAX_VALUE)
	print '----------org---------',results
	flag, element = model_interpretor.interpret_model(results, MAX_VALUE)
	while flag is False:

		value_constraints = ' '.join([ "(assert %s)"%util_trans_smt.get_smt_body('%s<=%s'%(constraint,MAX_VALUE)) for constraint in element])
		new_results = z3prover.imply(formula1,formula2, "(set-option :timeout 4000)"+z3prover.generate_head()+value_constraints)

		if imodel_interpretor.nterpret_results(new_results) is False:
			flag, element = model_interpretor.interpret_model(new_results, MAX_VALUE)

		MAX_VALUE = MAX_VALUE+2
	return element




def synthesis(Init, Goal, predicate_list):
	n=1

	positive_model_list = list()
	conjunct_model_list = list()
	fstructure = Fstructure.init(Goal, positive_model_list, conjunct_model_list)

	pred_score_dict = scoring.init_preds_base_score(predicate_list)

	while n>0:
		formula = Fstructure.to_formula(fstructure)
		next_formula = program_regress.A_regress(program_regress.E_regress(formula, __generate_pi_action()), __generate_pi_action())
		print 'before regress: ~~~~~~:', formula
		print 'regress: ~~~~~~~~~~', next_formula
		print
		result = z3prover.imply(formula, next_formula, "(set-option :timeout 10000)"+z3prover.generate_head())

		if model_interpretor.interpret_result(result) is True:
			result = z3prover.imply(Init, formula, "(set-option :timeout 10000)"+z3prover.generate_head())

			if model_interpretor.interpret_result(result) is True:
				return formula
			elif model_interpretor.interpret_result(result) is False:

				positive_model = __generate_small_model(formula, next_formula, result)
				fstructure = local_update.P_update(fstructure, positive_model, predicate_list, pred_score_dict)
			else:
				pass

		elif model_interpretor.interpret_result(result) is False:

			negative_model = __generate_small_model(formula, next_formula, result)
			fstructure = local_update.N_update(fstructure, negative_model, predicate_list, pred_score_dict)
			formula = Fstructure.to_formula(fstructure)

			print 'update(n):~~~~~~~~~', formula
			print
			#exit(0)
		else:
			pass


