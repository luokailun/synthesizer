
from parser import BATparser
from basic import context_operator
from basic import Util
from formula import Predicate
import re

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

def get_end():
	End = context_operator.get_axioms()['end']['']
	return End

def __before_verify(domain_file):
	BATparser.parser(domain_file) 
	#__load_state_constaints(domain_name)


__before_verify('chompNN.sc')

Init = get_inital_database()
Goal = get_goal('p1')
End = get_end()
#pi_action = generate_pi_action()
math_preds, fluent_preds = Predicate.generate_preds('chompNN.sc')


from regression import program_regress
from algorithm import algorithm2 



#F = "!(exists(G0:Int)[G0>=0&spile() >= G0&! fpile() > G0])"
#print 
#print program_regress.A_regress(F, algorithm2.__generate_pi_action('p2'))
#print program_regress.A_regress(F, algorithm2.__generate_pi_action('p2'))
#exit(0)

algorithm2.synthesis(Init, End, Goal, 'p1', math_preds+fluent_preds)








