




f1 = ['( numStone()=0 ) => ( numStone()=0&!(turn(p1)) )', '!(exists(G0:_S1)[turn(G0)&turn(p2)])', '!(numStone() = 4)', '!(exists(G0:Int)[G0>=0&G0 % 4 = 0&numStone() = G0])']
f2 = ['( numStone()=0 ) => ( numStone()=0&!(turn(p1)) )', '!(exists(G0:Int)[G0>=0&! G0 % 4 = 0&numStone() = G0])']

from parser import BATparser
from prover import z3prover
from model import model_interpretor

BATparser.parser('takeaway.sc')

k1 = "( numStone()=0 ) => ( numStone()=0&!(turn(p1)) )"
k2 = "!(exists(G0:Int)[G0>=0&! G0 % 4 = 0&numStone() = G0])"

#print z3prover.imply(k2,k1)
#print z3prover.imply(k1,k2)

#exit(0)


m = "! (exists(G0:Int)[G0>=0&! G0 % 4 = 0&(5=G0+numStone())])& ( numStone()=2 or numStone()=3)"

print z3prover.imply(m,'false')


def delete_weak_clauses(clause_list):
	delete_list = list()
	for i in range(0,len(clause_list)):
		for j in range(i+1, len(clause_list)):
			if model_interpretor.interpret_result(z3prover.imply(clause_list[i],clause_list[j])) is True:
				delete_list.append(clause_list[j])
			elif model_interpretor.interpret_result(z3prover.imply(clause_list[j],clause_list[i])) is True:
				delete_list.append(clause_list[i])

	clause_list = [c for c in clause_list if c not in delete_list]
	return clause_list



from basic import context_operator


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


print __generate_para_action('p1')

l1 = delete_weak_clauses(f1)
l2 = delete_weak_clauses(f2)

from regression import atomic_regress
print '&'.join(l2)
print atomic_regress.regress('&'.join(l2), "take(p1,K12)")


#print __generate_pi_action('p1') 






