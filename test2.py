



from parser import BATparser
BATparser.parser('takeaway.sc')
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


    turnp1 = false if (Player1.Action = takep1_1) or (Player1.Action = takep1_2) or (Player1.Action = takep1_3);
    turnp1 = true if (Player1.Action = none);
    turnp2 = false if (Player2.Action = takep2_1) or (Player2.Action = takep2_2) or (Player2.Action = takep2_3);
    turnp2 = true if (Player2.Action = none);

'''


#or Player1.Action=none and Player2.Action=none


M = ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': True, 'numStone()': 1, 'turn(p2)': False})

Goal = "numStone()=0 => !turn(p1)"


from prover import mcmas

print mcmas.interpret_result(mcmas.check_win(M,Goal))




