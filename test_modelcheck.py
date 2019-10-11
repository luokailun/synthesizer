


from model import model_checker
from model import model_interpretor
from prover import z3prover
from formula import Conjunct
from parser import BATparser



'''
(0):(['G0'], ['_S1'], ['turn(G0)', 'turn(p2)'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '1', 'turn(p2)': 'True'})
(1):(['G0', 'X1'], ['Int', 'Int'], ['numStone() > G0', 'G0 > 4', '! numStone() >= X1'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4', '7', '6', '8'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '7', 'turn(p2)': 'False'})
(2):(['G0'], ['Int'], ['G0 = 4', 'numStone() = G0'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '4', 'turn(p2)': 'False'})

'''


#!(exists(G0:Int)[G0>=0 & G0 > 4 & !numStone() >= G0])


from algorithm import local_update
from formula import Predicate
BATparser.parser('new_chompNN.sc')
math_preds, fluent_preds = Predicate.generate_preds('new_chompNN.sc')

pred_list = math_preds + fluent_preds

pos_model_list = [
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
]

neg_model_list = [({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})]



#print pred_list
#preds = local_update.__generate_new_conjuncts(neg_model_list, pos_model_list, pred_list, 2)
#print preds

"""

OO
OO
-------
##
##
-------
##
##
-------
O#
O#
-------
OO
##
-------


O#
##
-------

"""

from formula import Conjunct

c_list = [([], [], ['Ch(0,0)', '! Ch(1,0)', "!Ch(0,1)"])]
c = (['X1','X2'], ['Int','Int'], ['Ch(0,0)', '! Ch(1,X1)', "! Ch(X2,1)"])

#print model_checker.sat_conjunct(neg_model_list, c)

M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})

M2 = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})

#print model_checker.unsat_conjunct([M2], c)
#exit(0)

#print model_checker.sat_conjunct([M], c)
print model_checker.sat_conjunct(neg_model_list, c)
print
#print model_checker.unsat_conjunct(pos_model_list, c)
for m in pos_model_list:
	print m
	print model_checker.unsat_conjunct([m], c)



print Conjunct.get_characteristic_conjuncts([c], neg_model_list, pos_model_list)


