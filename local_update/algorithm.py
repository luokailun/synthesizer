

from regression import program_regress
from prover import z3prover
from model import model_interpretor
from basic import context_operator
from model import model_checker
#from local_update import local_update
import local_update
from formula import Fstructure
import scoring


def ____get_vars(sorts, sort, player):
	return [ context_operator.get_new_var() if s!=sort else player for s in sorts]



def __generate_pi_action(player):
	functions_sorts = context_operator.get_functions_sorts()
	sort_consts_dict = context_operator.get_sort_symbols_dict()
	p_sort = [sort for sort, consts in sort_consts_dict.iteritems() if player in consts].pop()

	actions_sorts_vars = [ (fun, sorts[0:len(sorts)-1] , ____get_vars(sorts[0:len(sorts)-1], p_sort, player)) \
	for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]

	action_list = [ "pi(%s)[%s(%s)]"%(','.join(["%s:%s"%(v,s) for (v,s) in zip(v_list,s_list) if s!=p_sort]) \
		, action, ','.join(v_list)) for (action, s_list, v_list) in actions_sorts_vars]

	return '#'.join(action_list)



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


def __get_sat_goal_Aformula(fstructure, Goal, predicate_list, pred_score_dict):
	print 'generating A formula .....'
	while True:
		formula = Fstructure.to_formula(fstructure)
		formula = '!numStone()%4=0&turn(p1)'
		A_formula = program_regress.A_regress(formula, __generate_pi_action('p2'))
		print 'aaaa',A_formula
		result = z3prover.imply(A_formula, Goal, "(set-option :timeout 10000)")
		if model_interpretor.interpret_result(result) is True:
			return A_formula, fstructure
		elif model_interpretor.interpret_result(result) is False:
			temp_model = __generate_small_model(A_formula, Goal, result)
			print 'temp N model:', temp_model

			model_formula = program_regress.E_regress(model_checker.to_formula(temp_model), __generate_pi_action('p1'))
			result = z3prover.imply('(%s)&(%s)'%(formula, model_formula), 'false', "(set-option :timeout 10000)")

			print model_formula
			print formula
			print result
			if model_interpretor.interpret_result(result) is False:
				negative_model = model_interpretor.interpret_model(result)
				fstructure = local_update.N_update(fstructure, negative_model, predicate_list, pred_score_dict)
				print 'update(n):~~~~~~~~~', formula
			else:
				print 'ERROR!!'
				exit(0)
		else:
			print 'backtrack'
			exit(0)

# Input: a initial database Init, the Goal  and a predicate_list
# Output: a game invariant F s.t.   (1) Init \models F,  (2) F \models Goal  (3) F \models AEregression(F)


def synthesis(Init, Goal, predicate_list):
	n=1

	positive_model_list = list()
	conjunct_model_list = list()
	# see the definition of fstructure in formula dir
	fstructure = Fstructure.init(Goal, positive_model_list, conjunct_model_list)

	# set the inital score (c=0) for each generated predicates 
	pred_score_dict = scoring.init_preds_base_score(predicate_list)

	while n>0:

		A_formula, fstructure = __get_sat_goal_Aformula(fstructure, Goal, predicate_list, pred_score_dict)
		EA_formula = program_regress.E_regress(A_formula, __generate_pi_action('p1'))
		# checking condition (3)
		formula = Fstructure.to_formula(fstructure)
		result = z3prover.imply(formula, EA_formula, "(set-option :timeout 10000)")
		print 'before regress: ~~~~~~:', formula
		print 'regress: ~~~~~~~~~~', EA_formula
		print	
		# if condition (3) holds
		if model_interpretor.interpret_result(result) is True:
			# checking condition (1)
			result = z3prover.imply(Init, formula, "(set-option :timeout 10000)")
			# if condition (1) holds 
			if model_interpretor.interpret_result(result) is True:
				print '#success~~~~~:', formula
				return formula #return the result (we have guaranteed condition (2) holds)
			elif model_interpretor.interpret_result(result) is False:
			# if condition (2) does not holds, generate small model M and strengthen formula F (fstructure): 
			# ensure that M \models F
				positive_model = __generate_small_model(Init, formula, result)
				print 'P model:', positive_model
				fstructure = local_update.P_update(fstructure, positive_model, predicate_list, pred_score_dict)
			else:
				print 'backtrack'
				exit(0)
		# if condition (3) does not holds, generate small model M and strengthen formula F (fstructure)
		# ensure that M \not\models F
		elif model_interpretor.interpret_result(result) is False:
			negative_model = __generate_small_model(formula, EA_formula, result)
			print 'N model:', negative_model
			fstructure = local_update.N_update(fstructure, negative_model, predicate_list, pred_score_dict)
			formula = Fstructure.to_formula(fstructure)
			print 'update(n):~~~~~~~~~', formula
			print
			#exit(0)
		else:
			print 'backtrack'
			exit(0)


