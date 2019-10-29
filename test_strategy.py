


#from strategy import strategy
from parser import BATparser
from basic import context_operator
from basic import Util


def get_goal(player):
	lambda_fun, para_list = context_operator.find_axiom_with_feature('win', Util.generate_function_feature(player+'()'))
	Win = lambda_fun(para_list)
	End = context_operator.get_axioms()['end']['']
	return "( %s ) => ( %s )"%(End, Win)



U = {'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5', '6'], 'Bool': ['True', 'False']}


BATparser.parser('empty.sc')

from strategy import strategy
#print strategy.get_init_models_with_universe(M)
#exit(0)


M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5','6'], 'Bool': ['True', 'False']}, {'turn(p2)': 'True', 'turn(p1)': 'False', 'chip1()': '1', 'chip2()': '5'}, {})
Goal = get_goal('p1')

#from basic import format_output
#print format_output.format_output(M,'Ch')

models =  strategy.get_init_models_with_universe(U)

print models

strategy_list = list()

for model in models:
	strategy_list.append(strategy.check_and_get_strategy(model, Goal, 'p1'))

#print strategy_list

print strategy.find_model_in_strategies(M, strategy_list)