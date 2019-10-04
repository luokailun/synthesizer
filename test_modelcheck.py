


from model import model_checker
from model import model_interpretor
from prover import z3prover
from formula import Conjunct
from parser import BATparser
BATparser.parser('takeaway.sc')


'''
(0):(['G0'], ['_S1'], ['turn(G0)', 'turn(p2)'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'False', 'numStone()': '1', 'turn(p2)': 'True'})
(1):(['G0', 'X1'], ['Int', 'Int'], ['numStone() > G0', 'G0 > 4', '! numStone() >= X1'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4', '7', '6', '8'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '7', 'turn(p2)': 'False'})
(2):(['G0'], ['Int'], ['G0 = 4', 'numStone() = G0'])
  ({'_S1': ['p2', 'p1'], 'Int': ['1', '0', '3', '2', '5', '4'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '4', 'turn(p2)': 'False'})

'''


#!(exists(G0:Int)[G0>=0 & G0 > 4 & !numStone() >= G0])


M = ({'_S1': ['p2', 'p1'], 'Int': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12'], 'Bool': ['True', 'False']}, {'turn(p1)': 'True', 'numStone()': '11', 'turn(p2)': 'False'})
C1 = (['G0'], ['_S1'], ['turn(G0)', 'turn(p2)'])
C2 = (['G0', 'X1'], ['Int', 'Int'], ['numStone() > G0', 'G0 > 4', '! numStone() >= X1'])
C3 = (['G0'], ['Int'], ['G0 = 4', 'numStone() = G0'])
print model_checker.sat_conjunct_by_model(M,C1)
print model_checker.sat_conjunct_by_model(M,C2)
print model_checker.sat_conjunct_by_model(M,C3)




