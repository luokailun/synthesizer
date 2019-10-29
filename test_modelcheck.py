


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

g_pos_model_list = [
  #({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  #({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'True', 'Ch(0,3)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'Ch(0,1)': 'True', 'turn(p1)': 'True', 'xlen()': '3', 'Ch(3,1)': 'False', 'Ch(3,0)': 'False', 'Ch(2,1)': 'True', 'Ch(2,0)': 'True', 'Ch(2,2)': 'True', 'ylen()': '3', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,3)': 'False', 'Ch(2,3)': 'False', 'Ch(1,2)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
  #({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  # ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
  ]


pos_model_list = [
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'True', 'Ch(1,0)': 'True', 'Ch(0,2)': 'True', 'Ch(0,3)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'Ch(0,1)': 'True', 'turn(p1)': 'True', 'xlen()': '3', 'Ch(3,1)': 'False', 'Ch(3,0)': 'False', 'Ch(2,1)': 'True', 'Ch(2,0)': 'True', 'Ch(2,2)': 'True', 'ylen()': '3', 'Ch(3,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,3)': 'False', 'Ch(2,3)': 'False', 'Ch(1,2)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'False', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'False', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'False', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'False'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'False', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'True', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'False', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'}),
  ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4'], 'Bool': ['True', 'False']}, {'Ch(1,0)': 'True', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(2,3)': 'False', 'Ch(1,4)': 'False', 'Ch(3,1)': 'False', 'Ch(3,3)': 'False', 'ylen()': '4', 'Ch(1,2)': 'False', 'Ch(0,2)': 'True', 'Ch(0,0)': 'True', 'Ch(4,3)': 'False', 'Ch(4,1)': 'False', 'Ch(4,4)': 'False', 'Ch(3,4)': 'False', 'Ch(1,1)': 'False', 'Ch(2,0)': 'True', 'Ch(2,2)': 'False', 'turn(p1)': 'True', 'Ch(4,2)': 'False', 'Ch(1,3)': 'False', 'Ch(3,0)': 'False', 'Ch(0,4)': 'False', 'Ch(3,2)': 'False', 'Ch(2,4)': 'False', 'Ch(0,3)': 'True', 'xlen()': '4', 'Ch(4,0)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})
  ]

neg_model_list = [({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2'], 'Bool': ['True', 'False']}, {'Ch(1,1)': 'False', 'Ch(1,0)': 'True', 'Ch(0,2)': 'False', 'Ch(2,1)': 'False', 'turn(p2)': 'False', 'Ch(0,0)': 'True', 'xlen()': '2', 'turn(p1)': 'True', 'Ch(2,0)': 'False', 'Ch(2,2)': 'False', 'ylen()': '2', 'Ch(1,2)': 'False', 'Ch(0,1)': 'True'}, {'Ch\\(\\d+,\\d+\\)': 'False'})]



from algorithm import local_update


#conjunct_list = Conjunct.generate_conjuncts([([],[],[])], neg_model_list, g_pos_model_list, pred_list, 3)
#print conjunct_list


conjunct_list = Conjunct.generate_conjuncts([([],[],[])], g_pos_model_list, neg_model_list, pred_list, 2)
print conjunct_list



'''
from formula import Xconjunct

pred_list = math_preds + fluent_preds
basic_conjunct_list = [(v_list, s_list, [pred]) for v_list, s_list, pred in pred_list]

#print basic_conjunct_list
#exit(0)
#basic_conjunct_list = [([], [], ['Ch(1,1)'])]
basic_conjunct_list = Xconjunct.unify_conjuncts(basic_conjunct_list)

#print basic_conjunct_list
#exit(0)
empty_conjunct = ([],[],[])
#print Xconjunct.generate_conjunct(empty_conjunct, neg_model_list, pos_model_list, basic_conjunct_list, 3)
print Xconjunct.generate_conjunct(empty_conjunct, pos_model_list, neg_model_list, basic_conjunct_list, 3)

OO
OO
-------
OOO
OOO
OOO
-------
##
##
-------
####
####
####
####
-------
O#
O#
-------
OO
##
-------
O###
O###
O###
O###
-------
OO##
O###
O###
O###
-------
OOO#
O###
O###
O###
-------
OOOO
####
####
####
-------
OOOO
O###
####
####
-------
OOOO
O###
O###
####
-------

['G0 = 1', '! Ch(1,G0)']
['G0 > 0', 'Ch(0,G0)']

forall ['Ch(G0,G1)', '! Ch(G1,G0)']

'''

print 
print
#formula = "exists(G0:Int)[G0 = 1 and ! Ch(1,G0)] and exists(G0:Int)[G0 > 0 and Ch(0,G0)] and forall(G0:Int,G1:Int)[!Ch(G0,G1) or Ch(G1,G0)]"

#print model_checker.sat_formula_math(neg_model_list[0],formula)




for model in pos_model_list:
	print model 
	print model_checker.sat_formula_math(model,formula)


print
print '-------------------------------'
print 

print model_checker.sat_formula_math(neg_model_list[0],formula)

#['G0 > 0', 'Ch(1,G0)']




