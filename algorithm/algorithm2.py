from regression import program_regress
from prover import z3prover
from prover import mcmas
from model import model_interpretor
from model import model_progress
from basic import context_operator
from model import model_checker
from prover import smt_translator
#from local_update import local_update
import local_update
import copy
import itertools
from formula import Fstructure
import scoring
import restart
import backtrack
from basic import format_output



################################################################################################################################################
#file_regress = open('./temp/regress','write')


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

def __progress_model(model):
	"""
		update the model to a set of models by doing any possible action
	"""
	universe, assignment, default_value = model
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
	"""
		generate a model that entails formula 1 but not formula2
		the universe of the model should be smallest 
	"""
	flag, element = model_interpretor.interpret_model(results, max_value=MAX_VALUE)
	while flag is False:

		value_constraints = ' '.join([ "(assert %s)"%smt_translator.get_smt_body('%s<=%s'%(constraint,MAX_VALUE)) for constraint in element])
		new_results = z3prover.imply(formula1,formula2, "(set-option :timeout 4000)"+value_constraints)
		#exit(0)
		if model_interpretor.interpret_result(new_results) is False:
			flag, element = model_interpretor.interpret_model(new_results, max_value=MAX_VALUE)

		MAX_VALUE = MAX_VALUE+2
	return element


################################################################################################################################################


def __update_structure(state, fstructure, neg_model_list, pos_model_list, pred_list):
	"""
	 P update is prefer than N update
	"""
	if pos_model_list!=list():
		update_type = 'P'
		update_model_list = pos_model_list
		update_function = local_update.P_update
	elif neg_model_list:
		update_type = 'N'
		update_model_list = neg_model_list
		update_function = local_update.N_update
	else:
		return fstructure

	# memory the type and the state of update for possible backtrack
	backtrack.set_update(update_type, state)
	print('State %s: %s models %s\n'%(state, update_type, str(update_model_list)))
	print(format_output.format_outputs(update_model_list, 'Ch'))
	fstructure = update_function(fstructure, update_model_list, pred_list)
	return fstructure


################################################################################################################################################



def ____check_reachability(model):

	Init_formula = context_operator.get_axioms()['init']['']
	if model_checker.sat_formula_math(model, Init_formula) is True:
		return True
	else:
	 	return mcmas.interpret_result(mcmas.check_reachability(model))



def __decide_update_model(model, state_type, Goal, player):
	"""
		decide to use the N update or P update
		@param 		model 			the model needed to use by N update or P update
		@param 		state_type		in the A state or E state
		@param 		Goal 			the goal needed be checked
		@return 	two models set (M1, M2), where
				        --- M1 means models need to be excluded in the current; 
				        --- M2 means models need to be included in the next state.
	"""
	#print("Checking %s model: %s\n%s"%(state_type, str(model), format_output.format_output(model,'Ch')))
	print("Checking %s model: %s\n"%(state_type, str(model)))
	print(format_output.format_output(model, 'Ch'))
	universe, assignment, default_value = model
	current_exclude_models, next_include_models = list(), list()

	right_turn = True if assignment['turn(p1)'] == 'True' and state_type == 'E' or assignment['turn(p2)'] == 'True' and state_type == 'A' else False

	if right_turn is False:
		print('**** Wrong Turn! Exclude it\n')
		current_exclude_models = [model]
	elif mcmas.interpret_result(mcmas.check_win(model, Goal, player)) is False:
		print('**** Lose Here! Exclude it\n')
		current_exclude_models = [model]
	elif ____check_reachability(model) is False:
		print('**** Not Reachable! Exclude it\n')
		current_exclude_models = [model]
	else:
		print('**** Win! Include it by next state\n')
		progress_model_list = __progress_model(model)
		update_model_list = [m for m in progress_model_list if mcmas.interpret_result(mcmas.check_win(m,Goal, player))]
		# if the state is in our turn, then we only choice an action to progress
		if state_type == 'E':
			next_include_models = [update_model_list.pop(0)]
		# if the state is in opponent's turn, then we know all actions should be performed
		else:
			next_include_models = update_model_list
	return current_exclude_models, next_include_models




def __generate_pi_action(player):
	"""
		generate a program denoting doing any possible action
	"""
	functions_sorts = context_operator.get_functions_sorts()
	sort_consts_dict = context_operator.get_sort_symbols_dict()
	p_sort = [sort for sort, consts in sort_consts_dict.iteritems() if player in consts].pop()

	actions_sorts_vars = [ (fun, sorts[0:len(sorts)-1] , \
	[ context_operator.get_new_var() if s!=p_sort else player for s in sorts[0:len(sorts)-1]] ) \
	for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]

	action_list = [ "pi(%s)[%s(%s)]"%(','.join(["%s:%s"%(v,s) for (v,s) in zip(v_list,s_list) if s!=p_sort]) \
		, action, ','.join(v_list)) for (action, s_list, v_list) in actions_sorts_vars]

	return '#'.join(action_list)




def __check_convergence(formula1, formula2):
	"""
		Checking whether formula 1 entails formula 2
	"""
	result = z3prover.imply(formula1, formula2, "(set-option :timeout 10000)")
	if model_interpretor.interpret_result(result) is True:
		return True
	elif model_interpretor.interpret_result(result) is False:
			negative_model = __generate_small_model(formula1, formula2, result)
			return negative_model
	else:
		print 'backtrack'
		return None
		exit(0)




def structure_regress_until_convergence(two_state_structure, pred_list, End,  Goal, player):
	"""
		update and check the two-state FSA until it becomes convergence (form an invariant)
	"""
	fstructure1, fstructure2 = two_state_structure

	while True:
		print('\n***************** Checking Convergence *****************:\n\n')

		formula1 = Fstructure.to_formula(fstructure1)
		formula2 = Fstructure.to_formula(fstructure2)

		regress_formula1 = program_regress.A_regress(formula1, __generate_pi_action('p2'))
		regress_formula2 = "!(%s)=>(%s)"%(End, program_regress.E_regress(formula2, __generate_pi_action('p1')))

		negative_model1 = __check_convergence(formula1, regress_formula2)
		negative_model2 = __check_convergence(formula2, regress_formula1)

		if negative_model1 is True and negative_model2 is True:
			return (fstructure1, fstructure2)
		elif negative_model1 is None or negative_model2 is None:
			print 'try backtrack....'
			fstructure1, fstructure2 = backtrack.backtrack(two_state_structure)
		else:
			e_neg_model_list, e_pos_model_list, a_neg_model_list, a_pos_model_list = list(), list(), list(), list()
			if negative_model1 is not True:
				e_neg_model_list, a_pos_model_list = __decide_update_model(negative_model1, 'E', Goal, player)
			if negative_model2 is not True:
				a_neg_model_list, e_pos_model_list = __decide_update_model(negative_model2, 'A', Goal, player)

			# initialize the choice structure for possible backtrack
			backtrack.init_choice()
			fstructure1 = __update_structure('q1', fstructure1, e_neg_model_list, e_pos_model_list, pred_list)
			fstructure2 = __update_structure('q2', fstructure2, a_neg_model_list, a_pos_model_list, pred_list)

			# if the local update fails, we restart by decreasing the score of the predicates
			if fstructure1 is None or fstructure2 is None:
				print('\n\n\n***************** Restart *****************:\n\n\n\n')
				fstructure1, fstructure2 =  restart.restart(two_state_structure)
				restart.init_conjunct_storer()
				#print fstructure1
				#exit(0)
			else:
				two_state_structure = (fstructure1, fstructure2)
				restart.store_two_state_conjuncts(two_state_structure)
		#print '#######~~~~~~~', storer[0]
		print('\n***************** Convergence Update Structure *****************:\n\n%s'%__printer((fstructure1, fstructure2)))


################################################################################################################################################


def synthesis(Init, End, Goal, player, pred_list):
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
	pred_score_dict1 = scoring.init_preds_base_score(pred_list)
	pred_score_dict2 = copy.deepcopy(pred_score_dict1)

	# See the definition of Fstructure in formula dir
	fstructure1 = Fstructure.init(Goal, list(), list(), pred_score_dict1)
	fstructure2 = Fstructure.init(Goal, list(), list(), pred_score_dict2)
	## Divide into two states: player1's state and player2's state
	two_state_structure = (fstructure1, fstructure2)

	# initialize to storing conjuncts for possible restart
	restart.init_conjunct_storer()

	while n>0:
		n += 1
		print(__printer(two_state_structure))
		# Getting a sufficient invariant
		new_two_state_structure = structure_regress_until_convergence(two_state_structure, pred_list, End,  Goal, player)
		formula1 = Fstructure.to_formula(new_two_state_structure[0])

		print('\n***************** Checking DS0 *****************:\n\n')
		# Proving the invariant is necessary
		result = z3prover.imply(Init, formula1, "(set-option :timeout 10000)")
		if model_interpretor.interpret_result(result) is True:
			print('#success~~~~~:')#, new_two_state_structure
			return new_two_state_structure #return the result (we have guaranteed condition (2) holds)

		# If the invariant is not necessary, update the formulas using the counterexamples.
		elif model_interpretor.interpret_result(result) is False:
			positive_model = __generate_small_model(Init, formula1, result)
			print('DS0 model:%s\n'%(str(positive_model)))
			print(format_output.format_output(positive_model, 'Ch'))

			progress_model_list = __progress_model(positive_model)
			update_model_list = [model for model in progress_model_list if mcmas.interpret_result(mcmas.check_win(model,Goal, player))]
			print('DS0 progressed updated model:%s\n'%('\n'.join([str(m) for m in update_model_list])))
			print(format_output.format_outputs(update_model_list, 'Ch'))
			print('---------------------------------------------------')
			fstructure1, fstructure2 = new_two_state_structure
			fstructure1 = __update_structure('q1',fstructure1,  [], [positive_model], pred_list)
			fstructure2 = __update_structure('q2', fstructure2, [], update_model_list, pred_list)
			two_state_structure = fstructure1, fstructure2
			# record for possible restart
			restart.store_two_state_conjuncts(two_state_structure)
			print('\n***************** P Update Structure *****************:\n\n')
		else:
			print('try backtrack....')
			two_state_structure = backtrack.backtrack(new_two_state_structure)


