
from parser import BATparser
from basic import context_operator
from basic import Util
from formula import Predicate
import re
#from parser import util_pred

from regression import program_regress


def __get_vars(sorts):
	return [ (context_operator.get_new_var(), sort) for sort in sorts]


def generate_pi_action():
	functions_sorts = context_operator.get_functions_sorts()

	actions_sorts = [ (fun, sorts) for fun, sorts in functions_sorts.iteritems() if fun in context_operator.get_actions() ]
	action_vars_sorts = [ (action, __get_vars(sorts[0:len(sorts)-1])) for action, sorts in actions_sorts]
	actions = "#".join([  "%s(%s)" % (action ,",".join(zip(*elem)[0])) for action, elem in action_vars_sorts])
	#print "---------",actions
	vars_sorts = ','.join([elem[0] + ":" + elem[1] for action, elem_list in action_vars_sorts for elem in elem_list])

	return "pi(" + vars_sorts + ")[" + actions +"]"


def get_inital_database():
	return context_operator.get_axioms()['init']['']

def get_goal(player):
	lambda_fun, para_list = context_operator.find_axiom_with_feature('win', Util.generate_function_feature(player+'()'))
	Win = lambda_fun(para_list)
	End = context_operator.get_axioms()['end']['']
	return "( %s ) => ( %s )"%(End, Win)


def __before_verify(domain_file):
	BATparser.parser(domain_file)
	#__load_state_constaints(domain_name)


__before_verify('new_chomp2N.sc')

Init = get_inital_database()
Goal = get_goal('p1')
#pi_action = generate_pi_action()

math_preds, fluent_preds = Predicate.genPreds('new_chomp2N.sc')

#print math_preds+fluent_preds
#exit(0)

import algorithm
algorithm.synthesis(Init, Goal, math_preds+fluent_preds)







#( !Ch(1,1) ) => ( !Ch(1,1)&turn(p1) )
#pi(K27:_S1,K28:Int,K29:Int)[eat(K27,K28,K29)]
#forall(K27:_S1,K28:Int,K29:Int)[ (Ch(K28,K29)&turn(K27) => ( !(Ch(1,1)&(K28>1|K29>1)) ) => ( !(Ch(1,1)&(K28>1|K29>1))&(!turn(p1)) )) ]


#print Goal
#print pi_action
#pi(K27:_S1,K28:Int,K29:Int)[eat(K27,K28,K29)]
#A_formula = program_regress.A_regress(Goal, pi_action)
#E_formula = program_regress.E_regress(Goal, pi_action)

#print A_formula
#print E_formula


#from prover import z3prover

#results = z3prover.imply(A_formula, Goal, z3prover.generate_head())

#print results

#from model import model_interpretor

#print model_interpretor.interpret_result(results)

