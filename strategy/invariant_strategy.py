
# translate a invariant to a strategy
# such that this strategy maintain the invariant
#
# 
#

from formula import Fstructure
from regression import atomic_regress
from basic import context_operator
from prover import z3prover
from model import model_interpretor


def from_invariant_to_strategy(two_state_structure):
	#
	# generate invariant strategy that maintain the invariant
	#
	#
	fstructure1, fstructure2 = two_state_structure
	invariant1_list = Fstructure.to_formula_list(fstructure1)
	invariant2_list = Fstructure.to_formula_list(fstructure2)

	invariant1_list = __delete_weak_clauses(invariant1_list)
	invariant2_list = __delete_weak_clauses(invariant2_list)


	action_list = __generate_para_action('p1')

	return [(atomic_regress.regress('&'.join(invariant2_list), action), action) for action in action_list]




def __generate_para_action(player):
	"""
		generate actions with parameters
	"""
	functions_sorts = context_operator.get_functions_sorts()
	sort_consts_dict = context_operator.get_sort_symbols_dict()
	p_sort = [sort for sort, consts in sort_consts_dict.iteritems() if player in consts].pop()

	actions_sorts_vars = [ (fun, sorts[0:len(sorts)-1] , \
	[ context_operator.get_new_var() if s!=p_sort else player for s in sorts[0:len(sorts)-1]] ) \
	for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]

	action_list = [ "%s(%s)"%(action, ','.join(v_list)) for (action, s_list, v_list) in actions_sorts_vars]

	return action_list



def __delete_weak_clauses(clause_list):
	"""
		delete clauses that are redundant
	"""
	delete_list = list()
	for i in range(0,len(clause_list)):
		for j in range(i+1, len(clause_list)):
			if model_interpretor.interpret_result(z3prover.imply(clause_list[i],clause_list[j])) is True:
				delete_list.append(clause_list[j])
			elif model_interpretor.interpret_result(z3prover.imply(clause_list[j],clause_list[i])) is True:
				delete_list.append(clause_list[i])

	clause_list = [c for c in clause_list if c not in delete_list]
	return clause_list

