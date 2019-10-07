



from parser import BATparser
BATparser.parser('new_chompNN.sc')
from basic import context_operator
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


#M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'False', 'xlen()': '1', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '1', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'})
M = ({'_S1': ['p2', 'p1'], 'Int': ['0','1'], 'Bool': ['True', 'False']}, {'turn(p2)': 'True', 'Ch(0,0)': 'False', 'turn(p1)': 'False', 'ylen()': '1',  'xlen()': '1'})
Goal = "!Ch(0,0) => turn(p1)"


from prover import mcmas
from prover import ispl_translator

#print ispl_translator.to_ispl(M,Goal)


print mcmas.interpret_result(mcmas.check_win(M,Goal))




