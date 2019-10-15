


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
BATparser.parser('chompNN.sc')
math_preds, fluent_preds = Predicate.generate_preds('chompNN.sc')

pred_list = math_preds + fluent_preds

'''
pos_model_list = [
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
,({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
]

neg_model_list = [({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})]
'''


#print pred_list

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

pos_model_list = [
 ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
  #,({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,2)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'False', 'Ch(2,4)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
]

neg_model_list = [({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'True', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})]



from algorithm import local_update

#conjunct_list = local_update.__generate_new_conjuncts(neg_model_list, pos_model_list, pred_list, 3)
#print conjunct_list

conjunct_list = Conjunct.generate_conjuncts([([],[],[])], neg_model_list, pos_model_list, pred_list, 2)
print conjunct_list


#conjunct_list = local_update.__generate_new_conjuncts(pos_model_list, neg_model_list, pred_list, 3)
#print conjunct_list










