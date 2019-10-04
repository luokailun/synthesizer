from regression import program_regress
from prover import z3prover
from prover import mcmas
from model import model_interpretor
from model import model_progress
from basic import context_operator
from model import model_checker
#from local_update import local_update
import local_update
import copy
import itertools
from formula import Fstructure
import scoring

################################################################################################################################################
file_regress = open('./temp/regress','write')


def __printer(two_state_structure):
	print_list =list()
	fstructure1, fstructure2 = two_state_structure
	print_list.append('--------------------------')
	print_list.append('[Structure1]\n%s\n'%(Fstructure.printer(fstructure1)))
	print_list.append('[Structure2]\n%s'%(Fstructure.printer(fstructure2)))
	print_list.append('\n[Formula1]: %s\n[Formula2]:%s'%(Fstructure.to_formula(fstructure1),Fstructure.to_formula(fstructure2)))
	print_list.append('~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
	return '\n'.join(print_list)

################################################################################################################################################

def ____update_structure(fstructure, model_list, pred_list):
	poss_model_list = Fstructure.get_pos_models(fstructure)
	for model in model_list:
		if model not in poss_model_list:
			fstructure = local_update.P_update(fstructure, model, pred_list)
	return fstructure


def __structure_P_update(two_state_structure, two_state_models, pred_list):
	fstructure1, fstructure2 = two_state_structure
	model_list1, model_list2 = two_state_models

	fstructure1 = ____update_structure(fstructure1, model_list1, pred_list)
	fstructure2 = ____update_structure(fstructure2, model_list2, pred_list)

	return (fstructure1, fstructure2)

################################################################################################################################################

def __progress_model(model):

	universe, assignment = model
	functions_sorts = context_operator.get_functions_sorts()
	actions = context_operator.get_actions()
	actions_sorts = [ (fun, sorts[0:len(sorts)-1]) for fun, sorts in functions_sorts.iteritems() if fun in actions ]

	new_model_list = list()
	for action_name, sort_list in actions_sorts:
		paras_list = list(itertools.product(*[ universe[sort] for sort in sort_list ]))
		actions = ["%s(%s)"%(action_name, ','.join(list(paras))) for paras in paras_list] 
		model_list = [model_progress.progress(action, model) for action in actions if model_progress.poss(action, model)]

		new_model_list.extend(model_list)
	return new_model_list



################################################################################################################################################

def __generate_small_model(formula1, formula2, results,  MAX_VALUE=2):
	#results = __interpret_model(__imply(formula1, formula2, "(set-option :timeout 10000)"), MAX_VALUE)
	#print '----------org---------',results
	flag, element = model_interpretor.interpret_model(results, MAX_VALUE)
	while flag is False:

		value_constraints = ' '.join([ "(assert %s)"%util_trans_smt.get_smt_body('%s<=%s'%(constraint,MAX_VALUE)) for constraint in element])
		new_results = z3prover.imply(formula1,formula2, "(set-option :timeout 4000)"+z3prover.generate_head()+value_constraints)

		if model_interpretor.interpret_results(new_results) is False:
			flag, element = model_interpretor.interpret_model(new_results, MAX_VALUE)

		MAX_VALUE = MAX_VALUE+2
	return element


################################################################################################################################################


def ____generate_pi_action(player):
	functions_sorts = context_operator.get_functions_sorts()
	sort_consts_dict = context_operator.get_sort_symbols_dict()
	p_sort = [sort for sort, consts in sort_consts_dict.iteritems() if player in consts].pop()

	actions_sorts_vars = [ (fun, sorts[0:len(sorts)-1] , \
	[ context_operator.get_new_var() if s!=p_sort else player for s in sorts[0:len(sorts)-1]] ) \
	for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]

	action_list = [ "pi(%s)[%s(%s)]"%(','.join(["%s:%s"%(v,s) for (v,s) in zip(v_list,s_list) if s!=p_sort]) \
		, action, ','.join(v_list)) for (action, s_list, v_list) in actions_sorts_vars]

	return '#'.join(action_list)




def ____check_convergence(formula1, formula2, predicate_list):

	result = z3prover.imply(formula1, formula2, "(set-option :timeout 10000)")

	if model_interpretor.interpret_result(result) is True:
		return True
	elif model_interpretor.interpret_result(result) is False:
			negative_model = __generate_small_model(formula1, formula2, result)
			#print 'N model:', negative_model
			return negative_model
	else:
		print 'backtrack'
		return None
		exit(0)



def __structure_regress_until_convergence(two_state_structure, predicate_list):
	fstructure1, fstructure2 = two_state_structure

	while True:
		print('\n***************** Checking Convergence *****************:\n\n')

		formula1 = Fstructure.to_formula(fstructure1)
		formula2 = Fstructure.to_formula(fstructure2)

		regress_formula1 = program_regress.A_regress(formula1, ____generate_pi_action('p2'))
		regress_formula2 = program_regress.E_regress(formula2, ____generate_pi_action('p1'))

		negative_model1 = ____check_convergence(formula1, regress_formula2, predicate_list)
		negative_model2 = ____check_convergence(formula2, regress_formula1, predicate_list)

		if negative_model1 is True and negative_model2 is True:
			return (fstructure1, fstructure2)
		elif negative_model1 is None or negative_model2 is None:
			print 'try backtrack....'
		else:
			if negative_model1 is not True:
				print('(1) N model %s\n'%str(negative_model1))
				fstructure1 = local_update.N_update(fstructure1, negative_model1, predicate_list)
			if negative_model2 is not True:
				print('(2) N model %s\n'%str(negative_model2))
				fstructure2 = local_update.N_update(fstructure2, negative_model2, predicate_list)

		print('\n***************** N Update Structure *****************:\n\n%s'%__printer((fstructure1, fstructure2)))

################################################################################################################################################





def synthesis(Init, Goal, predicate_list):
	"""
	Synthesize sufficient and necessary invariants X, where each formula f in X is of the form:
				f= \forall* Goal and clause1 and clause2 and ...

	@param Init 	initial database DS0 of the game
	@param Goal		the goal that always be true
	@param Predicate_list 	a list of generated predicates	

	# return: a game invariant F s.t.  (1) Init \models F,  (2) F \models Goal  (3) F \models AEregression(F)
	"""
	n=1
	# Set the inital score (c=0) for each generated predicate
	pred_score_dict1 = scoring.init_preds_base_score(predicate_list)
	pred_score_dict2 = copy.deepcopy(pred_score_dict1)

	# See the definition of Fstructure in formula dir
	fstructure1 = Fstructure.init(Goal, list(), list(), pred_score_dict1)
	fstructure2 = Fstructure.init(Goal, list(), list(), pred_score_dict2)
	## Divide into two states: player1's state and player2's state
	two_state_structure = (fstructure1, fstructure2)

	while n>0:
		print(__printer(two_state_structure))
		# Getting a sufficient invariant
		new_two_state_structure= __structure_regress_until_convergence(two_state_structure, predicate_list)
		formula1 = Fstructure.to_formula(new_two_state_structure[0])

		print('\n***************** Checking DS0 *****************:\n\n')
		# Proving the invariant is necessary
		result = z3prover.imply(Init,formula1, "(set-option :timeout 10000)")
		if model_interpretor.interpret_result(result) is True:
			print '#success~~~~~:', new_two_state_structure
			return new_two_state_structure #return the result (we have guaranteed condition (2) holds)

		# If the invariant is not necessary, update the formulas using the counterexamples.
		elif model_interpretor.interpret_result(result) is False:

			positive_model = __generate_small_model(Init, formula1, result)
			progress_model_list = __progress_model(positive_model)
			update_model_list = [model for model in progress_model_list if mcmas.interpret_result(mcmas.check_win(model,Goal))]

			print('P model:%s\nP progress model:%s\n'%(str(positive_model), '\n'.join([str(m) for m in update_model_list])))
			two_state_structure = __structure_P_update(new_two_state_structure, ([positive_model], update_model_list), predicate_list)
			print('\n***************** P Update Structure *****************:\n\n')
		else:
			print 'backtrack'
			exit(0)


