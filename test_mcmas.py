



from parser import BATparser

from regression import atomic_regress


'''
print context_operator.get_symbol_sorts_dict()
print 

print context_operator.get_sort_symbols_dict()

print context_operator.get_functions_sorts()


print context_operator.get_predicate_sorts()

print context_operator.get_fluents()

print context_operator.get_axioms()


print atomic_regress.poss_or_ssa('take(p1,1)','numStone()=0')
'''


#or Player1.Action=none and Player2.Action=none

#BATparser.parser('new_chompNN.sc')
#BATparser.parser('two_Nim.sc')
BATparser.parser('chompNN.sc')
from basic import context_operator


#M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'False', 'xlen()': '1', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '1', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'})
#M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1'], 'Bool': ['True', 'False']}, {'fpile()': '1', 'turn(p1)': 'True', 'spile()': '1', 'turn(p2)': 'False'}, {})
#Goal = "fpile() = 0 and spile() = 0 => !turn(p1)"



from prover import mcmas
from prover import ispl_translator
from basic import Util

#print ispl_translator.to_ispl(M,Goal)

def get_goal(player):
	lambda_fun, para_list = context_operator.find_axiom_with_feature('win', Util.generate_function_feature(player+'()'))
	Win = lambda_fun(para_list)
	End = context_operator.get_axioms()['end']['']
	return "( %s ) => ( %s )"%(End, Win)


def get_inital_database():
	return context_operator.get_axioms()['init']['']



M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'ylen()': '4', 'Ch(3,3)': 'False', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(0,3)': 'True', 'Ch(0,1)': 'True', 'Ch(4,0)': 'False', 'xlen()': '4'}, {'Ch\\(\\d+,\\d+\\)': 'False'})

#M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'ylen()': '4', 'Ch(3,3)': 'False', 'Ch(1,2)': 'True', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'True', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'True', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})


Goal = get_goal('p1')
Init = get_inital_database()

print mcmas.check_win(M, Goal,'p1')

from basic import format_output
print format_output.format_output(M,'Ch')

#M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
#print format_output.format_output(M,'Ch')
#print mcmas.check_reachability(M)





